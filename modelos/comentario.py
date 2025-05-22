from modelos.usuario.comprador import Comprador  # Lo importamos para poder usarlo en type-hinting

class Comentario:
    """
    Clase que representa un comentario realizado por un comprador sobre una publicación.

    Atributos
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

        Parametros
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

    @property
    def contenido(self) -> str:
        """Devuelve el texto del comentario"""
        return self.__contenido

    @contenido.setter
    def contenido(self, nuevo_contenido: str) -> None:
        """Permite actualizar el texto del comentario"""
        if not nuevo_contenido:
            raise ValueError("El contenidoo del comentario no puede estar vacío")
        self.__contenido = nuevo_contenido

    @property
    def autor(self) -> Comprador:
        """Devuelve el comprador que hizo el comentario"""
        return self.__autor

    @autor.setter
    def autor(self, nuevo_autor: Comprador) -> None:
        """Permite cambiar el autor del comentario"""
        if not isinstance(nuevo_autor, Comprador):
            raise TypeError("El autor debe ser una instancia de comprador")
        self.__autor = nuevo_autor

    @property
    def fecha_publicacion(self) -> str:
        """Devuelve la fecha en que se publicó el comentario"""
        return self.__fecha_publicacion

    @fecha_publicacion.setter
    def fecha_publicacion(self, nueva_fecha: str) -> None:
        """Permite cambiar la fecha de publicación"""
        self.__fecha_publicacion = nueva_fecha

    def __repr__(self) -> str:
        return (f"Comentario('{self.contenido}', autor={self.autor.nombre}, fecha_publicacion='{self.fecha_publicacion}')")