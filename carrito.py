#!/usr/bin/env python


# Programadora 3 Noemí
# Módulo de Carrito de Compras:
class Carrito:
    # Inicializa un objeto carrito vacio:
    def __init__(self):
        # Inicializa un diccionario vacio:
        self.productos = {}

    def agregar_al_carrito(self, producto, cantidad):
        """
        Añade un producto al carrito.
        Argumentos:
            - producto (dict): Diccionario cuya llave es el nombre del
            producto y cuyo valor es un diccionario de detalles
            del producto (nombre, precio, talla).

            - cantidad (int): Cantidad del producto a agregar.
        """
        if producto["nombre"] in self.productos:
            self.productos[producto["nombre"]]["cantidad"] += int(cantidad)
        else:
            # print("El producto no está disponible")

            # En lugar del mensaje de error, he implementado esta
            # opción de momento para mis tests:
            self.productos[producto["nombre"]] = {
                "precio": producto["precio"],
                "talla": producto["talla"],
                "cantidad": cantidad,
            }

    # Quita un producto del carrito:
    def eliminar_del_carrito(self, producto):
        if producto["nombre"] in self.productos:
            del self.productos[producto["nombre"]]

    # Suma el precio de todos los productos del carrito:
    def calcular_total(self):
        total = 0
        for detalles in self.productos.values():
            total += detalles["precio"] * detalles["cantidad"]
        return total

    # Muestra los productos en el carrito:
    def ver_carrito(self):
        print("Productos en el carrito:")
        for producto, values in self.productos.items():
            print(
                f"""
        ----------------------------------------
        {producto} (talla {values['talla']}): {values['precio']}€ x {values['cantidad']} = {values['precio']*values['cantidad']}€""",
                end="",
            )
        print(
            f"""
        ========================================
        TOTAL: {self.calcular_total()}€
        ========================================""",
            end="\n\n",
        )

    # Resetea el carrito:
    def vaciar_carrito(self):
        self.productos = {}


# He usado esta funcion main() para hacer mis tests:
def main():
    su_carrito = Carrito()
    producto1 = {"nombre": "Camisa", "precio": 20, "talla": "L"}
    producto2 = {"nombre": "Pantalones", "precio": 30, "talla": "M"}
    producto3 = {"nombre": "Chanclas", "precio": 10, "talla": "s"}
    su_carrito.agregar_al_carrito(producto1, 2)
    su_carrito.agregar_al_carrito(producto2, 1)
    su_carrito.agregar_al_carrito(producto3, 4)
    su_carrito.ver_carrito()
    su_carrito.vaciar_carrito()
    su_carrito.ver_carrito()


if __name__ == "__main__":
    main()
