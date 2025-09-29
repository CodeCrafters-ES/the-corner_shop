# seed.py
from db import init_db, get_conn
import hashlib

def h(p: str) -> str:
    return hashlib.sha256(p.encode("utf-8")).hexdigest()

def seed_usuarios(conn):
    usuarios = [
        ("admin",  h("admin"),  "admin"),
        ("ana",    h("pass123"), "cliente"),
        ("bruno",  h("pass123"), "cliente"),
        ("carla",  h("pass123"), "cliente"),
    ]
    conn.executemany(
        """
        INSERT INTO usuarios (nombre, password, rol)
        VALUES (?,?,?)
        ON CONFLICT(nombre) DO UPDATE SET
        password = excluded.password,
        rol      = excluded.rol
        """,
        usuarios,
    )

def seed_productos(conn):
    productos = [
        ("Vestido de flores", 19.99, "M", 25),
        ("Camiseta básica",    9.99, "L", 50),
        ("Pantalón chino",    24.90, "32", 30),
        ("Chaqueta vaquera",  39.00, "M", 15),
        ("Sudadera capucha",  29.50, "S", 20),
    ]
    conn.executemany(
        """
        INSERT INTO productos (nombre, precio, talla, cantidad)
        VALUES (?,?,?,?)
        ON CONFLICT(nombre) DO UPDATE SET
        precio   = excluded.precio,
        talla    = excluded.talla,
        cantidad = excluded.cantidad
        """,
        productos,
    )

def seed_carritos(conn):
    # mapa de productos -> id y precio
    prod_rows = conn.execute("SELECT id, nombre, precio FROM productos").fetchall()
    prod_id   = {r["nombre"]: r["id"] for r in prod_rows}
    prod_prec = {r["nombre"]: r["precio"] for r in prod_rows}

    clientes = conn.execute("SELECT id, nombre FROM usuarios WHERE rol='cliente'").fetchall()
    for u in clientes:
        # asegurar un carrito activo (tu índice único lo garantiza)
        row = conn.execute(
            "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
            (u["id"],),
        ).fetchone()
        if row:
            carrito_id = row["id"]
        else:
            carrito_id = conn.execute(
                "INSERT INTO carritos (id_usuario, estado) VALUES (?, 'activo')",
                (u["id"],),
            ).lastrowid

        # ítems de ejemplo (cantidades pequeñas para no agotar stock)
        items = [
            ("Camiseta básica", 2),
            ("Pantalón chino",  1),
        ]
        for nombre, qty in items:
            pid = prod_id[nombre]
            precio = prod_prec[nombre]  # snapshot de precio
            conn.execute(
                """
                INSERT INTO carrito_items (id_carrito, id_producto, cantidad, precio)
                VALUES (?,?,?,?)
                ON CONFLICT(id_carrito, id_producto) DO UPDATE SET
                cantidad = excluded.cantidad,
                precio   = excluded.precio
                """,
                (carrito_id, pid, qty, precio),
            )

def resumen(conn):
    c_usuarios  = conn.execute("SELECT COUNT(*) AS c FROM usuarios").fetchone()["c"]
    c_productos = conn.execute("SELECT COUNT(*) AS c FROM productos").fetchone()["c"]
    c_carritos  = conn.execute("SELECT COUNT(*) AS c FROM carritos").fetchone()["c"]
    c_items     = conn.execute("SELECT COUNT(*) AS c FROM carrito_items").fetchone()["c"]
    print(f"Usuarios: {c_usuarios} | Productos: {c_productos} | Carritos: {c_carritos} | Items: {c_items}")

def reset_datos(conn):
    """Opcional: limpia tablas en orden FK (no borra el esquema)."""
    conn.execute("DELETE FROM carrito_items")
    conn.execute("DELETE FROM carritos")
    conn.execute("DELETE FROM usuarios")
    conn.execute("DELETE FROM productos")

if __name__ == "__main__":
    init_db()  # asegura tablas
    with get_conn() as conn:
        # reset_datos(conn)  # descomenta si quieres limpiar antes
        seed_usuarios(conn)
        seed_productos(conn)
        seed_carritos(conn)
        resumen(conn)
    print("Seed completado.")
