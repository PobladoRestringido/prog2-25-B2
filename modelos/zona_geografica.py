from modelos.inmueble.inmueble import Inmueble
from typing import List


class ZonaGeografica:
    """
    Clase que representa una zona geográfica donde se encuentran ubicados distintos inmuebles.

    Atributos
    ----------
    nombre : str
        Nombre de la zona geográfica.

    pais : str
        País al que pertenece la zona geográfica.

    inmuebles : List[Inmueble]
        Lista de inmuebles ubicados en esta zona.
    """

    def __init__(self, nombre: str, pais: str, inmuebles: List['Inmueble'] = None) -> None:
        """
        Inicializa una nueva instancia de la clase ZonaGeografica.

        Parametros
        ----------
        nombre : str
            Nombre de la zona geográfica.

        pais : str
            País al que pertenece la zona.

        inmuebles : List[Inmueble]
            Lista de inmuebles que pertenecen a esta zona geográfica.
        """
        self.__nombre = nombre
        self.__pais = pais
        if inmuebles is None:
            self.__inmuebles = []
        else:
            self.__inmuebles = inmuebles

    def agregar_inmueble(self, inmueble):
        self.__inmuebles.append(inmueble)

    def __str__(self):
            return f"{self.__nombre} ({self.__pais})"

    def to_dict(self):
            return {
                "nombre": self.__nombre,
                "pais": self.__pais,
                "inmuebles": [inmueble.nombre for inmueble in self.__inmuebles]  # solo los nombres
            }

    @property
    def nombre(self):
        return self.__nombre

    @property
    def pais(self):
        return self.__pais

    @property
    def inmuebles(self):
        return self.__inmuebles



