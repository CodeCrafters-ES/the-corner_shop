import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent

DB_PATH = PROJECT_ROOT / "data" / "tienda.db"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "tienda.sql"

DB_PATH.parent.mkdir(parents=True, exist_ok=True) 

#Conectar
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
conn.row_factory = sqlite3.Row
print('Connected to', DB_PATH)

#Crear tablas por primera vez
sql = SCHEMA_PATH.read_text(encoding='utf-8')
conn.executescript(sql)

#crear cursor
cur = conn.cursor()

rows = cur.execute(
  "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
).fetchall()

tables =[r[0] for r in rows]

print(tables)

# ingresar datos tabla
conn.execute(
  "INSERT INTO productos(nombre, precio, talla, cantidad) VALUES (?,?,?,?) ON CONFLICT(nombre) DO UPDATE SET precio=excluded.precio, talla=excluded.talla, cantidad=excluded.cantidad",
  ('vestido de flores', 19.99, 'M', 20)
)

conn.execute(
  "INSERT INTO usuarios(nombre, password, rol) VALUES(?,?,?) ON CONFLICT(nombre) DO UPDATE SET password=excluded.password, rol=excluded.rol",
  ('admin', 'admin', 'admin')
)

conn.commit()

rows = conn.execute(
  "SELECT * FROM productos"
).fetchall()

admin_rows = conn.execute(
  "SELECT id, nombre, password, rol FROM usuarios"
).fetchall()

print([dict(r) for r in rows])
print(f"Info de usuario: {[dict(r) for r in admin_rows]}")


conn.close()