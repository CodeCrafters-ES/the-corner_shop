from database.db import init_db
from modules.pagos import procesar_pago, generar_factura
from repositories.producto_repository import ProductoRepository
from modules.producto import Producto
from modules.usuarios import Usuario
from modules.carrito import Carrito
from modules.utils.inputs import input_int, input_float

repo_producto = ProductoRepository()
init_db()

def menu_admin(usuario):
    nombre_admin = usuario["nombre"]
    while True:
        print(f"\n🛠️  Menú admin ({nombre_admin})")
        print("1️⃣  Listar productos")
        print("2️⃣  Añadir producto")
        print("3️⃣  Actualizar stock (valor exacto)")
        print("4️⃣  Actualizar precio")
        print("5️⃣  Eliminar producto")
        print("0️⃣  Salir")

        op = input("👉 Opción: ").strip()

        match op:
            case "1":
                print("\n🛍️ Productos disponibles:")
                productos = repo_producto.obtener_todos_productos()
                if not productos:
                    print("📦 No hay productos.")
                for p in productos:
                    print(f"- [{p.id_producto}] {p.nombre} · talla {p.talla} · {p.cantidad} uds · {p.precio:.2f} €")
            case "2":
                nombre = input("Nombre: ").strip().title()
                talla  = input("Talla: ").strip().upper()
                precio = input_float("Precio (€): ", minv=0.0)
                cant   = input_int("Cantidad: ", minv=0)

                prod = Producto(id_producto=0, nombre=nombre, precio=precio, talla=talla, cantidad=cant)
                nuevo_id = repo_producto.crear_producto(prod)
                if nuevo_id:
                    print(f"✅ Creado con id {nuevo_id}")
                else:
                    print("⚠️ No se pudo crear (¿nombre duplicado?).")
            
            case "3":
                pid  = input_int("ID de producto: ", minv=1)
                nuevo = input_int("Nuevo stock: ", minv=0)
                ok = repo_producto.actualizar_stock(pid, nuevo)
                print("✅ Stock actualizado." if ok else "⚠️ No se pudo actualizar.")
                
            case "4":
                pid = input_int("ID de producto: ", minv=1)
                p = repo_producto.obtener_producto_por_id(pid)
                if not p:
                    print("❌ No existe ese producto.")
                else:
                    nuevo = input_float(f"Precio actual {p.precio:.2f} €. Nuevo precio: ", minv=0.0)
                    p.precio = nuevo
                    ok = repo_producto.actualizar_producto(p)
                    print("✅ Precio actualizado." if ok else "⚠️ No se pudo actualizar.")
                    
            case "5":
                pid = input_int("ID de producto a eliminar: ", minv=1)
                conf = input("¿Seguro? (s/N): ").strip().lower()
                if conf == "s":
                    ok = repo_producto.eliminar_producto(pid)
                    print("🗑️  Eliminado." if ok else "⚠️ No se pudo eliminar.")
                else:
                    print("Cancelado.")

            case "0":
                print("👋 Saliendo del menú admin.")
                break
            
            case _:
                print("❓ Opción no reconocida.")
                
    
def menu_cliente(usuario):
    while True:
        print("\n👕 Bienvenido al menú de cliente")
        print("1️⃣ Ver catálogo de productos") #módulo carrito
        print("2️⃣ Añadir producto al carrito") #módulo carrito
        print("3️⃣ Quitar producto del carrito") #módulo carrito
        print("4️⃣ Consultar carrito") #módulo carrito
        print("5️⃣ Realizar pago") #Listo
        print("6️⃣ Vaciar carrito") #módulo carrito
        print("0️⃣ Cerrar sesión")
        
        opcion = input("👉 Elige una opción: ")
        
        match opcion:
            case "1":
                print("\n🛍️ Productos disponibles:")
                productos = repo_producto.obtener_todos_productos()
                if not productos:
                    print("📦 No hay productos.")
                for p in productos:
                    print(f"- [{p.id_producto}] {p.nombre} · talla {p.talla} · {p.cantidad} uds · {p.precio:.2f} €")
            case "2":
                Carrito.agregar_al_carrito(usuario["id"])
            case "3":
                Carrito.eliminar_del_carrito(usuario["id"])
            case "4":
                Carrito.ver_carrito(usuario["id"])                
            case "5":
                user_id = usuario["id"]
                try:
                    resultado = procesar_pago(user_id)
                    if not resultado.get("ok"):
                        print(resultado.get("error", "No se pudo procesar el pago."))
                    else:
                        print("\n=== RESULTADO DEL PAGO ===")
                        print(resultado["ticket"])
                        op = input("¿Quiere generar factura? (s/n)\n-> ").lower().strip()
                        if op == "s":
                            print(generar_factura(
                                resultado["carrito_id"],
                                resultado["lineas"],
                                resultado["total"]
                            ))
                except RuntimeError as e:
                    print(f"Error de pago: {e}")                    
            case "6":
                Carrito.vaciar_carrito(usuario["id"])
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
        
        match opcion:
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
                print(f"✅ {res['msg']}" if res["ok"] else f"⚠️ {res['error']}")
            case "0":
                print("👋 Gracias por visitar nuestra tienda. ¡Hasta la próxima!")
                break
            case _:
                print("❓ Opción no reconocida. Intenta de nuevo.")
            
            
if __name__ == "__main__":
    main()

