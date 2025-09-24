import json
import hashlib

ARCHIVO_USUARIOS="usuarios.json"

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

        
def  registrar_usuario(username, password):
    try:
        with open(ARCHIVO_USUARIOS, 'r') as f:
            usuarios = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {}
    
    if username in usuarios:
        print("Error: El nombre de usuario ya existe.")
        return False
    
    password_hash=hashlib.sha256(password.encode()).hexdigest() #Pasar la contraseña a hash
    usuarios[username] = {"password_hash":password_hash, "rol":"cliente"}
    
    with open(ARCHIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f, indent=4)
    
    print(f"¡Usuario {username} registrado con éxito!")
    return True

def iniciar_sesion(username,password):
    try:
        with open(ARCHIVO_USUARIOS, 'r') as f:
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
    
def es_admin(usuario):
    return usuario is not None and usuario.get_rol() == 'admin'

if __name__ == '__main__':
    registrar_usuario("esteve2","pass123")
    esteve2=iniciar_sesion("esteve2","pass123")
    if esteve2:
        if es_admin(esteve2):
            print("Es admin")
        else:
            print("No es admin")