from modelos.habitacion import Habitacion

class Banyo(Habitacion):
    """
        Clase que representa un baño dentro de una vivienda, heredando de la clase Habitacion.

        Attributes
        ----------
        superficie : float
            Superficie total del baño en metros cuadrados (heredado de Habitacion).
        tiene_ducha : bool
            Indica si el baño dispone de ducha.
        tiene_banyera : bool
            Indica si el baño dispone de bañera.
        tiene_vater : bool
            Indica si el baño dispone de váter/inodoro.
        tiene_lavabo : bool
            Indica si el baño dispone de lavabo. Por defecto, True.
        """

    def __init__(self, superficie : float, tiene_ducha : bool = False, tiene_banyera : bool = False,
                 tiene_vater : bool = False, tiene_lavabo : bool = True):
        """
        Inicializa una nueva instancia de la clase Banyo.

        Parameters
        ----------
        superficie : float
            Superficie total del baño en metros cuadrados.
        tiene_ducha : bool, optional
            Indica si el baño tiene ducha (por defecto False).
        tiene_banyera : bool, optional
            Indica si el baño tiene bañera (por defecto False).
        tiene_vater : bool, optional
            Indica si el baño tiene váter/inodoro (por defecto False).
        tiene_lavabo : bool, optional
            Indica si el baño tiene lavabo (por defecto True).
        """
        super().__init__(superficie)
        self.__tiene_ducha = tiene_ducha
        self.__tiene_banyera = tiene_banyera
        self.__tiene_vater = tiene_vater
        self.__tiene_lavabo = tiene_lavabo
