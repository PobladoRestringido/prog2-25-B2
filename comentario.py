from comprador import Comprador # lo importamos para poder usarlo en type-hinting

class Comentario:
    def __init__(self, contenido : str, autor : Comprador, fecha_publicacion : str):
        self.__contenido = contenido
        self.__autor = autor
        self.__fecha_publicacion = fecha_publicacion