class Habitacion:
    """
    Clase que representa una habitación dentro de un inmueble.

    Atributos privados:
        __superficie (float): Superficie de la habitación en metros cuadrados.

    Métodos:
        __init__(superficie): Constructor que inicializa la superficie de la habitación.

    Ejemplo de uso:
        h1 = Habitacion(12.5)
    """
    def __init__(self, superficie : float):
        """
        Inicializa una nueva instancia de Habitacion.

        Parámetros:
            superficie (float): Superficie de la habitación en m².
        """
        self.__superficie = superficie

