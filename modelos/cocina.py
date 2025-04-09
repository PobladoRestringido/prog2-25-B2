from modelos.habitacion import Habitacion

class Cocina(Habitacion):

    def __init__(self,  superficie : float, tiene_frigorifico : bool = False, tiene_horno : bool = False,
                 tiene_microondas : bool = False, tiene_fregadero : bool = False, tiene_mesa : bool = False) -> None:
        super().__init__(superficie)
        self.__tiene_frigorifico = tiene_frigorifico
        self.__tiene_horno = tiene_horno
        self.__tiene_microondas = tiene_microondas
        self.__tiene_fregadero = tiene_fregadero
        self.__tiene_mesa = tiene_mesa