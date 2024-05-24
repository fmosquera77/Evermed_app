# login.py

def login(username, password):
    users = {
        "fmosquera": "fernando77",
        "usuario2": "contraseña2"
    }
    stored_password = users.get(username)
    if stored_password == password:
        return True
    return False
