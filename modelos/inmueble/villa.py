# villa.py

# [todo] esta clase podría eliminarse, puesto que `vivienda_unifamiliar` hace
#  exactamente lo mismo, y estaba antes
from modelos.inmueble.inmueble import Inmueble

class Villa(Inmueble):
    """
    Clase para representar una villa o casa de lujo

    Atributos
    ---------
    nombre : str
        nombre de la villa
    descripcion : str
        descripcion de la villa
    habitaciones : list['Habitacion']
        lista de habitaciones
    precio : float
        precio de la villa
    zona : 'ZonaGeográfica'
        ubicación geográfica de la villa
    duenyo : 'Persona'
        dueño de la villa
    tiene_piscina : bool
        indica si la villa tiene piscina
    superficie_terreno : float
        tamaño del terreno en metros cuadrados
    """
    def __init__(self, nombre : str, descripcion: str, habitaciones: list['Habitacion'], precio : float, zona : 'ZonaGeografica', duenyo : 'Persona', tiene_piscina : bool = False, superficie_terreno : float = 0.0) -> None:
        """
        Parámetros
        ----------
        nombre : str
            Nombre de la villa.
        descripcion : str
            Descripción general de la villa.
        habitaciones : list['Habitacion']
            Lista de objetos de tipo Habitacion que forman parte de la villa.
        precio : float
            Precio de venta o alquiler de la villa (en euros).
        zona : ZonaGeografica
            Zona donde está ubicada la villa.
        duenyo : Persona
            Persona propietaria de la villa.
        tiene_piscina : bool, opcional
            Indica si la villa cuenta con piscina. Por defecto es False.
        superficie_terreno : float, opcional
            Tamaño del terreno de la villa en metros cuadrados. Por defecto es 0.0.
        """
        super().__init__(nombre, descripcion, habitaciones, precio, zona, duenyo)
        self.__tiene_piscina = tiene_piscina
        self.__superficie_terreno = superficie_terreno

    @property
    def tiene_piscina(self) -> bool:
        return self.__tiene_piscina

    @property
    def superficie_terreno(self) -> float:
        return self.__superficie_terreno

    def __len__(self):
        return len(self.habitaciones)

    def __str__(self):
        piscina = "Sí" if self.tiene_piscina else "No"
        return (f"Villa: {self.nombre}\n"
                f"Descripción: {self.descripcion}\n"
                f"Nº habitaciones: {len(self)}\n"
                f"Superficie del terreno: {self.superficie_terreno} m²\n"
                f"Piscina: {piscina}\n"
                f"Precio: {self.precio} €\n"
                f"Zona: {self.zona}")