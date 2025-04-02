from modelos.habitacion import Habitacion

class Banyo(Habitacion):

    def __init__(self, superficie : float, tiene_ducha : bool = False, tiene_banyera : bool = False,
                 tiene_vater : bool = False, tiene_lavabo : bool = True):
        super().__init__(superficie)
        self.__tiene_ducha = tiene_ducha
        self.__tiene_banyera = tiene_banyera
        self.__tiene_vater = tiene_vater
        self.__tiene_lavabo = tiene_lavabo

