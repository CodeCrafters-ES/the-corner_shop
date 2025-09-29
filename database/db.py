import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "tienda.db"
SCHEMA_PATH = PROJECT_ROOT / "database" / "tienda.sql"
DB_PATH.parent.mkdir(parents=True, exist_ok=True) 

#Conectar a base datos, importar a los modelos
def get_conn():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  conn.execute("PRAGMA foreign_keys = ON;")
  return conn

#importar desde main.py
def init_db():
  assert SCHEMA_PATH.exists(), f"No se encontró el esquema: {SCHEMA_PATH}"
  with get_conn() as conn:
    exists = conn.execute(
      "SELECT 1 FROM sqlite_master WHERE type='table' AND name='productos'"      
    ).fetchone()
    if not exists:
      #Crear tablas por primera vez
      sql = SCHEMA_PATH.read_text(encoding='utf-8')
      conn.executescript(sql)
      
##HELPERS
      
#execute(sql, params=()) → INSERT/UPDATE/DELETE (devuelve lastrowid)
def execute(sql: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.lastrowid
#Ejemplo de execute() donde devuelve el id nuevo
# pid = execute("INSERT INTO productos(nombre, precio, talla, cantidad) VALUES (?,?,?,?)",
#               ("vestido de flores", 19.99, "M", 20))
# print("nuevo producto id:", pid)


#fetch_one(sql, params=()) → una fila (sqlite3.Row o None)
def fetch_one(sql: str, params: tuple = ()):
    with get_conn() as conn:
        return conn.execute(sql, params).fetchone()
#Ejemplo de fetch_one()
# u = fetch_one("SELECT id, nombre, rol FROM usuarios WHERE nombre = ?", ("admin",))
# print(dict(u) if u else "No existe")

#fetch_all(sql, params=()) → lista de filas (sqlite3.Row)
def fetch_all(sql: str, params: tuple = ()):
    with get_conn() as conn:
        return conn.execute(sql, params).fetchall()
#Ejemplo de cómo usar fetch_all()
# rows = fetch_all("SELECT id, nombre, precio, talla, cantidad FROM productos ORDER BY id")
# productos = [dict(r) for r in rows]
# print(productos)
# def create(cls, nombre: str, password: str, rol: str = "cliente") -> "Usuario":
#   new_id = execute(
#             "INSERT INTO usuarios(nombre, password, rol) VALUES (?,?,?)",
#              (nombre, password, rol)
#             )

if __name__ == "__main__":
    init_db()
    tablas = [r["name"] for r in fetch_all("SELECT name FROM sqlite_master WHERE type='table'")]
    print("Tablas:", tablas)
    
    
    # PRUEBA DE USUARIOS EN DDBB
    # id = execute("INSERT INTO usuarios(nombre,password,rol) VALUES('administrador','pass123','admin')")
    # Esteve = execute("INSERT INTO usuarios(nombre,password) VALUES('Esteve','pass123')")
    # Rossana = execute("INSERT INTO usuarios(nombre,password) VALUES('Rossana','pass123')")
    # Noemie = execute("INSERT INTO usuarios(nombre,password) VALUES('Noemie','pass123')")
    # Alejandro = execute("INSERT INTO usuarios(nombre,password) VALUES('Alejandro','pass123')")
    # clientes=fetch_all("SELECT id, nombre, rol, password FROM usuarios WHERE rol = 'cliente'")
    # for cliente in clientes:
    #   print(dict(cliente))