"""Conexión a MySQL. Se abre una conexión por petición y se cierra al terminar."""
import datetime
import decimal

import pymysql
from pymysql.cursors import DictCursor
from flask import g

import config


def conectar(con_base=True):
    return pymysql.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME if con_base else None,
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=False,
    )


def get_db():
    # Si la petición actual aún no tiene conexión, se crea
    if 'db' not in g:
        g.db = conectar()
    return g.db


def cerrar_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        # Lo que no se confirmó con commit() se descarta
        db.close()


def _normalizar(fila):
    """Decimal -> número y fechas -> texto ISO, para poder convertir la fila a JSON."""
    if fila is None:
        return None
    for clave, valor in fila.items():
        if isinstance(valor, decimal.Decimal):
            fila[clave] = float(valor)
        elif isinstance(valor, (datetime.datetime, datetime.date)):
            fila[clave] = valor.isoformat()
    return fila


def consultar(sql, params=(), uno=False):
    """SELECT: devuelve una lista de diccionarios (o un solo diccionario si uno=True)."""
    with get_db().cursor() as cursor:
        cursor.execute(sql, params)
        if uno:
            return _normalizar(cursor.fetchone())
        return [_normalizar(fila) for fila in cursor.fetchall()]


def ejecutar(sql, params=(), commit=True):
    """INSERT / UPDATE / DELETE: devuelve el id insertado."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        nuevo_id = cursor.lastrowid
        filas = cursor.rowcount
    if commit:
        db.commit()
    return nuevo_id if nuevo_id else filas
