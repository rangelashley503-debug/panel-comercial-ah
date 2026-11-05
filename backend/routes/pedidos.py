"""Pedidos, cotizaciones y surtido de almacén."""
import math
from datetime import datetime
from decimal import Decimal

from flask import Blueprint, jsonify, request

from auth_utils import rol_requerido, usuario_actual
from db import consultar, ejecutar, get_db
from validaciones import texto

bp = Blueprint('pedidos', __name__, url_prefix='/api/pedidos')

ESTATUS = ['Registrado', 'En preparación', 'Listo / En ruta', 'Entregado']
ESCALAS = ['Pieza', 'Caja', 'Tarima']


def piezas_por_escala(producto, escala):
    """Cuántas piezas trae una unidad de la escala elegida."""
    if escala == 'Pieza':
        return 1
    if escala == 'Caja':
        return producto['piezas_por_caja']
    return producto['piezas_por_caja'] * producto['cajas_por_tarima']


def armar_lineas(items):
    """Valida los productos pedidos y calcula piezas y subtotal con los precios de la base de datos.
    Devuelve (lineas, total, error). Los precios nunca se toman del navegador."""
    if not isinstance(items, list) or not items or len(items) > 50:
        return None, None, 'Agrega al menos un producto.'

    lineas = []
    total = Decimal('0')
    for item in items:
        if not isinstance(item, dict):
            return None, None, 'Producto no válido.'
        escala = texto(item.get('escala'))
        try:
            producto_id = int(item.get('producto_id'))
            cantidad = int(item.get('cantidad'))
        except (TypeError, ValueError):
            return None, None, 'Producto o cantidad no válidos.'
        if escala not in ESCALAS or cantidad < 1 or cantidad > 100000:
            return None, None, 'Escala o cantidad no válidas.'

        producto = consultar(
            'SELECT id, nombre, precio_pieza, piezas_por_caja, cajas_por_tarima FROM productos WHERE id = %s',
            (producto_id,), uno=True)
        if producto is None:
            return None, None, 'El producto no existe.'

        piezas = piezas_por_escala(producto, escala) * cantidad
        subtotal = (Decimal(str(producto['precio_pieza'])) * piezas).quantize(Decimal('0.01'))
        total += subtotal
        lineas.append({'producto_id': producto_id, 'escala': escala,
                       'cantidad': cantidad, 'piezas': piezas, 'subtotal': subtotal})
    return lineas, total, None


@bp.get('')
@rol_requerido('Administrador', 'Vendedor', 'Almacén')
def listar():
    filtro = texto(request.args.get('estatus'))
    sql = ('SELECT p.id, p.folio, c.tienda AS cliente, p.volumen, p.total, p.estatus, p.fecha_entrega '
           'FROM pedidos p JOIN clientes c ON c.id = p.cliente_id ')
    if filtro in ESTATUS:
        filas = consultar(sql + 'WHERE p.estatus = %s ORDER BY p.id DESC', (filtro,))
    else:
        filas = consultar(sql + 'ORDER BY p.id DESC')
    return jsonify(filas)


@bp.get('/resumen')
@rol_requerido('Administrador', 'Vendedor', 'Almacén')
def resumen():
    filas = consultar('SELECT estatus, COUNT(*) AS total FROM pedidos GROUP BY estatus')
    conteo = {fila['estatus']: fila['total'] for fila in filas}
    return jsonify(
        nuevos=conteo.get('Registrado', 0),
        en_preparacion=conteo.get('En preparación', 0),
        en_ruta=conteo.get('Listo / En ruta', 0),
        entregados=conteo.get('Entregado', 0),
    )


@bp.post('/cotizar')
@rol_requerido('Administrador', 'Vendedor')
def cotizar():
    """Calcula el total sin guardar nada (botón 'Generar Cotización')."""
    datos = request.get_json(silent=True) or {}
    lineas, total, error = armar_lineas(datos.get('items'))
    if error:
        return jsonify(error=error), 400
    return jsonify(total=float(total), lineas=[
        {**linea, 'subtotal': float(linea['subtotal'])} for linea in lineas])


