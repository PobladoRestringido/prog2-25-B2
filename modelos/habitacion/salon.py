from modelos.habitacion.habitacion import Habitacion

class Salon(Habitacion):
    """
        Clase que representa un salón dentro de un entorno doméstico o institucional.

        Attributes
        ----------
        superficie : float
            Superficie total del salón en metros cuadrados.
        tiene_televisor : bool
            Indica si el salón dispone de televisor.
        tiene_sofa : bool
            Indica si el salón dispone de sofá.
        tiene_mesa_recreativa : bool
            Indica si el salón tiene una mesa recreativa (ej. futbolín, billar).

        """

    def __init__(self, superficie: float, tiene_televisor: bool = False, tiene_sofa: bool = False,
                     tiene_mesa_recreativa: bool = False) -> None:
        """
            Inicializa una nueva instancia de la clase Salon.

           Parameters
           ----------
           superficie : float
               Superficie total del salón en metros cuadrados.
           tiene_televisor : bool, optional
               Indica si el salón tiene televisor (por defecto False).
           tiene_sofa : bool, optional
               Indica si el salón tiene sofá (por defecto False).
           tiene_mesa_recreativa : bool, optional
               Indica si el salón tiene una mesa recreativa (por defecto False).
                   """
        super().__init__(superficie)
        self.__tiene_televisor = tiene_televisor
        self.__tiene_sofa = tiene_sofa
        self.__tiene_mesa_recreativa = tiene_mesa_recreativa

    @property
    def tiene_televisor(self):
        return self.__tiene_televisor

    @property
    def tiene_sofa(self):
        return self.__tiene_sofa

    @property
    def tiene_mesa_recreativa(self):
        return self.__tiene_mesa_recreativa


    def __str__(self):
        extras = []
        if self.tiene_televisor:
            extras.append("televisor")
        if self.tiene_sofa:
            extras.append("sofá")
        if self.tiene_mesa_recreativa:
            extras.append("mesa recreativa")
        extras_str = ", ".join(extras) if extras else "sin extras"
        return f"Salón {extras_str} - {super().__str__()}"

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "salon",
            "tiene_televisor": self.__tiene_televisor,
            "tiene_sofa": self.__tiene_sofa,
            "tiene_mesa_recreativa": self.__tiene_mesa_recreativa
        })
        return base
