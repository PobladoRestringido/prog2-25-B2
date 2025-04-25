from modelos.inmueble import Inmueble # lo importamos para poder usarlo en type-hinting
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