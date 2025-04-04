from modelos.inmueble import Inmueble
from typing import Optional

class ViviendaUnifamiliar(Inmueble):

    def __init__(self, duenyo: 'Persona', habitaciones : list['Habitacion', ...], zona : 'ZonaGeografica',
                 tiene_piscina : bool = False, jardin : Optional['Jardin'] = None) -> None:
        super().__init__(duenyo, habitaciones, zona)
        self.__tiene_piscina = tiene_piscina
        self.__jardin = jardin

