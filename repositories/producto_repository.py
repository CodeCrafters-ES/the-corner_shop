# Author: Alejandro

from pathlib import Path
from typing import List, Optional
from modules.producto import Producto
from database.db import execute, fetch_one, fetch_all # Funciones helper de conexión

class ProductoRepository:
    """
    Clase para manejar las operaciones de base de datos para productos usando las funciones helper de conexión
    """    
    
    def crear_producto(self, producto: Producto) -> Optional[int]:
        """
        Inserta un nuevo producto en la base de datos
        Retorna el ID del nuevo producto o None si falla
        """
        try:
            nuevo_id = execute(
                "INSERT INTO productos (nombre, precio, talla, cantidad) VALUES (?, ?, ?, ?)",
                (producto.nombre, producto.precio, producto.talla, producto.cantidad)
            )
            # Actualizar el ID del objeto producto
            producto._set_id(nuevo_id)
            return nuevo_id
        except Exception as e:
            print(f"❌ Error al crear producto: {e}")
            return None
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        """
        Obtiene un producto por su ID
        """
        try:
            row = fetch_one("SELECT * FROM productos WHERE id = ?", (id_producto,))
            
            if row:
                return Producto(
                    id_producto=row['id'],
                    nombre=row['nombre'],
                    precio=row['precio'],
                    talla=row['talla'],
                    cantidad=row['cantidad']
                )
            return None
        except Exception as e:
            print(f"❌ Error al obtener producto: {e}")
            return None
    
    def obtener_todos_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos de la base de datos
        """
        try:
            rows = fetch_all("SELECT * FROM productos ORDER BY id")
            
            productos = []
            for row in rows:
                producto = Producto(
                    id_producto=row['id'],
                    nombre=row['nombre'],
                    precio=row['precio'],
                    talla=row['talla'],
                    cantidad=row['cantidad']
                )
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"❌ Error al obtener productos: {e}")
            return []
    
    def actualizar_producto(self, producto: Producto) -> bool:
        """
        Actualiza un producto existente en la base de datos
        """
        try:
            execute(
                """UPDATE productos 
                   SET nombre = ?, precio = ?, talla = ?, cantidad = ?
                   WHERE id = ?""",
                (producto.nombre, producto.precio, producto.talla, 
                 producto.cantidad, producto.id_producto)
            )
            return True
        except Exception as e:
            print(f"❌ Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """
        Elimina un producto de la base de datos
        """
        try:
            execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            return True
        except Exception as e:
            print(f"❌ Error al eliminar producto: {e}")
            return False
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos por nombre (búsqueda parcial)
        """
        try:
            rows = fetch_all(
                "SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre",
                (f"%{nombre}%",)
            )
            
            productos = []
            for row in rows:
                producto = Producto(
                    id_producto=row['id'],
                    nombre=row['nombre'],
                    precio=row['precio'],
                    talla=row['talla'],
                    cantidad=row['cantidad']
                )
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []
    
    def obtener_productos_por_talla(self, talla: str) -> List[Producto]:
        """
        Obtiene productos filtrados por talla
        """
        try:
            rows = fetch_all(
                "SELECT * FROM productos WHERE talla = ? ORDER BY nombre",
                (talla.upper(),)
            )
            
            productos = []
            for row in rows:
                producto = Producto(
                    id_producto=row['id'],
                    nombre=row['nombre'],
                    precio=row['precio'],
                    talla=row['talla'],
                    cantidad=row['cantidad']
                )
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"❌ Error al filtrar por talla: {e}")
            return []        
    
    def actualizar_stock(self, id_producto: int, nueva_cantidad: int) -> bool:
        """
        Actualiza solo el stock de un producto
        """
        try:
            execute(
                "UPDATE productos SET cantidad = ? WHERE id = ?",
                (nueva_cantidad, id_producto)
            )
            return True
        except Exception as e:
            print(f"❌ Error al actualizar stock: {e}")
            return False
    
    def obtener_productos_stock_bajo(self, limite: int = 5) -> List[Producto]:
        """
        Obtiene productos con stock bajo
        """
        try:
            rows = fetch_all(
                "SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC",
                (limite,)
            )
            
            productos = []
            for row in rows:
                producto = Producto(
                    id_producto=row['id'],
                    nombre=row['nombre'],
                    precio=row['precio'],
                    talla=row['talla'],
                    cantidad=row['cantidad']
                )
                productos.append(producto)
            
            return productos
        except Exception as e:
            print(f"❌ Error al obtener productos con stock bajo: {e}")
            return []
        
    def contar_productos(self) -> int:
        """
        Cuenta el total de productos en la base de datos
        """
        try:
            row = fetch_one("SELECT COUNT(*) as total FROM productos")
            return row['total'] if row else 0
        except Exception as e:
            print(f"❌ Error al contar productos: {e}")
            return 0

# # Ejemplo de uso
# if __name__ == "__main__":
#     from database.db import init_db
    
#     # Inicializar la base de datos
#     init_db()
    
#     # Crear instancia del repositorio
#     repo = ProductoRepository()
    
#     # Crear un nuevo producto
#     try:
#         nuevo_producto = Producto(
#             id_producto=0,  # Se asignará automáticamente
#             nombre="Camiseta Básica",
#             precio=19.99,
#             talla="M",
#             cantidad=10
#         )
        
#         nuevo_id = repo.crear_producto(nuevo_producto)
#         if nuevo_id:
#             print(f"✅ Producto creado con ID: {nuevo_id}")
#         else:
#             print("❌ Error al crear producto")
#     except ValueError as e:
#         print(f"⚠️ Error de validación: {e}")
    
#     # Obtener todos los productos
#     productos = repo.obtener_todos_productos()
#     print(f"\n📦 Total de productos: {len(productos)}")
#     for producto in productos:
#         print(producto)
    
#     # Buscar productos
#     resultados = repo.buscar_productos_por_nombre("Camiseta")
#     print(f"\n🔍 Productos encontrados: {len(resultados)}")
#     for producto in resultados:
#         print(producto)
    
#     # Productos con stock bajo
#     stock_bajo = repo.obtener_productos_stock_bajo(5)
#     print(f"\n⚠️ Productos con stock bajo: {len(stock_bajo)}")
#     for producto in stock_bajo:
#         print(f"{producto} - Estado: {producto.obtener_estado_stock()}")