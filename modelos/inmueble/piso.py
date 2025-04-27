# piso.py
from modelos.inmueble.inmueble import Inmueble

class Piso(Inmueble):
    """
    Clase usada para representar un inmueble de tipo piso / apartamento

    Atributos
    ---------
    nombre : str
        nombre del piso
    descripcion : str
        descripcion del piso
    habitaciones : list['Habitacion']
        lista de habitaciones
    precio : float
        precio del piso
    zona : 'ZonaGeográfica'
        ubicación geográfica del piso
    duenyo : 'Persona'
        dueño del piso
    planta : int
        planta donde se ubica el apartamento
    ascensor : bool
        existencia de ascensor
    """

    def __init__(self, nombre : str, descripcion : str, habitaciones : list['Habitacion'], precio : float, zona : 'ZonaGeográfica', duenyo : 'Persona', planta : int, ascensor : bool = False) -> None:
        """
        Parámetros
        ----------
        nombre : str
            Nombre del piso o apartamento.
        descripcion : str
            Descripción detallada del inmueble.
        habitaciones : list['Habitacion']
            Lista de objetos de tipo Habitacion que componen el piso.
        precio : float
            Precio del inmueble en euros (€).
        zona : ZonaGeográfica
            Zona geográfica en la que se encuentra el piso.
        duenyo : Persona
            Persona propietaria del piso.
        planta : int
            Número de planta donde se encuentra el piso. Debe ser 0 o mayor.
        ascensor : bool, opcional
            Indica si el edificio dispone de ascensor (por defecto es False).

        Excepciones
        -----------
        ValueError
            Si el número de planta es negativo.
        """
        super().__init__(nombre, descripcion, habitaciones, precio, zona, duenyo)
        self.__tiene_ascensor = ascensor
        if planta < 0:
            raise ValueError("La planta no puede ser negativa")
        self.__planta = planta

    @property
    def tiene_ascensor(self) -> bool:
        return self.__tiene_ascensor

    @property
    def planta(self) -> int:
        return self.__planta

    @planta.setter
    def planta(self, nueva_planta : int):
        if nueva_planta < 0:
            raise ValueError("La planta no puede ser negativa")
        self.__planta = nueva_planta

    def __len__(self):
        return len(self.habitaciones)

    def __str__(self):
        base = (f"Piso en planta {self.planta} con {'ascensor' if self.tiene_ascensor else 'sin ascensor'}\n"
                f"Nombre: {self.nombre}\n"
                f"Descripción: {self.descripcion}\n"
                f"Nº habitaciones: {len(self)}\n"
                f"Precio: {self.precio} €\n"
                f"Zona: {self.zona}")
        return base