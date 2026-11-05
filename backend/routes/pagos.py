"""Pagos, corte de caja y cierre de turno."""
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request

from auth_utils import rol_requerido, usuario_actual
from db import consultar, ejecutar
from validaciones import texto

bp = Blueprint('pagos', __name__, url_prefix='/api')

METODOS = ['Efectivo', 'Tarjeta', 'Transferencia']


def turno_abierto():
    return consultar("SELECT id, abierto_en FROM turnos WHERE estatus = 'Abierto' ORDER BY id DESC LIMIT 1",
                     uno=True)


def armar_corte(turno):
    """Suma los pagos del turno por método (siempre devuelve los tres métodos)."""
    filas = consultar(
        'SELECT metodo, COUNT(*) AS operaciones, COALESCE(SUM(monto), 0) AS monto '
        'FROM pagos WHERE turno_id = %s GROUP BY metodo', (turno['id'],))
    por_metodo = {fila['metodo']: fila for fila in filas}

    metodos = []
    for nombre in METODOS:
        fila = por_metodo.get(nombre, {'operaciones': 0, 'monto': 0})
        metodos.append({'metodo': nombre, 'operaciones': fila['operaciones'], 'monto': fila['monto']})

    return {
        'turno_id': turno['id'],
        'metodos': metodos,
        'total_operaciones': sum(m['operaciones'] for m in metodos),
        'total_monto': round(sum(m['monto'] for m in metodos), 2),
    }


@bp.post('/pagos')
@rol_requerido('Administrador', 'Vendedor')
def registrar_pago():
    datos = request.get_json(silent=True) or {}
    metodo = texto(datos.get('metodo'))

    try:
        monto = Decimal(str(datos.get('monto'))).quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError):
        return jsonify(error='Escribe un monto válido.'), 400
    if metodo not in METODOS:
        return jsonify(error='Método de pago no válido.'), 400
    if monto <= 0 or monto > Decimal('10000000'):
        return jsonify(error='El monto debe ser mayor a 0.'), 400

    pedido_id = datos.get('pedido_id')
    if pedido_id is not None:
        try:
            pedido_id = int(pedido_id)
        except (TypeError, ValueError):
            return jsonify(error='Pedido no válido.'), 400
        if consultar('SELECT id FROM pedidos WHERE id = %s', (pedido_id,), uno=True) is None:
            return jsonify(error='El pedido no existe.'), 404

    # Si no hay turno abierto, el primer pago lo abre
    turno = turno_abierto()
    if turno is None:
        turno_id = ejecutar('INSERT INTO turnos (abierto_por) VALUES (%s)', (usuario_actual()['id'],))
    else:
        turno_id = turno['id']

    pago_id = ejecutar(
        'INSERT INTO pagos (turno_id, pedido_id, metodo, monto) VALUES (%s, %s, %s, %s)',
        (turno_id, pedido_id, metodo, monto))
    return jsonify(id=pago_id), 201


@bp.get('/corte')
@rol_requerido('Administrador', 'Vendedor')
def corte():
    alertas = consultar(
        'SELECT COUNT(*) AS total FROM productos WHERE existencia_cajas < stock_minimo_cajas', uno=True)['total']

    turno = turno_abierto()
    if turno is None:
        return jsonify(turno_id=None, estado='Sin turno abierto', metodos=[{'metodo': m, 'operaciones': 0, 'monto': 0} for m in METODOS],
                       total_operaciones=0, total_monto=0, alertas_stock=alertas)

    resultado = armar_corte(turno)
    resultado.update(estado='Turno abierto', alertas_stock=alertas)
    return jsonify(resultado)


@bp.post('/turno/cerrar')
@rol_requerido('Administrador', 'Vendedor')
def cerrar_turno():
    turno = turno_abierto()
    if turno is None:
        return jsonify(error='No hay un turno abierto.'), 404

    resultado = armar_corte(turno)
    ejecutar("UPDATE turnos SET estatus = 'Cerrado', cerrado_en = NOW() WHERE id = %s", (turno['id'],))
    resultado.update(estado='Turno cerrado')
    return jsonify(resultado)
