from db import init_db, fetch_one
from modules.pagos import procesar_pago, generar_factura

if __name__ == "__main__":
    # 1) Asegura el esquema (una vez al arrancar) Debe ir al inicio del Main.py
    init_db()

    # 2) Elige el usuario (por nombre) y consigue su id
    nombre = input("Nombre del cliente:")
    row = fetch_one("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
    if not row:
        print(f"No existe el usuario '{nombre}'. Crea/seed primero.")
        raise SystemExit(1)

    user_id = row["id"]

    # 3) Ejecuta el pago y muestra el resultado
    try:
        resultado_pago = procesar_pago(user_id)
        print("\n=== RESULTADO DEL PAGO ===")
        print(resultado_pago["ticket"])
        op = input("¿Quiere generar factura? (y/n)")
        if op == "y":
            print(generar_factura(resultado_pago["carrito_id"], resultado_pago["lineas"], resultado_pago["total"]))
            
        
    except RuntimeError as e:
        # p.ej., si el stock cambió entre el chequeo y el descuento
        print(f"Error de pago: {e}")