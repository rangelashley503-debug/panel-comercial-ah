-- Base de datos del proyecto Impulso Mexa
CREATE DATABASE IF NOT EXISTS impulso_mexa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE impulso_mexa;

-- Se borran en orden inverso por las llaves foráneas (solo para reiniciar en desarrollo)
DROP TABLE IF EXISTS pagos;
DROP TABLE IF EXISTS turnos;
DROP TABLE IF EXISTS detalle_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS productos;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tienda VARCHAR(120) NOT NULL,
    rfc VARCHAR(13) NOT NULL UNIQUE,
    contacto VARCHAR(100),
    telefono VARCHAR(10),
    direccion VARCHAR(200),
    ciudad VARCHAR(80),
    cp VARCHAR(5),
    referencias VARCHAR(200),
    estatus ENUM('Activo', 'Suspendido') NOT NULL DEFAULT 'Activo',
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('Vendedor', 'Almacén', 'Administrador', 'Cliente') NOT NULL,
    cliente_id INT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    categoria ENUM('Energizantes', 'Isotónicas', 'Confitería') NOT NULL,
    precio_pieza DECIMAL(10,2) NOT NULL,
    piezas_por_caja INT NOT NULL DEFAULT 24,
    cajas_por_tarima INT NOT NULL DEFAULT 40,
    existencia_cajas INT NOT NULL DEFAULT 0,
    stock_minimo_cajas INT NOT NULL DEFAULT 0,
    lote VARCHAR(30),
    caducidad DATE
);

CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    folio VARCHAR(20) UNIQUE,
    cliente_id INT NOT NULL,
    volumen ENUM('Pieza', 'Caja', 'Tarima') NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    estatus ENUM('Registrado', 'En preparación', 'Listo / En ruta', 'Entregado') NOT NULL DEFAULT 'Registrado',
    fecha_entrega DATE,
    observaciones TEXT,
    creado_por INT NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (creado_por) REFERENCES usuarios(id)
);

CREATE TABLE detalle_pedido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    escala ENUM('Pieza', 'Caja', 'Tarima') NOT NULL,
    cantidad INT NOT NULL,
    piezas INT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    abierto_por INT NOT NULL,
    abierto_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cerrado_en TIMESTAMP NULL,
    estatus ENUM('Abierto', 'Cerrado') NOT NULL DEFAULT 'Abierto',
    FOREIGN KEY (abierto_por) REFERENCES usuarios(id)
);

CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    turno_id INT NOT NULL,
    pedido_id INT NULL,
    metodo ENUM('Efectivo', 'Tarjeta', 'Transferencia') NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (turno_id) REFERENCES turnos(id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
