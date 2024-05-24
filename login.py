# login.py

import json

def cargar_usuarios():
    try:
        with open("usuarios.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f)

def login(username, password, usuarios):
    stored_password = usuarios.get(username)
    if stored_password == password:
        return True
    return False

def crear_usuario(nuevo_usuario, nueva_contraseña, usuarios):
    # Verificar si el nombre de usuario ya existe
    if nuevo_usuario in usuarios:
        return False
    else:
        # Si no existe, agregar el nuevo usuario y su contraseña al diccionario de usuarios
        usuarios[nuevo_usuario] = nueva_contraseña
        guardar_usuarios(usuarios)
        return True
