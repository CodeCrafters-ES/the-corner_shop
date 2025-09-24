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
├── app/ 
│ ├── models/ 
│ │ ├── product.py 
│ │ ├── user.py 
│ │ └── order.py 
│ ├── controllers/ 
│ │ ├── auth_controller.py 
│ │ ├── product_controller.py 
│ │ └── order_controller.py 
│ ├── views/ 
│ │ └── templates/ 
│ ├── static/ 
│ │ └── css/ 
│ └── main.py 
├── database/ 
│ └── corner_shop.db 
├── requirements.txt 
└── README.md
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
