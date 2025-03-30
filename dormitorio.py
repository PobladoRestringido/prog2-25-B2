from habitacion import Habitacion

class dormitorio(Habitacion):

    def __init__(self, superficie : float, tiene_cama : bool = False,
                 tiene_lampara : bool = False, tiene_mesa_estudio : bool = False):
        super().__init__(superficie)
        self.__tiene_cama = tiene_cama
        self.__tiene_lampara = tiene_lampara
        self. tiene_mesa_estudio = tiene_mesa_estudio
        