# habitacion.py
from modelos.excepciones import SuperficieInvalidaError

class Habitacion:
    """
    Clase que representa una habitación dentro de un inmueble.

    Descripción:
    -------------
    Esta clase modela una habitación. Se almacena la superficie en metros
    cuadrados, lo que determinará el tamaño del inmueble. A cada instancia se
    le asigna un identificador único a partir de un contador, que persiste en
    el fichero `contador_habitaciones.txt`.

    Atributos:
    -----------
    __superficie : float
        Superficie de la habitación en metros cuadrados.
    __id : int
        Identificador único asignado a la habitación.
    contador_habitaciones : int
        Atributo de clase contador que se incrementa para asignar un id
        único a cada instancia.

    Métodos:
    --------
    __init__(superficie: float)
        Inicializa la instancia y actualiza el contador persistente.
    """

    try:
        with open('contador_habitaciones.txt', 'r') as file:
            contador_habitaciones: int = int(file.read())
    except FileNotFoundError:
        with open('contador_habitaciones.txt', 'w') as file:
            file.write('0')
        contador_habitaciones: int = 0

    def __init__(self, superficie: float):
        """
        Inicializa una nueva instancia de Habitacion.

        Parámetros:
        -----------
        superficie : float
            Superficie de la habitación en metros cuadrados.
        """
        self.__id = self.__class__.contador_habitaciones

        if superficie is None or superficie <= 0:
            raise SuperficieInvalidaError("La superficie debe ser mayor que 0", field="superficie", value=superficie)
        self.__superficie = superficie

        self.__class__.contador_habitaciones += 1

        with open('contador_habitaciones.txt', 'w') as file:
            file.write(str(self.__class__.contador_habitaciones))

    def __str__(self):
        return f"Habitación {self.__id} - {self.__superficie} m²"

    def to_dict(self):
        return {
            "id": self.__id,
            "superficie": self.__superficie
        }

    @property
    def id(self) -> int:
        return self.__id

    @@property
    def superficie(self) -> float:
        return self.__superficie