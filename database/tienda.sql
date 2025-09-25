PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS productos(
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE,
  precio REAL NOT NULL,
  talla TEXT NOT NULL,
  cantidad INTEGER NOT NULL DEFAULT 1,
  check(cantidad > 0 AND precio >= 0)
);

CREATE TABLE IF NOT EXISTS usuarios(
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  rol TEXT NOT NULL DEFAULT 'cliente',
  check(rol IN('cliente', 'admin'))
);

CREATE TABLE IF NOT EXISTS carritos(
  id INTEGER PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
  estado TEXT NOT NULL DEFAULT 'activo',
  check(estado IN('activo', 'enviado'))
);
CREATE UNIQUE INDEX IF NOT EXISTS u_carritos_usuario_activo ON carritos(id_usuario) WHERE estado='activo';

CREATE TABLE IF NOT EXISTS carrito_items(
  id INTEGER PRIMARY KEY,
  id_carrito INTEGER NOT NULL REFERENCES carritos(id) ON DELETE CASCADE,
  id_producto INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
  cantidad INTEGER NOT NULL,
  precio REAL NOT NULL,
  check(cantidad > 0 AND precio >= 0),
  unique(id_carrito, id_producto)
);
CREATE INDEX IF NOT EXISTS idx_carritos_id_usuario ON carritos(id_usuario);
CREATE INDEX IF NOT EXISTS idx_carritos_id_producto ON carrito_items(id_producto);