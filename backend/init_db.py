"""Crea la base de datos, las tablas y los datos de prueba.
Ejecutar una sola vez:  python init_db.py   (¡borra las tablas si ya existían!)"""
import os

from werkzeug.security import generate_password_hash

from db import conectar

AQUI = os.path.dirname(os.path.abspath(__file__))

CLIENTES = [
    ('Miscelánea La Esperanza', 'MLE850312AB4', 'María Hernández', '4181002345', 'Calle Hidalgo 12, Col. Centro', 'Dolores Hidalgo', '37800', 'Activo'),
    ('Abarrotes Don Chuy', 'ADC900625KL2', 'Jesús Ramírez', '4181006789', 'Av. Juárez 45, Col. San Juan', 'Dolores Hidalgo', '37800', 'Activo'),
    ('Tienda El Güero', 'TGU780920PQ7', 'Ricardo Torres', '4181004411', 'Calle Morelos 8, Col. Las Flores', 'Dolores Hidalgo', '37800', 'Suspendido'),
    ('Super Mayoreo del Centro', 'SMC010204XY9', 'Laura Martínez', '4181008820', 'Blvd. Principal 300, Zona Industrial', 'Dolores Hidalgo', '37800', 'Activo'),
]

# nombre, categoría, precio por pieza, piezas por caja, cajas por tarima, existencia, mínimo, lote, caducidad
PRODUCTOS = [
    ('Monster Energy 473 ml', 'Energizantes', 38, 24, 40, 120, 30, 'L-2406-A', '2027-03-15'),
    ('Red Bull 250 ml', 'Energizantes', 35, 24, 40, 90, 25, 'L-2407-C', '2027-04-22'),
    ('Electrolit 600 ml', 'Isotónicas', 22, 24, 40, 12, 25, 'L-2405-B', '2027-01-10'),
    ('Panditas (bolsa)', 'Confitería', 4, 24, 40, 9, 20, 'L-2408-D', '2027-06-30'),
    ('Paletas Payaso', 'Confitería', 5, 24, 40, 140, 20, 'L-2406-F', '2027-05-18'),
    ('Chocolate en barra', 'Confitería', 12, 24, 40, 60, 15, 'L-2409-G', '2027-08-01'),
]

# Usuarios de DEMOSTRACIÓN: cambia estas contraseñas antes de usar el sistema de verdad
USUARIOS = [
    ('admin@impulsomexa.com', 'Admin2026', 'Administrador', None),
    ('vendedor@impulsomexa.com', 'Vende2026', 'Vendedor', None),
    ('almacen@impulsomexa.com', 'Almacen2026', 'Almacén', None),
    ('cliente@impulsomexa.com', 'Cliente2026', 'Cliente', 1),
]


def ejecutar_esquema(cursor):
    with open(os.path.join(AQUI, 'schema.sql'), encoding='utf-8') as archivo:
        contenido = archivo.read()
    for sentencia in contenido.split(';'):
        # Se quitan los comentarios; si no queda nada, se omite
        limpia = '\n'.join(l for l in sentencia.splitlines() if not l.strip().startswith('--')).strip()
        if limpia:
            cursor.execute(limpia)


def main():
    conexion = conectar(con_base=False)
    try:
        with conexion.cursor() as cursor:
            ejecutar_esquema(cursor)

            cursor.executemany(
                'INSERT INTO clientes (tienda, rfc, contacto, telefono, direccion, ciudad, cp, estatus) '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', CLIENTES)
            cursor.executemany(
                'INSERT INTO productos (nombre, categoria, precio_pieza, piezas_por_caja, cajas_por_tarima, '
                'existencia_cajas, stock_minimo_cajas, lote, caducidad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                PRODUCTOS)
            cursor.executemany(
                'INSERT INTO usuarios (correo, password_hash, rol, cliente_id) VALUES (%s, %s, %s, %s)',
                [(correo, generate_password_hash(pw), rol, cid) for correo, pw, rol, cid in USUARIOS])
        conexion.commit()
    finally:
        conexion.close()

    print('Base de datos lista. Usuarios de prueba:')
    for correo, pw, rol, _ in USUARIOS:
        print('  %-14s %-28s %s' % (rol, correo, pw))


if __name__ == '__main__':
    main()
