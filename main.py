from database.db import init_db, fetch_one
from modules.pagos import procesar_pago, generar_factura
from modules.producto import *
from modules.usuarios import Usuario
from modules.carrito import *
from modules.pagos import procesar_pago, generar_factura

init_db()

def menu_admin(usuario):
    while True:
        break
    

def menu_cliente(usuario):
    while True:
        print("\n👕 Bienvenido al menú de cliente")
        print("1️⃣ Ver catálogo de productos")
        print("2️⃣ Añadir producto al carrito")
        print("3️⃣ Quitar producto del carrito")
        print("4️⃣ Consultar carrito")
        print("5️⃣ Realizar pago") #Listo
        print("6️⃣ Vaciar carrito")
        print("0️⃣ Cerrar sesión")
        
        opcion = input("👉 Elige una opción: ")
        
        match (opcion):
            case "1":
                print("\n🛍️ Productos disponibles:")
                productos = obtener_productos()
                for p in productos:
                    print(f" - {p}")
            case "2":
                user_id = usuario["id"] #id para crear carrito
                print(user_id)
                nombre = input("🔎 Nombre del producto que deseas añadir: ")
                cantidad = int(input("📦 ¿Cuántas unidades?: "))
                agregar_al_carrito(nombre, cantidad)
                print(f"✅ {cantidad} unidad(es) de '{nombre}' añadidas al carrito.")
            case "3":
                nombre = input("🗑️ Nombre del producto que deseas quitar: ")
                eliminar_del_carrito(nombre)
                print(f"❌ '{nombre}' eliminado del carrito.")
            case "4":
                print("\n🛒 Tu carrito contiene:")
                ver_carrito()
                
            case "5":
                nombre = usuario["nombre"]
                row = fetch_one("SELECT id FROM usuarios WHERE nombre = ?", (nombre,))
                if not row:
                    raise SystemExit(1)
                
                user_id = row["id"]
                
                try:
                    resultado_pago = procesar_pago(user_id)
                    print("\n=== RESULTADO DEL PAGO ===")
                    print(resultado_pago["ticket"])
                    op = input("¿Quiere generar factura? (y/n)").lower().strip()
                    if op == "y":
                        print(generar_factura(resultado_pago["carrito_id"], resultado_pago["lineas"], resultado_pago["total"]))
                except RuntimeError as e:
                    # p.ej., si el stock cambió entre el chequeo y el descuento
                    print(f"Error de pago: {e}")
                    
            case "6":
                vaciar_carrito()
                print("🧹 Carrito vaciado con éxito.")
            case "0":
                print("👋 Cerrando sesión. ¡Hasta pronto!")
                break
            case _:
                print("❓ Opción no reconocida. Intenta de nuevo.")

def main():
    print("👗 Bienvenido a la Tienda de Ropa Online 👠")
    while True:
        print("\n🔐 Menú principal")
        print("1️⃣ Iniciar sesión") #Listo
        print("2️⃣ Registrarse") #Listo
        print("0️⃣ Salir") #Listo
        
        opcion = input("👉 Elige una opción: ")
        
        match (opcion):
            case "1":
                username = input("👤 Usuario: ").strip().title()
                password = input("🔑 Contraseña: ").strip()
                usuario = Usuario.login(username, password)
                if usuario:
                    print(f"🙌 ¡Hola, {username}! Accediendo a tu perfil...")
                    if Usuario.es_admin_row(usuario):
                        menu_admin(usuario)
                    else:
                        menu_cliente(usuario)
                else:
                    print("❌ Usuario o contraseña incorrectos. Intenta de nuevo.")
            case "2":
                username = input("🆕 Elige un nombre de usuario: ").strip().title()
                password = input("🔐 Elige una contraseña: ").strip()
                res = Usuario.create(username, password)
                print(f"✅ {res["msg"]}" if res["ok"] else f"⚠️ {res["error"]}")
            case "0":
                print("👋 Gracias por visitar nuestra tienda. ¡Hasta la próxima!")
                break
            case _:
                print("❓ Opción no reconocida. Intenta de nuevo.")
            
            
if __name__ == "__main__":
    main()

