# pickling.py
# módulo encargado de la serialización/des-serialización

import pickle
from typing import Any

def cargar_data() -> dict[str, Any]:
    """
    Método encargado de hacer el unpickling de los usuarios ya registrados.
    Si el fichero no existe, crea uno nuevo y devuelve un diccionario vacío

    Retorna
    -------
    dict[str, Any]
        diccionario con toda la información extraída del unpickling
    """
    try:
        with open('data.txt', 'rb') as file:
            return pickle.load(file)

    except FileNotFoundError:
        print("Warning: No se ha encontrado el fichero 'data.txt'. Creando fichero...")
        with open('data.txt', 'x') as _:
            return {}

