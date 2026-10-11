# Interfaz web

Interfaz web para una comercializadora y distribuidora mayorista de dulces y bebidas energizantes.

Proyecto de la materia **Infraestructura de Aplicaciones Web**.

- **Universidad:** Universidad tecnologica del norte de Guanajuato
- **Profesor:** Eric Domenzain Morales
- **Fecha de entrega:** Sin aclarar

## Integrantes
- Ashley Hermione Dominguez Rangel
- Katerinne Kreishell Irusta Torres

| Integrante | Módulo |
|---|---|
| [Hermione] | Administración y supervisión |
| [Hermione] | Catálogo de productos |
| [Hermione] | Inventario y existencias |
| [Hermione] | Ventas de mostrador |
| [Hermione - Kreishell] | Autenticación y usuarios |
| [Kreishell] | Clientes y cuentas comerciales |
| [Kreishell] | Gestión de pedidos y cotizaciones |
| [Kreishell] | Pagos, reportes y panel |
| [Kreishell] | Surtido de almacén y logística |

## Contexto del negocio

La empresa vende al mayoreo dos tipos de productos:

- **Confitería:** paletas, chocolates y gomitas.
- **Bebidas:** energizantes e isotónicas (Monster, Red Bull, Electrolit, entre otras).

Las ventas se manejan en tres escalas: **Pieza**, **Caja** y **Tarima / Mayoreo**.

Los pedidos pasan por cuatro estatus: **Registrado**, **En preparación**, **Listo / En ruta** y **Entregado**.

## Módulos

1. **Administración y supervisión** (`admi.html`):
2. **Catalogo de productos** (`catalogo.html`):
3. **Inventario y existencias** (`inventario.html`):
4. **Ventas de mostrador** (`ventas_mostrador`):
5. **Autenticación y usuarios** (`Inicio de sesión.html`): inicio de sesión con selector de rol (Vendedor, Almacén, Administrador, Cliente) y registro comercial con datos fiscales.
6. **Gestión de pedidos y cotizaciones** (`Gestión.html`): resumen por estatus, tabla de pedidos y formulario para cotizar o registrar un pedido. Calcula el total según producto, escala y cantidad.
7. **Surtido de almacén y logística** (`Surtido.html`): cola de pedidos para bodega y hoja de surtido con lote, caducidad y verificación de anaquel. El botón "Marcar como listo para ruta" se habilita al verificar todos los productos.
8. **Clientes y cuentas comerciales** (`Clientes.html`): directorio de clientes mayoristas con buscador, cambio de estatus (Activo / Suspendido) y formulario de alta con dirección de entrega.
9. **Pagos, reportes y panel administrativo** (`Pagos.html`): corte de turno, corte de caja por método de pago (efectivo, tarjeta, transferencia), alertas de stock mínimo y reporte de productos más vendidos con filtro por categoría.

## Tecnologías

- HTML5
- [Tailwind CSS](https://tailwindcss.com/) mediante CDN
- JavaScript (sin frameworks ni librerías externas)
- `Paletadecolores.js`: archivo con la paleta de colores del proyecto

No requiere npm ni instalación de dependencias.

## Cómo abrir el proyecto

1. Descarga o clona la carpeta completa `panel-comercial-ah`.
2. Abre `Inicio de sesión.html` en el navegador (doble clic o clic derecho > Abrir con).
3. Navega entre módulos con el menú superior.

> Se necesita conexión a internet, ya que Tailwind CSS se carga desde su CDN.

## Estructura de archivos

```
panel-comercial-ah/
├── Administración y supervisión-H/
│   └── admi.html
├── Autenticación y usuarios/
│   └── Inicio de sesión.html
├── Catalogo de productos- H/
│   └── catalogo.html
├── Clientes y cuentas comerciales - K/
│   └── Clientes.html
├── Gestión de pedidos y cotizaciones - K/
│   └── Gestión.html
├── Inventario y existencias-H/
│   └── inventario.html
├── Pagos, reportes y panel - K/
│   └── Pagos.html
├── Surtido de almacén y logística - K/
│   └── Surtido.html
├── Ventas de mostrador-H/
│   └── ventas_mostrador.html
├── index.html
├── Paletadecolores.js
└── Readme.md
```

## Alcance y limitaciones

Este proyecto es la **maqueta del frontend**:

- Los datos (clientes, pedidos, precios, lotes, montos) son de ejemplo.
- No hay servidor ni base de datos, por lo que los cambios hechos en pantalla (pedidos nuevos, pagos, clientes) se pierden al recargar la página.
- Las validaciones del navegador mejoran la experiencia de uso, pero **no sustituyen la validación en el servidor**. La autenticación real (usuarios, contraseñas, roles y sesiones) debe implementarse en el backend.

## Posibles mejoras

- Conectar los formularios a una API y una base de datos.
- Autenticación y control de acceso por rol en el servidor.
- Generación de cotizaciones en PDF.
- Reportes con rango de fechas.
