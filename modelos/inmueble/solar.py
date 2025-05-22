# solar.py
from typing import Optional
from __future__ import annotations
from modelos.inmueble.inmueble import Inmueble
from modelos.excepciones import SuperficieInvalidaError

class Solar(Inmueble):
    """
    Clase usada para representar un solar (terreno)

    Parámetros
    ----------
    duenyo : Persona
        Propietario del solar
    zona : ZonaGeografica
        Zona donde se ubica
    nombre : str
        Nombre identificativo de la parcela
    descripcion : str
        Descripción del terreno
    precio : float
        Precio de venta en euros
    area : float
        Superficie del terreno en metros cuadrados
    edificable : bool
        Indica si el terreno es edificable según la normativa
    uso : str
        Uso del suelo

    Excepciones
    -----------
    SuperficieInvalidaError
        Si el área es nula o negativa
    """

    def __init__(self, duenyo: "Persona", zona: "ZonaGeografica", nombre: str, descripcion: str, precio: float, area: float, *, edificable: bool = False, uso: Optional[str] = None) -> None:
        if area is None or area <= 0:
            raise SuperficieInvalidaError("El área de un solar debe ser mayor que 0", field="area", value=area)
        super().__init__(duenyo, [], zona, nombre, descripcion, precio)
        self.__area: float = area
        self.__edificable: bool = edificable
        self.__uso Optional[str] = uso

    @property
    def area(self) -> float:
        """Metros cuadrados del terreno"""
        return self.__area

    @property
    def edificable(self) -> bool:
        """True si la normativa permite construir en el solar"""
        return self.__edificable

    @property
    def uso(self) -> Optional[str]:
        """Uso del suelo"""
        return self.__uso

    def tipo(self) -> str:
        return "solar"

    def __len__(self) -> int:
        """Número de habitaciones"""
        return 0

    def __str__(self) -> str:
        edificable_txt = "edificable" if self.edificable else "no edificable"
        uso_txt = f"Uso: {self.uso}" if self.uso else "Uso no especificado"

        return (
            f"Solar ({edificable_txt})\n"
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Área: {self.area} m²\n"
            f"Precio: {self.precio} €\n"
            f"Zona: {self.zona}\n"
            f"{uso_txt}"
        )

    def to_dict(self) -> dict[str, object]:
        """Representación serializable del solar."""
        return {
            "tipo": "solar",
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "zona": self.zona.nombre,
            "pais": self.zona.pais,
            "duenyo": self.duenyo.nombre,
            "area": self.area,
            "edificable": self.edificable,
            "uso": self.uso,
            "habitaciones": [],  # siempre vacío
        }