"""Servidor principal. Entrega las páginas HTML y expone la API en /api/..."""
import os

import pymysql
from flask import Flask, abort, jsonify, request

import config
from db import cerrar_db
from routes import auth, clientes, pagos, pedidos, productos, reportes

# La carpeta raíz del proyecto (donde está index.html) está un nivel arriba de backend/
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, static_folder=RAIZ, static_url_path='')
app.config.update(
    SECRET_KEY=config.SECRET_KEY,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    MAX_CONTENT_LENGTH=1024 * 1024,  # 1 MB como máximo por petición
)

# Al terminar cada petición se cierra la conexión a MySQL
app.teardown_appcontext(cerrar_db)

for modulo in (auth, clientes, pedidos, pagos, productos, reportes):
    app.register_blueprint(modulo.bp)


@app.before_request
def proteger_codigo():
    """Como se sirve toda la carpeta del proyecto, se bloquea el código del servidor."""
    ruta = request.path.lower()
    if ruta.startswith('/backend') or '/.' in ruta:
        abort(404)


@app.get('/')
def inicio():
    return app.send_static_file('index.html')


@app.errorhandler(pymysql.err.IntegrityError)
def error_integridad(error):
    return jsonify(error='El registro ya existe o tiene datos relacionados.'), 409


@app.errorhandler(pymysql.err.MySQLError)
def error_mysql(error):
    app.logger.exception('Error de MySQL')
    return jsonify(error='Error en la base de datos.'), 500


if __name__ == '__main__':
    # debug=True solo para desarrollo: nunca se usa en un servidor real
    app.run(host='127.0.0.1', port=5000, debug=True)
