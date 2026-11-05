"""Reportes del panel administrativo."""
from flask import Blueprint, jsonify, request

from auth_utils import rol_requerido
from db import consultar
from validaciones import texto

bp = Blueprint('reportes', __name__, url_prefix='/api/reportes')

CATEGORIAS = ('Energizantes', 'Isotónicas', 'Confitería')


@bp.get('/mas-vendidos')
@rol_requerido('Administrador', 'Vendedor')
def mas_vendidos():
    categoria = texto(request.args.get('categoria'))
    sql = ('SELECT p.nombre AS producto, p.categoria, '
           'ROUND(SUM(d.piezas) / p.piezas_por_caja) AS cajas, SUM(d.subtotal) AS ingresos '
           'FROM detalle_pedido d JOIN productos p ON p.id = d.producto_id ')
    if categoria in CATEGORIAS:
        filas = consultar(sql + 'WHERE p.categoria = %s GROUP BY p.id ORDER BY cajas DESC LIMIT 10', (categoria,))
    else:
        filas = consultar(sql + 'GROUP BY p.id ORDER BY cajas DESC LIMIT 10')
    return jsonify(filas)
