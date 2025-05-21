from modelos.inmueble.inmueble import Inmueble
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

    def __init__(self, duenyo: 'Persona', descripcion:str,precio:float,nombre:str,habitaciones : list['Habitacion', ...], zona : 'ZonaGeografica',
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
        super().__init__(duenyo,habitaciones,zona,nombre,descripcion,precio)
        self.__tiene_piscina = tiene_piscina
        self.__jardin = jardin

    def tipo(self) -> str:
        return "vivienda unifamiliar"

    @property
    def descripcion(self):
        return self._Inmueble__descripcion

    @property
    def precio(self):
        return self._Inmueble__precio

    @property
    def tiene_piscina(self) -> bool:
        return self.__tiene_piscina

    @property
    def jardin(self) -> Optional['Jardin']:
        return self.__jardin

    def __len__(self):
        return len(self.habitaciones)

    def __str__(self):
        extras = []
        if self.tiene_piscina:
            extras.append("piscina")
        if self.jardin:
            extras.append("jardín")

        extra_texto = ", ".join(extras) if extras else "sin extras"

        return (
            f"Vivienda unifamiliar ({extra_texto})\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Habitaciones: {len(self)}\n"
            f"Precio: {self.precio} €\n"
            f"Zona: {self.zona}"
        )

    def to_dict(self):
        return {
            "tipo": "vivienda_unifamiliar",
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "zona": self.zona.nombre,
            "pais": self.zona.pais,
            "duenyo": self.duenyo.nombre,
            "tiene_piscina": self.tiene_piscina,
            "jardin": self.jardin,
            "habitaciones": [str(hab) for hab in self.habitaciones]
        }
