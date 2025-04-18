from modelos.habitacion import Habitacion

class Cocina(Habitacion):
    """
    Clase que representa una cocina como una habitación dentro de un inmueble.

    Atributos
    ----------
    tiene_frigorifico : bool
        Indica si la cocina tiene frigorífico.
    tiene_horno : bool
        Indica si la cocina tiene horno.
    tiene_microondas : bool
        Indica si la cocina tiene microondas.
    tiene_fregadero : bool
        Indica si la cocina tiene fregadero.
    tiene_mesa : bool
        Indica si la cocina tiene una mesa.
    """

    def __init__(self, superficie: float, tiene_frigorifico: bool = False, tiene_horno: bool = False, tiene_microondas: bool = False,
        tiene_fregadero: bool = False, tiene_mesa: bool = False) -> None:
        """
        Inicializa una nueva instancia de la clase Cocina.

        Parametros
        ----------
        superficie : float
            Superficie total de la cocina en metros cuadrados.
        tiene_frigorifico : bool, optional
            True si la cocina incluye un frigorífico (por defecto False).
        tiene_horno : bool, optional
            True si la cocina incluye un horno (por defecto False).
        tiene_microondas : bool, optional
            True si la cocina incluye un microondas (por defecto False).
        tiene_fregadero : bool, optional
            True si la cocina incluye un fregadero (por defecto False).
        tiene_mesa : bool, optional
            True si la cocina incluye una mesa (por defecto False).
        """
        super().__init__(superficie)

        self.__tiene_frigorifico = tiene_frigorifico
        self.__tiene_horno = tiene_horno
        self.__tiene_microondas = tiene_microondas
        self.__tiene_fregadero = tiene_fregadero
        self.__tiene_mesa = tiene_mesa

