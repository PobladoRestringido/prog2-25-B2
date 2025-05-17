from modelos.habitacion.habitacion import Habitacion

class Dormitorio(Habitacion):
    """
    Clase que representa un dormitorio dentro de un inmueble.

    Atributos
    ----------
    tiene_cama : bool
        Indica si el dormitorio incluye una cama.
    tiene_lampara : bool
        Indica si el dormitorio incluye una lámpara.
    tiene_mesa_estudio : bool
        Indica si el dormitorio incluye una mesa de estudio.
    """

    def __init__(self, superficie: float, tiene_cama: bool = False, tiene_lampara: bool = False, tiene_mesa_estudio: bool = False):
        """
        Inicializa una nueva instancia de la clase Dormitorio.

        Parametros
        ----------
        superficie : float
            Superficie total del dormitorio en metros cuadrados.
        tiene_cama : bool, optional
            True si el dormitorio tiene cama (por defecto False).
        tiene_lampara : bool, optional
            True si el dormitorio tiene lámpara (por defecto False).
        tiene_mesa_estudio : bool, optional
            True si el dormitorio tiene mesa de estudio (por defecto False).
        """
        super().__init__(superficie)
        self.__tiene_cama = tiene_cama
        self.__tiene_lampara = tiene_lampara
        self.__tiene_mesa_estudio = tiene_mesa_estudio

    def __str__(self):
        extras = []
        if self.tiene_cama:
            extras.append("cama")
        if self.tiene_lampara:
            extras.append("lámpara")
        if self.tiene_mesa_estudio:
            extras.append("mesa de estudio")
        extras_str = ", ".join(extras) if extras else "sin extras"
        return f"Dormitorio {extras_str} - {super().__str__()}"

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "dormitorio",
            "tiene_cama": self.__tiene_cama,
            "tiene_lampara": self.__tiene_lampara,
            "tiene_mesa_estudio": self.__tiene_mesa_estudio
        })
        return base
        