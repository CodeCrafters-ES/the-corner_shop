import sqlite3
from pathlib import Path
from typing import List, Optional
from modules.producto import Producto

class ProductoRepository:
    """
    Clase para manejar las operaciones de base de datos para productos
    """
    
    def __init__(self, db_path: str = "tienda.db"):
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Inicializa la base de datos con las tablas necesarias"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys=ON")            
            
    def _get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys=ON")
        conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        return conn
    
    def crear_producto(self, producto: Producto) -> bool:
        """
        Inserta un nuevo producto en la base de datos
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO productos (nombre, precio, talla, cantidad)
                    VALUES (?, ?, ?, ?)
                """, (producto.nombre, producto.precio, producto.talla, producto.cantidad))
                conn.commit()
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: El producto '{producto.nombre}' ya existe")
            return False
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return False
    
    def obtener_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        """
        Obtiene un producto por su ID
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
                row = cursor.fetchone()
                
                if row:
                    return Producto(
                        id_producto=row['id'],
                        nombre=row['nombre'],
                        precio=row['precio'],
                        talla=row['talla'],
                        cantidad=row['cantidad']
                    )
                return None
        except sqlite3.Error as e:
            print(f"Error al obtener producto: {e}")
            return None
    
    def obtener_todos_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos de la base de datos
        """
        productos = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos ORDER BY id")
                rows = cursor.fetchall()
                
                for row in rows:
                    producto = Producto(
                        id_producto=row['id'],
                        nombre=row['nombre'],
                        precio=row['precio'],
                        talla=row['talla'],
                        cantidad=row['cantidad']
                    )
                    productos.append(producto)
        except sqlite3.Error as e:
            print(f"Error al obtener productos: {e}")
        
        return productos
    
    def actualizar_producto(self, producto: Producto) -> bool:
        """
        Actualiza un producto existente en la base de datos
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE productos 
                    SET nombre = ?, precio = ?, talla = ?, cantidad = ?
                    WHERE id = ?
                """, (producto.nombre, producto.precio, producto.talla, 
                     producto.cantidad, producto.id_producto))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    print(f"No se encontró el producto con ID {producto.id_producto}")
                    return False
        except sqlite3.IntegrityError as e:
            print(f"Error: El nombre '{producto.nombre}' ya existe")
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, id_producto: int) -> bool:
        """
        Elimina un producto de la base de datos
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    print(f"No se encontró el producto con ID {id_producto}")
                    return False
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos por nombre (búsqueda parcial)
        """
        productos = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM productos 
                    WHERE nombre LIKE ? 
                    ORDER BY nombre
                """, (f"%{nombre}%",))
                rows = cursor.fetchall()
                
                for row in rows:
                    producto = Producto(
                        id_producto=row['id'],
                        nombre=row['nombre'],
                        precio=row['precio'],
                        talla=row['talla'],
                        cantidad=row['cantidad']
                    )
                    productos.append(producto)
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
        
        return productos
    
    def obtener_productos_por_talla(self, talla: str) -> List[Producto]:
        """
        Obtiene productos filtrados por talla
        """
        productos = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM productos 
                    WHERE talla = ? 
                    ORDER BY nombre
                """, (talla.upper(),))
                rows = cursor.fetchall()
                
                for row in rows:
                    producto = Producto(
                        id_producto=row['id'],
                        nombre=row['nombre'],
                        precio=row['precio'],
                        talla=row['talla'],
                        cantidad=row['cantidad']
                    )
                    productos.append(producto)
        except sqlite3.Error as e:
            print(f"Error al filtrar por talla: {e}")
        
        return productos
    
    def actualizar_stock(self, id_producto: int, nueva_cantidad: int) -> bool:
        """
        Actualiza solo el stock de un producto
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE productos 
                    SET cantidad = ? 
                    WHERE id = ?
                """, (nueva_cantidad, id_producto))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    print(f"No se encontró el producto con ID {id_producto}")
                    return False
        except sqlite3.Error as e:
            print(f"Error al actualizar stock: {e}")
            return False
    
    def obtener_productos_stock_bajo(self, limite: int = 5) -> List[Producto]:
        """
        Obtiene productos con stock bajo
        """
        productos = []
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM productos 
                    WHERE cantidad <= ? 
                    ORDER BY cantidad ASC
                """, (limite,))
                rows = cursor.fetchall()
                
                for row in rows:
                    producto = Producto(
                        id_producto=row['id'],
                        nombre=row['nombre'],
                        precio=row['precio'],
                        talla=row['talla'],
                        cantidad=row['cantidad']
                    )
                    productos.append(producto)
        except sqlite3.Error as e:
            print(f"Error al obtener productos con stock bajo: {e}")
        
        return productos


# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia del repositorio
    repo = ProductoRepository("tienda.sql")
    
    # Crear un nuevo producto
    try:
        nuevo_producto = Producto(
            id_producto=0,  # Se asignará automáticamente por la BD
            nombre="Camiseta Básica",
            precio=19.99,
            talla="M",
            cantidad=10
        )
        
        if repo.crear_producto(nuevo_producto):
            print("✅ Producto creado exitosamente")
        else:
            print("❌ Error al crear producto")
    except ValueError as e:
        print(f"Error de validación: {e}")
    
    # Obtener todos los productos
    productos = repo.obtener_todos_productos()
    print(f"\n📦 Total de productos: {len(productos)}")
    for producto in productos:
        print(producto)
    
    # Buscar productos
    resultados = repo.buscar_productos_por_nombre("Camiseta")
    print(f"\n🔍 Productos encontrados: {len(resultados)}")
    for producto in resultados:
        print(producto)
    
    # Productos con stock bajo
    stock_bajo = repo.obtener_productos_stock_bajo(5)
    print(f"\n⚠️ Productos con stock bajo: {len(stock_bajo)}")
    for producto in stock_bajo:
        print(f"{producto} - Estado: {producto.obtener_estado_stock()}")