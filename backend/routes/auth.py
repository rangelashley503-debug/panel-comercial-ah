"""Inicio de sesión, cierre de sesión y registro comercial."""
import pymysql
from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from auth_utils import usuario_actual
from db import consultar, ejecutar
from validaciones import (correo_valido, password_valida, rfc_valido,
                          telefono_valido, texto)

bp = Blueprint('auth', __name__, url_prefix='/api')

ROLES = ('Vendedor', 'Almacén', 'Administrador', 'Cliente')


@bp.post('/login')
def login():
    datos = request.get_json(silent=True) or {}
    correo = texto(datos.get('correo')).lower()
    password = datos.get('password') or ''
    rol = texto(datos.get('rol'))

    usuario = consultar(
        'SELECT id, correo, password_hash, rol, cliente_id FROM usuarios WHERE correo = %s',
        (correo,), uno=True)

    # Mismo mensaje para cualquier fallo: no se revela si el correo existe
    if (usuario is None or rol not in ROLES or usuario['rol'] != rol
            or not check_password_hash(usuario['password_hash'], password)):
        return jsonify(error='Correo, contraseña o rol incorrectos.'), 401

    # Una cuenta comercial suspendida o pendiente de aprobación no puede entrar
    if usuario['cliente_id']:
        cliente = consultar('SELECT estatus FROM clientes WHERE id = %s',
                            (usuario['cliente_id'],), uno=True)
        if cliente is None or cliente['estatus'] != 'Activo':
            return jsonify(error='Tu cuenta está pendiente de aprobación o suspendida.'), 403

    session.clear()
    session['usuario'] = {
        'id': usuario['id'],
        'correo': usuario['correo'],
        'rol': usuario['rol'],
        'cliente_id': usuario['cliente_id'],
    }
    return jsonify(ok=True, rol=usuario['rol'], correo=usuario['correo'])


@bp.post('/logout')
def logout():
    session.clear()
    return jsonify(ok=True)


@bp.get('/sesion')
def sesion():
    usuario = usuario_actual()
    if usuario is None:
        return jsonify(error='Sin sesión.'), 401
    return jsonify(usuario)


@bp.post('/registro')
def registro():
    datos = request.get_json(silent=True) or {}
    razon = texto(datos.get('razon'))
    rfc = texto(datos.get('rfc')).upper()
    telefono = texto(datos.get('telefono'))
    correo = texto(datos.get('correo')).lower()
    password = datos.get('password') or ''

    if not razon or len(razon) > 120:
        return jsonify(error='Escribe la razón social del negocio.'), 400
    if not rfc_valido(rfc):
        return jsonify(error='El RFC no tiene un formato válido.'), 400
    if not telefono_valido(telefono):
        return jsonify(error='El teléfono debe tener 10 dígitos.'), 400
    if not correo_valido(correo):
        return jsonify(error='Escribe un correo electrónico válido.'), 400
    if not password_valida(password):
        return jsonify(error='La contraseña debe tener al menos 8 caracteres e incluir un número.'), 400

    try:
        # La cuenta queda Suspendida hasta que un administrador la apruebe
        cliente_id = ejecutar(
            'INSERT INTO clientes (tienda, rfc, telefono, estatus) VALUES (%s, %s, %s, %s)',
            (razon, rfc, telefono, 'Suspendido'), commit=False)
        ejecutar(
            'INSERT INTO usuarios (correo, password_hash, rol, cliente_id) VALUES (%s, %s, %s, %s)',
            (correo, generate_password_hash(password), 'Cliente', cliente_id))
    except pymysql.err.IntegrityError:
        return jsonify(error='Ese RFC o correo ya está registrado.'), 409

    return jsonify(ok=True, mensaje='Solicitud enviada. Un administrador revisará tus datos.'), 201
