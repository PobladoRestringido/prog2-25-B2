# pickling.py
# módulo encargado de la serialización/des-serialización

import pickle
from typing import Any

def cargar_data() -> dict[str, Any]:
    """
    Metodo encargado de hacer el unpickling (i.e. de-serialización) de toda
    la información que deba permanecer en disco.

    Si el fichero no existe, crea uno nuevo y devuelve un diccionario vacío

    Retorna
    -------
    dict[str, Any]
        - diccionario con toda la información guardada en disco durante
        sesiones anteriores
    """
    try:
        with open('data.pkl', 'rb') as file:
            return pickle.load(file)

    except FileNotFoundError:
        print("Warning: No se ha encontrado el fichero 'data.txt'. "
              "Creando fichero...")
        with open('data.txt', 'wb') as file:
            pickle.dump({}, file)
        return {}

def guardar_data(data : dict[str, Any]) -> None:
    """
    Metodo encargado de hacer el pickling (i.e. serialización) de toda
    la información que deba permanecer en disco.

    Parámetros
    ----------
    data: dict[str, Any]
        - diccionario con toda la información que deba permanecer en disco
    """

    with open('data.pkl', 'wb') as file:
        pickle.dump(data, file)