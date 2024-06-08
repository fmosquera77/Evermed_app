# login.py

import json
import os

def login(username, password):
    users = cargar_usuarios()
    if username in users and users[username] == password:
        return True
    return False

def cargar_usuarios():
    with open('users.json', 'r') as file:
        users = json.load(file)
    return users
