from typing import List # esto permite utilizar List en type-hinting
from inmueble import Inmueble # esto permite utilizar Inmueble en type-hinting

class ZonaGeografica:

    def __init__(self, nombre : str, pais : str, inmuebles : List[Inmueble, ...]) -> None:
        self.__nombre = nombre
        self.__pais = pais
        self.__inmuebles = inmuebles
