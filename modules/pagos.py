from database.db import get_conn, execute, fetch_one, fetch_all
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORT_PATH = PROJECT_ROOT / "data" / "facturas"
EXPORT_PATH.mkdir(parents=True, exist_ok=True)

def procesar_pago(id_usuario: int) -> dict:
    with get_conn() as conn:
        # 1) carrito activo
        row = conn.execute(
            "SELECT id FROM carritos WHERE id_usuario=? AND estado='activo' LIMIT 1",
            (id_usuario,)
        ).fetchone()
        if not row:
            return {"ok": False, "error": "No tienes un carrito activo."}
        carrito_id = row["id"]

        # 2) líneas + stock + nombre
        items = conn.execute("""
            SELECT
                ci.id_producto,
                ci.cantidad  AS cant,
                ci.precio    AS precio,
                p.cantidad   AS stock,
                p.nombre     AS nombre
            FROM carrito_items ci
            JOIN productos p ON p.id = ci.id_producto
            WHERE ci.id_carrito = ?
        """, (carrito_id,)).fetchall()
        if not items:
            return {"ok": False, "error": "El carrito está vacío."}

        # 3) validar disponibilidad
        insuf = [r for r in items if r["stock"] < r["cant"]]
        if insuf:
            detalle = "\n".join(
                f"- {r['nombre']}: pedido {r['cant']}, disponible {r['stock']}"
                for r in insuf
            )
            return {"ok": False, "error": f"Stock insuficiente:\n{detalle}"}

        # 4) descontar stock (a prueba de carreras)
        for r in items:
            updated = conn.execute(
                "UPDATE productos SET cantidad = cantidad - ? "
                "WHERE id = ? AND cantidad >= ?",
                (r["cant"], r["id_producto"], r["cant"])   # <-- usa 'cant'
            ).rowcount
            if updated != 1:
                raise RuntimeError(f"El stock de '{r['nombre']}' cambió; intenta de nuevo.")

        # 5) cerrar carrito
        conn.execute("UPDATE carritos SET estado='enviado' WHERE id=?", (carrito_id,))

        # 6) calcular total y armar ticket
        lineas = []
        total = 0.0
        for r in items:
            sub = r["cant"] * r["precio"]
            total += sub
            lineas.append(f"{r['nombre']}: {r['cant']} x {r['precio']:.2f} = {sub:.2f}")
        return {
        "ok": True,
        "carrito_id": carrito_id,
        "lineas": lineas,
        "total": total,
        "ticket": f"Nº carrito: {carrito_id}\n" + "\n".join(lineas) + f"\nTOTAL: {total:.2f} €"
        }
        

    # # 2) Elige el usuario (por nombre) y consigue su id
    # nombre = "ana"  # o pídeselo por input()
    # row = fetch_one("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
    # if not row:
    #     print(f"No existe el usuario '{nombre}'. Crea/seed primero.")
    #     raise SystemExit(1)

    # user_id = row["id"]

    # # 3) Ejecuta el pago y muestra el resultado
    # try:
    #     ticket = procesar_pago(user_id)
    #     print("\n=== RESULTADO DEL PAGO ===")
    #     print(ticket)
    # except RuntimeError as e:
    #     # p.ej., si el stock cambió entre el chequeo y el descuento
    #     print(f"Error de pago: {e}")
    
def generar_factura(carrito_id: int, lineas: list[str], total: float) -> str:
    # (opcional) comprobar que el carrito está enviado
    row = fetch_one("SELECT estado FROM carritos WHERE id=?", (carrito_id,))
    if not row:
        raise ValueError("Carrito inexistente.")
    if row["estado"] != "enviado":
        raise ValueError("El carrito debe estar 'enviado' antes de facturar.")

    file_path = EXPORT_PATH / f"factura_{carrito_id:06d}.txt"
    contenido = []
    contenido.append(f"FACTURA — Carrito {carrito_id:06d}")
    contenido.append("")  # línea en blanco
    contenido.extend(lineas)
    contenido.append(f"\nTOTAL: {total:.2f} €")

    file_path.write_text("\n".join(contenido), encoding="utf-8")
    return f"Su factura se ha guardado en {file_path}. Gracias por su compra."

