from modelos.inmueble.inmueble import Inmueble # lo importamos para poder usarlo en type-hinting
from modelos.usuario.vendedor import Vendedor
from modelos.comentario import Comentario
from typing import List, Optional

class Publicacion:
    """
    Clase que representa una publicación de un inmueble en una plataforma de anuncios.

    Attributes
    ----------
    inmueble : Inmueble
        Objeto que representa el inmueble a publicar.
    precio : float
        Precio de venta o alquiler del inmueble.
    vendedor : Vendedor
        Objeto que representa al vendedor del inmueble.
    fecha_publicacion : str
        Fecha en la que se realizó la publicación (formato de fecha como cadena).
    comentarios : List[Comentario]
        Lista de comentarios realizados en la publicación.
    vendido : bool
        Indica si el inmueble ya fue vendido (por defecto False).
    tipo_alquiler : Optional[str]
        Tipo de alquiler si aplica (por ejemplo: "temporal", "permanente").
    """

    def __init__(self, inmueble : Inmueble, precio : float, vendedor : Vendedor,
                 fecha_publicacion : str, comentarios : List[Comentario],
                 vendido : bool = False, tipo_alquiler: Optional[str] = None):
        """
                Inicializa una nueva instancia de la clase Publicacion.

                Parameters
                ----------
                inmueble : Inmueble
                    El inmueble que se desea publicar.
                precio : float
                    El precio asignado al inmueble.
                vendedor : Vendedor
                    La persona u organización que publica el inmueble.
                fecha_publicacion : str
                    Fecha de publicación de la oferta.
                comentarios : List[Comentario]
                    Lista de comentarios sobre la publicación.
                vendido : bool, optional
                    Estado de la publicación; True si ya fue vendido (por defecto False).
                tipo_alquiler : Optional[str], optional
                    Tipo de alquiler si no es una venta directa (por defecto None).
                """
        self.__inmueble = inmueble
        self.__precio = precio
        self.__vendedor = vendedor
        self.__fecha_publicacion = fecha_publicacion
        self.__vendido = vendido
        self.comentarios = comentarios
        self.tipo_alquiler = tipo_alquiler

    @property
    def inmueble(self) -> Inmueble:
        return self.__inmueble

    @inmueble.setter
    def inmueble(self, nuevo_inmueble : Inmueble) -> None:
        if not isinstance(nuevo_inmueble, Inmueble):
            raise TypeError("El inmueble debe ser una instancia de Inmueble")
        self.__inmueble = nuevo_inmueble

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio: float) -> None:
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")
        self.__precio = nuevo_precio

    @property
    def vendedor(self) -> Vendedor:
        return self.__vendedor

    @vendedor.setter
    def vendedor(self, nuevo_vendedor: Vendedor) -> None:
        if not isinstance(nuevo_vendedor, Vendedor):
            raise TypeError("El vendedor debe ser una instancia de Vendedor")
        self.__vendedor = nuevo_vendedor

    @property
    def fecha_publicacion(self) -> str:
        return self.__fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, nueva_fecha: str) -> None:
        self.__fecha_publicacion = nueva_fecha

    @property
    def vendido(self) -> bool:
        return self.__vendido

    @vendido.setter
    def vendido(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise TypeError("El estado debe ser booleano")
        self.__vendido = estado