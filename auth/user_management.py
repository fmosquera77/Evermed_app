#user_management

import json
from auth.login import cargar_usuarios

def crear_usuario(username, password):
    users = cargar_usuarios()
    if username in users:
        return False
    users[username] = password
    with open('users.json', 'w') as file:
        json.dump(users, file)
    return True
