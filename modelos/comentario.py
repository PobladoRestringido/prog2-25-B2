from modelos.comprador import Comprador  # Lo importamos para poder usarlo en type-hinting

class Comentario:
    """
    Clase que representa un comentario realizado por un comprador sobre una publicación.

    Attributes
    ----------
    contenido : str
        Texto del comentario realizado.
    autor : Comprador
        Objeto que representa al comprador que hizo el comentario.
    fecha_publicacion : str
        Fecha en la que se realizó el comentario (como cadena de texto).
    """

    def __init__(self, contenido: str, autor: Comprador, fecha_publicacion: str):
        """
        Inicializa una nueva instancia de la clase Comentario.

        Parameters
        ----------
        contenido : str
            Contenido del comentario.
        autor : Comprador
            Comprador que realizó el comentario.
        fecha_publicacion : str
            Fecha del comentario (en formato de texto, por ejemplo '2025-01-23').
        """
        self.__contenido = contenido
        self.__autor = autor
        self.__fecha_publicacion = fecha_publicacion
