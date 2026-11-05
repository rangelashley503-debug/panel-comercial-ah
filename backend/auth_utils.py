"""Control de acceso: quién inició sesión y qué rol tiene."""
from functools import wraps
from flask import session, jsonify


def usuario_actual():
    return session.get('usuario')


def rol_requerido(*roles):
    """Decorador: exige sesión iniciada y, si se indican roles, que el rol coincida."""
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            usuario = usuario_actual()
            if usuario is None:
                return jsonify(error='Inicia sesión para continuar.'), 401
            if roles and usuario['rol'] not in roles:
                return jsonify(error='No tienes permiso para esta acción.'), 403
            return funcion(*args, **kwargs)
        return envoltura
    return decorador
