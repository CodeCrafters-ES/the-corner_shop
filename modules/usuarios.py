import json
import hashlib
from sqlite3 import IntegrityError
from database.db import get_conn, execute, fetch_one
from pathlib import Path

#Esteve

# ARCHIVO_USUARIOS="../data/usuarios.json"
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # sube de /modules a la raíz
file_path = PROJECT_ROOT / "data" / "exports" / "json" / "usuarios.json"
file_path.parent.mkdir(parents=True, exist_ok=True)  # SI NO EXISTE, crea carpetas


class Usuario:
    def __init__(self, username, password_hash, rol="cliente"):
        self.__username=username
        self.__password_hash=password_hash
        self.__rol=rol
    
    # Getters
    def get_username(self):
        return self.__username
    def get_password_hash(self):
        return self.__password_hash
    def get_rol(self):
        return self.__rol
    # Setters
    def set_username(self, new_username):
        self.__username=new_username
    def set_password_hash(self, new_password_hash):
        self.__password_hash=new_password_hash
    def set_rol(self, new_rol):
        self.__rol=new_rol
    
    #Método estático para hashear la password
    @staticmethod
    def _hash(pwd: str) -> str:
        return hashlib.sha256(pwd.encode("utf-8")).hexdigest()
    
    # REGISTRO DE USUARIOS PARA EL SQLITE con validación de usuario si hay duplicado
    @classmethod
    def create(cls, nombre: str, password: str, rol: str = "cliente") -> dict:
        try:
            new_id = execute(
                    "INSERT INTO usuarios(nombre, password, rol) VALUES (?,?,?)",
                    (nombre, cls._hash(password), rol.lower())
                )
            return {
                "ok": True,
                "id": new_id,
                "msg": f"Usuario '{nombre}' creado con éxito. ¡Ya puedes iniciar sesión!"                
            }         
        except IntegrityError:
            row = fetch_one("SELECT id FROM usuarios WHERE nombre=?", (nombre,))
            return {"ok": False, "error": f"El usuario '{nombre}' ya existe.", "id": row["id"] if row else None}

    #Iniciar sesión con SQLite
    @classmethod
    def login(cls, nombre: str, password: str):
        row = fetch_one(
            "SELECT id, nombre, rol FROM usuarios WHERE nombre=? AND password=?",
            (nombre, cls._hash(password))
        )
        return row
    
    @staticmethod
    def es_admin_row(row) -> bool:
        return bool(row) and row["rol"].lower() == "admin"
    

    # REGISTRO DE USUARIOS PARA EL JSON
    def  registrar_usuario(username, password):
        try:
            with open(file_path, 'r') as f:
                usuarios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            usuarios = {}
        
        if username in usuarios:
            print("Error: El nombre de usuario ya existe.")
            return False
        
        password_hash=hashlib.sha256(password.encode()).hexdigest() #Pasar la contraseña a hash
        usuarios[username] = {"password_hash":password_hash, "rol":"cliente"}
        
        if not file_path.exists():
            with open(file_path, 'w') as f:
                json.dump(usuarios, f, indent=4)
                    
        print(f"¡Usuario {username} registrado con éxito!")
        return True

    # FUNCION PARA INICIO DE SESIÓN
    def iniciar_sesion(username,password):
        try:
            with open(file_path, 'r') as f:
                usuarios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        
        if username in usuarios:
            password_a_verificar_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_a_verificar_hash == usuarios[username]['password_hash']:
                rol = usuarios[username].get('rol', 'cliente') # .get para evitar errores si no hay rol
                usuario_logueado = Usuario(username, usuarios[username]['password_hash'], rol)
                print(f"Bienvenido, {username}!")
                return usuario_logueado
        print("Nombre de usuario o contraseña incorrectas")
        return None
        
    # FUNCION VERIFICAR ADMINISTRADOR
    def is_admin(nombre):
        try:
            with open(file_path, 'r') as f:
                usuarios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        if nombre in usuarios:
                #Busqueda dentro de usuarios, dentro del dict de nombre, en la clave ROL
                if usuarios[nombre]["rol"] == "admin": 
                    print(f"{nombre} es admin")
                else:
                    print(f"{nombre} no tiene permisos de admin")
        