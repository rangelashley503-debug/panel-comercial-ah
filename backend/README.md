# Backend Impulso Mexa (Python + Flask + MySQL)

## Instalación (una sola vez)

1. Instala Python 3.10 o superior y MySQL Server (o XAMPP/MariaDB).
2. Copia esta carpeta `backend` dentro de `panel-comercial-ah`, junto a `index.html`.
3. Abre una terminal en `backend` y crea un entorno virtual:

       python -m venv venv
       venv\Scripts\activate          (Windows)
       source venv/bin/activate       (Mac / Linux)
       pip install -r requirements.txt

4. Indica tus datos de MySQL en `config.py` (usuario y contraseña) o con variables de entorno:
   `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`.
5. Crea la base de datos con datos de prueba (borra las tablas si ya existían):

       python init_db.py

## Ejecutar

    python app.py

Abre http://127.0.0.1:5000/index.html. Las páginas se abren desde el servidor, no con doble clic.

## Usuarios de prueba (cámbialos)

| Rol | Correo | Contraseña |
|---|---|---|
| Administrador | admin@impulsomexa.com | Admin2026 |
| Vendedor | vendedor@impulsomexa.com | Vende2026 |
| Almacén | almacen@impulsomexa.com | Almacen2026 |
| Cliente | cliente@impulsomexa.com | Cliente2026 |

## API

| Método y ruta | Roles | Qué hace |
|---|---|---|
| POST /api/login, /api/logout, /api/registro | público | Sesión y registro comercial |
| GET /api/sesion | con sesión | Usuario actual |
| GET, POST /api/clientes | Admin, Vendedor | Directorio y alta (GET acepta ?q=) |
| PATCH /api/clientes/:id/estatus | Admin | Activo / Suspendido |
| GET /api/productos | con sesión | Catálogo |
| GET /api/productos/stock-minimo | Admin, Vendedor, Almacén | Productos bajo el mínimo |
| GET /api/pedidos, /api/pedidos/resumen | Admin, Vendedor, Almacén | Lista y tarjetas por estatus |
| POST /api/pedidos/cotizar, POST /api/pedidos | Admin, Vendedor | Cotizar sin guardar / registrar |
| PATCH /api/pedidos/:id/estatus | Admin, Vendedor, Almacén | Avanzar de etapa |
| GET /api/pedidos/:id/surtido | Admin, Almacén | Hoja de surtido |
| PATCH /api/pedidos/:id/listo | Admin, Almacén | Descuenta inventario y marca Listo / En ruta |
| POST /api/pagos | Admin, Vendedor | Registrar pago |
| GET /api/corte, POST /api/turno/cerrar | Admin, Vendedor | Corte de caja y cierre de turno |
| GET /api/reportes/mas-vendidos | Admin, Vendedor | Ranking (acepta ?categoria=) |

## Seguridad incluida

- Contraseñas cifradas (hash de Werkzeug), nunca en texto plano.
- Consultas con parámetros (`%s`), sin concatenar datos del usuario: evita inyección SQL.
- Roles verificados en el servidor en cada ruta.
- Validación de RFC, teléfono, correo, contraseña y cantidades en el servidor.
- Los precios y totales se calculan en el servidor con los precios de la base de datos.
- La carpeta `backend/` no se puede descargar desde el navegador.

## Antes de publicarlo en serio

Usar una clave `SECRET_KEY` larga y secreta, desactivar `debug`, servir con HTTPS, limitar los
intentos de inicio de sesión y no usar el usuario `root` de MySQL.
