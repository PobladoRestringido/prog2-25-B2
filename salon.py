from habitacion import Habitacion

class Salon:
    def __init__(self):
        def __init__(self, superficie: float, tiene_televisor: bool = False, tiene_sofa: bool = False,
                     tiene_mesa_recreativa: bool = False) -> None:
            super().__init__(superficie)
            self.__tiene_televisor = tiene_televisor
            self.__tiene_sofa = tiene_sofa
            self.__tiene_mesa_recreativa = tiene_mesa_recreativa
        

