from database.db import init_db, fetch_one
from modules.pagos import procesar_pago, generar_factura
from productos import *
from usuarios import *
from carrito import *
from pagos import *

def menu_cliente(usuario):
    while True:
        print("\n👕 Bienvenido al menú de cliente")
        print("1️⃣ Ver catálogo de productos")
        print("2️⃣ Añadir producto al carrito")
        print("3️⃣ Quitar producto del carrito")
        print("4️⃣ Consultar carrito")
        print("5️⃣ Realizar pago")
        print("6️⃣ Vaciar carrito")
        print("0️⃣ Cerrar sesión")
        opcion = input("👉 Elige una opción: ")
        if opcion == "1":
            print("\n🛍️ Productos disponibles:")
            productos = obtener_productos()
            for p in productos:
                print(f" - {p}")
        elif opcion == "2":
            nombre = input("🔎 Nombre del producto que deseas añadir: ")
            cantidad = int(input("📦 ¿Cuántas unidades?: "))
            agregar_al_carrito(nombre, cantidad)
            print(f"✅ {cantidad} unidad(es) de '{nombre}' añadidas al carrito.")
        elif opcion == "3":
            nombre = input("🗑️ Nombre del producto que deseas quitar: ")
            eliminar_del_carrito(nombre)
            print(f"❌ '{nombre}' eliminado del carrito.")
        elif opcion == "4":
            print("\n🛒 Tu carrito contiene:")
            ver_carrito()
        elif opcion == "5":
            total = calcular_total()
            print(f"\n💳 Total a pagar: {total:.2f} €")
            if procesar_pago("carrito"):
                generar_factura("carrito", total)
                vaciar_carrito()
                print("🎉 ¡Pago exitoso! Tu factura ha sido generada.")
            else:
                print("⚠️ No se pudo procesar el pago. Intenta nuevamente.")
        elif opcion == "6":
            vaciar_carrito()
            print("🧹 Carrito vaciado con éxito.")
        elif opcion == "0":
            print("👋 Cerrando sesión. ¡Hasta pronto!")
            break
        else:
            print("❓ Opción no reconocida. Intenta de nuevo.")

def main():
    print("👗 Bienvenido a la Tienda de Ropa Online 👠")
    while True:
        print("\n🔐 Menú principal")
        print("1️⃣ Iniciar sesión")
        print("2️⃣ Registrarse")
        print("0️⃣ Salir")
        opcion = input("👉 Elige una opción: ")
        if opcion == "1":
            username = input("👤 Usuario: ")
            password = input("🔑 Contraseña: ")
            usuario = iniciar_sesion(username, password)
            if usuario:
                print(f"🙌 ¡Hola {username}! Accediendo a tu perfil...")
                if es_admin(usuario):
                    menu_admin(usuario)
                else:
                    menu_cliente(usuario)
            else:
                print("❌ Usuario o contraseña incorrectos. Intenta de nuevo.")
        elif opcion == "2":
            username = input("🆕 Elige un nombre de usuario: ")
            password = input("🔐 Elige una contraseña: ")
            registrar_usuario(username, password)
            print(f"✅ Usuario '{username}' registrado con éxito. ¡Ya puedes iniciar sesión!")
        elif opcion == "0":
            print("👋 Gracias por visitar nuestra tienda. ¡Hasta la próxima!")
            break
        else:
            print("❓ Opción no reconocida. Intenta de nuevo.")
            
            


if __name__ == "__main__":
    # 1) Asegura el esquema (una vez al arrancar) Debe ir al inicio del Main.py
    init_db()



    #ejemplo de ejecución de módulo de pago y generar factura
    # Elige el usuario (por nombre) y consigue su id
    nombre = input("Nombre del cliente:")
    row = fetch_one("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
    if not row:
        print(f"No existe el usuario '{nombre}'. Crea/seed primero.")
        raise SystemExit(1)

    user_id = row["id"]

    # Ejecuta el pago y muestra el resultado, luego pide al usuario si generar factura
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
            
            
            

if __name__ == "__main__":
    main()

