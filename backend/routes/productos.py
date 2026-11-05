"""Catálogo de productos e inventario."""
from flask import Blueprint, jsonify

from auth_utils import rol_requerido
from db import consultar

bp = Blueprint('productos', __name__, url_prefix='/api/productos')


@bp.get('')
@rol_requerido()
def listar():
    """Catálogo completo (cualquier usuario con sesión iniciada)."""
    return jsonify(consultar(
        'SELECT id, nombre, categoria, precio_pieza, piezas_por_caja, cajas_por_tarima, existencia_cajas '
        'FROM productos ORDER BY categoria, nombre'))


@bp.get('/stock-minimo')
@rol_requerido('Administrador', 'Vendedor', 'Almacén')
def stock_minimo():
    """Productos con existencia por debajo del mínimo."""
    return jsonify(consultar(
        'SELECT id, nombre, existencia_cajas AS existencia, stock_minimo_cajas AS minimo '
        'FROM productos WHERE existencia_cajas < stock_minimo_cajas ORDER BY nombre'))
