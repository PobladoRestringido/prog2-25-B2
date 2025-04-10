from typing import List  # Esto permite utilizar List en type-hinting
from modelos.inmueble import Inmueble  # Esto permite utilizar Inmueble en type-hinting

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

    def __init__(self, nombre: str, pais: str, inmuebles: List[Inmueble,...]) -> None:
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
        self.__inmuebles = inmuebles

