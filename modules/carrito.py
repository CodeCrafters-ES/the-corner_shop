from database.db import get_conn, execute, fetch_one, fetch_all


# Programadora 3 Noemí
# Módulo de Carrito de Compras:
class Carrito:
    # Inicializa un objeto carrito vacio:
    def __init__(self, id, id_usuario, estado = 'activo'):
        self.id = id
        self.id_usuario = id_usuario
        self.estado = estado
        
    @classmethod
    def agregar_al_carrito(cls, id_usuario: int) -> int:
        with get_conn() as conn:
            # 1) buscar/crear carrito activo
            row = conn.execute(
                "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
                (id_usuario,)
            ).fetchone()
            if row:
                carrito_id = row["id"]
            else:
                carrito_id = conn.execute(
                    "INSERT INTO carritos(id_usuario, estado) VALUES (?, 'activo')",
                    (id_usuario,)
                ).lastrowid

            # 2) bucle para añadir artículos
            while True:
                nombre = input("¿Qué artículo deseas añadir? (Enter para cancelar)\n-> ").strip().capitalize()
                if not nombre:
                    print("Operación cancelada.")
                    break

                # 3) buscar producto
                prenda = conn.execute(
                    "SELECT id, nombre, precio, cantidad FROM productos WHERE nombre=? LIMIT 1",
                    (nombre,)
                ).fetchone()
                if not prenda:
                    print("❌ Ese producto no existe en inventario.")
                    continue

                # 4) cantidad ya en carrito y disponible real
                linea = conn.execute(
                    "SELECT cantidad FROM carrito_items WHERE id_carrito=? AND id_producto=?",
                    (carrito_id, prenda["id"])
                ).fetchone()
                en_carrito = linea["cantidad"] if linea else 0
                disponible = prenda["cantidad"] - en_carrito
                if disponible <= 0:
                    print(f"⚠️ Sin stock disponible para '{prenda['nombre']}'. Ya tienes {en_carrito} en el carrito.")
                    continue

                # 5) pedir cantidad válida
                while True:
                    try:
                        s = input(
                            f"Hay {prenda['cantidad']} en almacén (ya tienes {en_carrito} en tu carrito). "
                            f"¿Cuántas quieres añadir? (1..{disponible})\n-> "
                        )
                        qty = int(s)
                        if 1 <= qty <= disponible:
                            break
                    except ValueError:
                        pass
                    print("Cantidad inválida. Intenta de nuevo.")

                # 6) insertar/actualizar línea del carrito (snapshot de precio)
                if linea:
                    conn.execute(
                        "UPDATE carrito_items "
                        "SET cantidad = ?, precio = ? "
                        "WHERE id_carrito=? AND id_producto=?",
                        (en_carrito + qty, prenda["precio"], carrito_id, prenda["id"])
                    )
                else:
                    conn.execute(
                        "INSERT INTO carrito_items(id_carrito, id_producto, cantidad, precio) "
                        "VALUES (?,?,?,?)",
                        (carrito_id, prenda["id"], qty, prenda["precio"])
                    )

                print(f"✅ Añadidas {qty} u. de '{prenda['nombre']}' al carrito #{carrito_id}.")

                # 7) ¿seguir añadiendo?
                again = input("¿Agregar otro artículo? [s/n]\n-> ").strip().lower()
                if again != "s":
                    break

            return carrito_id  



    @classmethod
    def eliminar_del_carrito(cls, id_usuario: int) -> None:
        with get_conn() as conn:
            # 1) Carrito activo
            row = conn.execute(
                "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
                (id_usuario,)
            ).fetchone()
            if not row:
                print("No tienes un carrito activo.")
                return
            carrito_id = row["id"]

            while True:
                # 2) Listar artículos del carrito
                items = conn.execute("""
                    SELECT ci.id, ci.id_producto, ci.cantidad, p.nombre
                    FROM carrito_items ci
                    JOIN productos p ON p.id = ci.id_producto
                    WHERE ci.id_carrito = ?
                    ORDER BY p.nombre
                """, (carrito_id,)).fetchall()

                if not items:
                    print("Tu carrito está vacío.")
                    return

                print("\n🛒 Artículos en tu carrito:")
                for idx, it in enumerate(items, start=1):
                    print(f"{idx}. {it['nombre']} x {it['cantidad']}")

                sel = input("Elige Nº para eliminar (0 cancelar) o escribe el nombre: ").strip()
                if sel in ("", "0"):
                    print("Cancelado.")
                    return

                # 3) Resolver selección por índice o por nombre
                elegido = None
                if sel.isdigit():
                    k = int(sel)
                    if 1 <= k <= len(items):
                        elegido = items[k-1]
                if not elegido:
                    elegido = next((it for it in items if it["nombre"].lower() == sel.lower()), None)

                if not elegido:
                    print("No encontrado. Intenta de nuevo.")
                    continue

                # 4) Pedir cantidad a quitar
                cant_actual = elegido["cantidad"]
                while True:
                    s2 = input(f"¿Cuántas unidades de '{elegido['nombre']}' quieres quitar? (1..{cant_actual}, 0 cancelar): ").strip()
                    if s2 in ("", "0"):
                        print("Cancelado.")
                        return
                    try:
                        q = int(s2)
                    except ValueError:
                        print("Cantidad inválida."); continue
                    if 1 <= q <= cant_actual:
                        break
                    print("Fuera de rango.")

                # 5) Aplicar cambio (borrar línea o reducir cantidad)
                if q == cant_actual:
                    conn.execute("DELETE FROM carrito_items WHERE id=?", (elegido["id"],))
                    print(f"❌ Eliminado '{elegido['nombre']}' del carrito.")
                else:
                    conn.execute(
                        "UPDATE carrito_items SET cantidad = cantidad - ? WHERE id=?",
                        (q, elegido["id"])
                    )
                    print(f"➖ Quitadas {q} u. de '{elegido['nombre']}'. Quedan {cant_actual - q}.")

                # 6) ¿Seguir eliminando?
                again = input("¿Eliminar otro artículo? [s/n]\n-> ").strip().lower()
                if again != "s":
                    break

    # --- Mostrar carrito ---
    @classmethod
    def ver_carrito(cls, id_usuario: int) -> float:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
                (id_usuario,)
            ).fetchone()
            if not row:
                print("No tienes un carrito activo.")
                return 0.0

            carrito_id = row["id"]
            filas = conn.execute("""
                SELECT p.nombre, ci.cantidad, ci.precio,
                       (ci.cantidad * ci.precio) AS subtotal
                FROM carrito_items ci
                JOIN productos p ON p.id = ci.id_producto
                WHERE ci.id_carrito = ?
                ORDER BY p.nombre
            """, (carrito_id,)).fetchall()

            if not filas:
                print("Tu carrito está vacío.")
                return 0.0

            total = 0.0
            print(f"\n🛒 Carrito #{carrito_id}")
            for r in filas:
                sub = r["subtotal"]
                total += sub
                print(f"- {r['nombre']}: {r['cantidad']} x {r['precio']:.2f} = {sub:.2f}")
            print(f"TOTAL: {total:.2f} €")
            return total

    # --- Vaciar carrito ---
    @classmethod
    def vaciar_carrito(cls, id_usuario: int) -> None:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
                (id_usuario,)
            ).fetchone()
            if not row:
                print("No tienes un carrito activo.")
                return

            carrito_id = row["id"]
            c = conn.execute(
                "SELECT COUNT(*) AS c FROM carrito_items WHERE id_carrito=?",
                (carrito_id,)
            ).fetchone()["c"]

            if c == 0:
                print("Tu carrito ya está vacío.")
                return

            ans = input(f"¿Vaciar completamente el carrito #{carrito_id}? [s/n]\n-> ").strip().lower()
            if ans == "s":
                conn.execute("DELETE FROM carrito_items WHERE id_carrito=?", (carrito_id,))
                print("🧹 Carrito vaciado.")
            else:
                print("Operación cancelada.")

