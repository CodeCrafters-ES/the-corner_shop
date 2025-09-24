class Producto:
    def __init__(self, nombre, precio, talla, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.talla = talla
        self.cantidad = cantidad
        
        self.productos = []
        
    def agregar_producto(self, p):
        self.productos.append(p)
        
        
        
        