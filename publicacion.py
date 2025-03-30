from inmueble import Inmueble # lo importamos para poder usarlo en type-hinting
from vendedor import Vendedor
from comentario import Comentario
from typing import List

class Publicacion:

    def __init__(self, inmueble : Inmueble, precio : float, vendedor : Vendedor,
                 fecha_publicacion : str, comentarios : List[Comentario, ...],
                 vendido : bool = False):
        self.__inmueble = inmueble
        self.__precio = precio
        self.__vendedor = vendedor
        self.__fecha_publicacion = fecha_publicacion
        self.__vendido = vendido
        self.comentarios = comentarios