@bp.post('')
@rol_requerido('Administrador', 'Vendedor')
def crear():
    datos = request.get_json(silent=True) or {}

    try:
        cliente_id = int(datos.get('cliente_id'))
    except (TypeError, ValueError):
        return jsonify(error='Selecciona un cliente.'), 400
    cliente = consultar('SELECT id, estatus FROM clientes WHERE id = %s', (cliente_id,), uno=True)
    if cliente is None:
        return jsonify(error='El cliente no existe.'), 404
    if cliente['estatus'] != 'Activo':
        return jsonify(error='El cliente está suspendido.'), 400

    fecha_entrega = texto(datos.get('fecha_entrega')) or None
    if fecha_entrega:
        try:
            datetime.strptime(fecha_entrega, '%Y-%m-%d')
        except ValueError:
            return jsonify(error='Fecha de entrega no válida.'), 400

    lineas, total, error = armar_lineas(datos.get('items'))
    if error:
        return jsonify(error=error), 400

    # El volumen del pedido es la escala más grande que contiene
    volumen = max((linea['escala'] for linea in lineas), key=ESCALAS.index)

    # Todo el pedido se guarda junto: si algo falla, no queda a medias
    pedido_id = ejecutar(
        'INSERT INTO pedidos (cliente_id, volumen, total, fecha_entrega, observaciones, creado_por) '
        'VALUES (%s, %s, %s, %s, %s, %s)',
        (cliente_id, volumen, total, fecha_entrega, texto(datos.get('observaciones')),
         usuario_actual()['id']), commit=False)
    folio = '#PED-' + str(1020 + pedido_id)
    ejecutar('UPDATE pedidos SET folio = %s WHERE id = %s', (folio, pedido_id), commit=False)
    for linea in lineas:
        ejecutar(
            'INSERT INTO detalle_pedido (pedido_id, producto_id, escala, cantidad, piezas, subtotal) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (pedido_id, linea['producto_id'], linea['escala'], linea['cantidad'],
             linea['piezas'], linea['subtotal']), commit=False)
    get_db().commit()

    return jsonify(id=pedido_id, folio=folio, total=float(total)), 201


@bp.patch('/<int:pedido_id>/estatus')
@rol_requerido('Administrador', 'Vendedor', 'Almacén')
def cambiar_estatus(pedido_id):
    datos = request.get_json(silent=True) or {}
    nuevo = texto(datos.get('estatus'))
    if nuevo not in ESTATUS:
        return jsonify(error='Estatus no válido.'), 400

    pedido = consultar('SELECT estatus FROM pedidos WHERE id = %s', (pedido_id,), uno=True)
    if pedido is None:
        return jsonify(error='Pedido no encontrado.'), 404

    # Solo se puede avanzar al siguiente estatus, sin saltarse etapas
    if ESTATUS.index(nuevo) != ESTATUS.index(pedido['estatus']) + 1:
        return jsonify(error='El pedido solo puede avanzar al siguiente estatus.'), 400
    # El almacén prepara y despacha; confirmar la entrega es de ventas
    if nuevo == 'Entregado' and usuario_actual()['rol'] == 'Almacén':
        return jsonify(error='No tienes permiso para marcar entregas.'), 403

    ejecutar('UPDATE pedidos SET estatus = %s WHERE id = %s', (nuevo, pedido_id))
    return jsonify(ok=True, estatus=nuevo)


@bp.get('/<int:pedido_id>/surtido')
@rol_requerido('Administrador', 'Almacén')
def hoja_surtido(pedido_id):
    pedido = consultar(
        'SELECT p.id, p.folio, c.tienda AS cliente, p.estatus FROM pedidos p '
        'JOIN clientes c ON c.id = p.cliente_id WHERE p.id = %s', (pedido_id,), uno=True)
    if pedido is None:
        return jsonify(error='Pedido no encontrado.'), 404

    filas = consultar(
        'SELECT pr.nombre AS producto, d.piezas, pr.piezas_por_caja, pr.lote, pr.caducidad '
        'FROM detalle_pedido d JOIN productos pr ON pr.id = d.producto_id '
        'WHERE d.pedido_id = %s ORDER BY d.id', (pedido_id,))
    for fila in filas:
        # La hoja de surtido se maneja en cajas
        fila['cajas'] = math.ceil(fila['piezas'] / fila['piezas_por_caja'])
    return jsonify(pedido=pedido, productos=filas)


@bp.patch('/<int:pedido_id>/listo')
@rol_requerido('Administrador', 'Almacén')
def marcar_listo(pedido_id):
    """Botón 'Marcar como Listo para ruta': descuenta el inventario y cambia el estatus."""
    pedido = consultar('SELECT estatus FROM pedidos WHERE id = %s', (pedido_id,), uno=True)
    if pedido is None:
        return jsonify(error='Pedido no encontrado.'), 404
    if pedido['estatus'] not in ('Registrado', 'En preparación'):
        return jsonify(error='Este pedido ya salió del almacén.'), 400

    lineas = consultar(
        'SELECT d.producto_id, d.piezas, pr.piezas_por_caja, pr.nombre '
        'FROM detalle_pedido d JOIN productos pr ON pr.id = d.producto_id WHERE d.pedido_id = %s',
        (pedido_id,))

    for linea in lineas:
        cajas = math.ceil(linea['piezas'] / linea['piezas_por_caja'])
        # El descuento solo se aplica si hay existencia suficiente
        filas = ejecutar(
            'UPDATE productos SET existencia_cajas = existencia_cajas - %s '
            'WHERE id = %s AND existencia_cajas >= %s',
            (cajas, linea['producto_id'], cajas), commit=False)
        if filas == 0:
            get_db().rollback()
            return jsonify(error='Existencia insuficiente de ' + linea['nombre'] + '.'), 409

    ejecutar('UPDATE pedidos SET estatus = %s WHERE id = %s', ('Listo / En ruta', pedido_id), commit=False)
    get_db().commit()
    return jsonify(ok=True, estatus='Listo / En ruta')
