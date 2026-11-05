"""Clientes y cuentas comerciales."""
import pymysql
from flask import Blueprint, jsonify, request

from auth_utils import rol_requerido
from db import consultar, ejecutar
from validaciones import cp_valido, rfc_valido, telefono_valido, texto

bp = Blueprint('clientes', __name__, url_prefix='/api/clientes')

COLUMNAS = 'id, tienda, rfc, contacto, telefono, direccion, ciudad, cp, referencias, estatus'


@bp.get('')
@rol_requerido('Administrador', 'Vendedor')
def listar():
    busqueda = texto(request.args.get('q'))
    if busqueda:
        patron = '%' + busqueda + '%'
        filas = consultar(
            'SELECT ' + COLUMNAS + ' FROM clientes WHERE tienda LIKE %s OR rfc LIKE %s ORDER BY id DESC',
            (patron, patron))
    else:
        filas = consultar('SELECT ' + COLUMNAS + ' FROM clientes ORDER BY id DESC')
    return jsonify(filas)


@bp.post('')
@rol_requerido('Administrador', 'Vendedor')
def crear():
    datos = request.get_json(silent=True) or {}
    tienda = texto(datos.get('tienda'))
    rfc = texto(datos.get('rfc')).upper()
    contacto = texto(datos.get('contacto'))
    telefono = texto(datos.get('telefono'))
    direccion = texto(datos.get('direccion'))
    ciudad = texto(datos.get('ciudad'))
    cp = texto(datos.get('cp'))
    referencias = texto(datos.get('referencias'))
    estatus = texto(datos.get('estatus')) or 'Activo'

    if not tienda or not contacto or not direccion or not ciudad:
        return jsonify(error='Completa nombre, contacto, dirección y ciudad.'), 400
    if not rfc_valido(rfc):
        return jsonify(error='El RFC no tiene un formato válido.'), 400
    if not telefono_valido(telefono):
        return jsonify(error='El teléfono debe tener 10 dígitos.'), 400
    if not cp_valido(cp):
        return jsonify(error='El código postal debe tener 5 dígitos.'), 400
    if estatus not in ('Activo', 'Suspendido'):
        return jsonify(error='Estatus no válido.'), 400

    try:
        nuevo_id = ejecutar(
            'INSERT INTO clientes (tienda, rfc, contacto, telefono, direccion, ciudad, cp, referencias, estatus) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (tienda, rfc, contacto, telefono, direccion, ciudad, cp, referencias, estatus))
    except pymysql.err.IntegrityError:
        return jsonify(error='Ya existe un cliente con ese RFC.'), 409

    return jsonify(id=nuevo_id), 201


@bp.patch('/<int:cliente_id>/estatus')
@rol_requerido('Administrador')
def cambiar_estatus(cliente_id):
    datos = request.get_json(silent=True) or {}
    estatus = texto(datos.get('estatus'))
    if estatus not in ('Activo', 'Suspendido'):
        return jsonify(error='Estatus no válido.'), 400

    if consultar('SELECT id FROM clientes WHERE id = %s', (cliente_id,), uno=True) is None:
        return jsonify(error='Cliente no encontrado.'), 404

    ejecutar('UPDATE clientes SET estatus = %s WHERE id = %s', (estatus, cliente_id))
    return jsonify(ok=True, estatus=estatus)
