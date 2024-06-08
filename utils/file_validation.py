#file_validation

def validar_nombre_archivo(ruta_archivo, palabra_clave):
    return palabra_clave.lower() in ruta_archivo.lower()
