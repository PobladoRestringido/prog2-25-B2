from modelos.inmueble import Inmueble
from typing import Optional

class ViviendaUnifamiliar(Inmueble):
    """
    Clase que representa una vivienda unifamiliar, como una casa o chalet.

    Atributos
    ----------
    tiene_piscina : bool
        Indica si la vivienda cuenta con piscina.
    jardin : Optional[Jardin]
        Objeto que representa el jardín de la vivienda, si tiene.
    """

    def __init__(self, duenyo: 'Persona', habitaciones : list['Habitacion', ...], zona : 'ZonaGeografica',
                 tiene_piscina : bool = False, jardin : Optional['Jardin'] = None) -> None:
        """
        Inicializa una nueva instancia de ViviendaUnifamiliar.

        Parametros
        ----------
        duenyo : Persona
            Persona propietaria de la vivienda.
        habitaciones : list[Habitacion]
            Lista de habitaciones que componen la vivienda.
        zona : ZonaGeografica
            Zona geográfica en la que se encuentra la vivienda.
        tiene_piscina : bool, optional
            True si la vivienda cuenta con piscina (por defecto False).
        jardin : Optional[Jardin], optional
            Jardín de la vivienda, si tiene (por defecto None).
        """
        super().__init__(duenyo, habitaciones, zona)
        self.__tiene_piscina = tiene_piscina
        self.__jardin = jardin


