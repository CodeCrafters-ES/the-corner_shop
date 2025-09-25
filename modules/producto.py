import json
import csv

from pathlib import Path

class Producto:
    def __init__(self, id_producto, nombre, precio, talla, cantidad, categoria=""):
        self.__id_producto = id_producto
        self.__nombre = self.__validar_nombre(nombre)
        self.__precio = self.__validar_precio(precio)
        self.__talla = self.__validar_talla(talla)
        self.__cantidad = self.__validar_cantidad(cantidad)
        self.__categoria = categoria if categoria else ""
        
    # Métodos privados de validación
    def __validar_nombre(self, nombre):        
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío")
        return nombre.strip()
    
    def __validar_precio(self, precio):        
        try:
            precio_float = float(precio)
            if precio_float < 0:
                raise ValueError("El precio no puede ser negativo")
            return precio_float
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un número válido")
    
    def __validar_talla(self, talla):        
        if not isinstance(talla, str):
            raise ValueError("La talla debe ser un texto")
        tallas_validas = ["XXS", "XS", "S", "M", "L", "XL", "XXL", "XXXL"]
        talla_upper = talla.upper().strip()
        if talla_upper not in tallas_validas:
            # Permitir tallas numéricas también
            if not talla.strip():
                raise ValueError("La talla no puede estar vacía")
        return talla_upper if talla_upper in tallas_validas else talla.strip()
    
    def __validar_cantidad(self, cantidad):        
        try:
            cantidad_int = int(cantidad)
            if cantidad_int < 0:
                raise ValueError("La cantidad no puede ser negativa")
            return cantidad_int
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un número entero válido")
     
    # Propiedades Getters
    @property # Convertir método en getter
    def id_producto(self):        
        return self.__id_producto
    
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def talla(self):        
        return self.__talla
    
    @property 
    def cantidad(self):       
        return self.__cantidad
    
    @property
    def categoria(self):        
        return self.__categoria    

    # Propiedades Setters
    @nombre.setter # Definir setter de cantidad
    def nombre(self, valor):        
        self.__nombre = self.__validar_nombre(valor)
        
    @precio.setter
    def precio(self, valor):
        self.__precio = self.__validar_precio(valor)
        
    @talla.setter
    def talla(self, valor):        
        self.__talla = self.__validar_talla(valor)
    
    @cantidad.setter
    def cantidad(self, valor):        
        self.__cantidad = self.__validar_cantidad(valor)
        
    # Métodos públicos
    def actualizar_stock(self, nueva_cantidad):        
        self.cantidad = nueva_cantidad
        return True
        
    # Comprobar si hay stock y dar info
    def obtener_estado_stock(self):        
        if self.__cantidad == 0:
            return "SIN STOCK"
        elif self.__cantidad <= 5:
            return "STOCK BAJO"
        else:
            return "EN STOCK"
    
    def obtener_producto(self):
        return {
            'id': self.__id_producto,
            'nombre': self.__nombre,
            'precio': self.__precio,
            'talla': self.__talla,
            'cantidad': self.__cantidad,
            'categoria': self.__categoria,
        }
            
    @staticmethod
    def obtener_productos(productos):        
        if not productos:
            print("⚠️ No hay productos en la lista.")
            return

        print("\n📦 Lista de productos")
        print("-" * 60)
        for p in productos:
            print(p)  # usa __str__ de la clase
        print("-" * 60)
        print(f"Total de productos: {len(productos)}\n")
        
    # Métodos estáticos para persistencia    
    @staticmethod
    def guardar_json(productos, archivo = Path("json/productos.json")):
        archivo = Path(archivo)  # convertir a Path
        archivo.parent.mkdir(parents=True, exist_ok=True)  # crea carpeta si no existe
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([p.obtener_producto() for p in productos], f, indent=4, ensure_ascii=False)
   
    @staticmethod
    def guardar_csv(productos, archivo = Path("csv/productos.csv")):
        archivo = Path(archivo)  # convertir a Path
        archivo.parent.mkdir(parents=True, exist_ok=True)  # crea carpeta si no existe
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "precio", "talla", "cantidad", "categoria"])
            writer.writeheader()
            writer.writerows([p.obtener_producto() for p in productos])      
        
    # Mostrar string con info del producto
    def __str__(self):    
        return f"ID: {self.__id_producto} | {self.__nombre} | Talla: {self.__talla} | Precio: €{self.__precio:.2f} | Stock: {self.__cantidad}"
        

# # EJEMPLO DE USO    
# # Crear productos
# p1 = Producto(1, "Camiseta", 19.99, "M", 10, "Ropa")
# p2 = Producto(2, "Pantalón", 39.5, "L", 3, "Ropa")
# p3 = Producto(3, "Zapatos", 59.9, "42", 0, "Calzado")

# # Mostrar productos
# print("Mostrar productos:")
# print(p1)
# print(p2)
# print(p3)

# # Verificar estado del stock
# print("Estado del stock:")
# print(f"Producto: {p1.id_producto} - {p1.nombre}", p1.obtener_estado_stock())  # EN STOCK
# print(p2.obtener_estado_stock())  # STOCK BAJO
# print(p3.obtener_estado_stock())  # SIN STOCK

# # Actualizar cantidad
# p2.actualizar_stock(12)
# print(p2)

# # Guardar en archivos
# productos = [p1, p2, p3]
# Producto.guardar_json(productos, "json/productos.json")
# Producto.guardar_csv(productos, "csv/productos.csv")

# # Lista de productos
# Producto.obtener_productos(productos)
      