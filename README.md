# 🛍️ The Corner Shop

**The Corner Shop** es una tienda online de ropa minimalista, desarrollada con Python y SQLite. Este proyecto simula una plataforma de e-commerce donde los usuarios pueden explorar productos, gestionar su carrito de compras y realizar pedidos, mientras que los administradores pueden administrar el inventario y las ventas.

## 🚀 Características principales

- Catálogo de productos con imágenes, precios y descripciones.
- Sistema de autenticación para usuarios y administradores.
- Gestión de carrito de compras y pedidos.
- Panel de administración para CRUD de productos.
- Base de datos relacional con SQLite.
- Backend modular en Python con enfoque OOP.
- Interfaz web sencilla con HTML/CSS (opcionalmente integrable con Flask o Django).

## 🧱 Tecnologías utilizadas

- **Python 3.10+**
- **SQLite3**
- **HTML/CSS** (para la interfaz)
- **Flask** (opcional para servir la app)
- **Jinja2** (si se usa Flask para plantillas)

## 🗂️ Estructura del proyecto

```bash
the-corner-shop/ 
├── README.md
├── requirements.txt
├── .gitignore
├── main.py
│
├── models/ 
│   ├── __init__.py
│   ├── product.py 
│   ├── user.py 
│   └── order.py 
│
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py
│   ├── producto_repository.py
│   ├── usuario_repository.py
│   └── carrito_repository.py
│
├── services/
│   ├── __init__.py
│   ├── producto_service.py
│   ├── usuario_service.py
│   └── carrito_service.py
│
├── controllers/
│   ├── __init__.py
│   ├── producto_controller.py
│   ├── usuario_controller.py
│   └── carrito_controller.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   ├── migrations/
│   │   ├── 001_initial_schema.sql
│   │   └── 002_add_categories.sql
│   └── seeds/
│       ├── productos_ejemplo.json
│       └── usuarios_ejemplo.json
│
├── data/
│   ├── exports/
│   │   ├── csv/
│   │   └── json/
│   └── backups/
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_models/
    │   ├── __init__.py
    │   ├── test_producto.py
    │   ├── test_usuario.py
    │   └── test_carrito.py
    ├── test_repositories/
    │   ├── __init__.py
    │   ├── test_producto_repository.py
    │   ├── test_usuario_repository.py
    │   └── test_carrito_repository.py
    └── test_services/
        ├── __init__.py
        ├── test_producto_service.py
        ├── test_usuario_service.py
        └── test_carrito_service.py
```

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/the-corner-shop.git
cd the-corner-shop
```

## Ejecuta la aplicación

```bash
python app/main.py
```

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.
