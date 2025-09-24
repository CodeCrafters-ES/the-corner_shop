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
    main()