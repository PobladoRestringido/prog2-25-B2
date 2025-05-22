from abc import ABC, abstractmethod
from modelos.excepciones import PrecioInvalidoError

class Inmueble(ABC):
    """
    Clase abstracta que representa un inmueble

    Atributos
    ---------
    nombre: str
        el nombre del inmueble
    descripcion: str
        una descripcion opcional de las caracteristicas del inmueble
    habitaciones: list[Habitacion, ...]
        una lista con las habitaciones que forman parte del inmueble
    precio: float
        el precio de mercado (en euros €) del inmueble
    zona: Zona
        la zona geografica a la que pertenece el inmueble

    Metodos
    -------
    __init__(self, nombre: str, descripcion: str,
    habitaciones: list['Habitacion', ...], precio: float, zona: 'Zona')
    -> None
        El constructor de la clase
    """

    contador_inmuebles = 0 # usado para asignar un identificador a cada
    # inmueble

    def __init__(self, duenyo: 'Persona',habitaciones : list['Habitacion', ...],zona :'ZonaGeografica', nombre:str, descripcion:str, precio:float) -> None:
        """
        Metodo constructor de la clase Inmueble

        Parametros
        ----------
        nombre: str
            el nombre del inmueble

        descripcion: str
            una descripcion opcional de las caracteristicas del inmueble

        habitaciones: list
            una lista con las habitaciones que forman parte del inmueble

        precio: float
            el precio de mercado (en euros €) del inmueble

        zona: Zona
            la zona geográfica a la que pertenece el inmueble
        direccion: str
            la direccion del inmueble para buscar en Google Maps
        """
        if precio is None or precio <= 0:
            raise PrecioInvalidoError("El precio debe ser un número positivo", field="precio", value=precio)
        self.__id : int = type(self).contador_inmuebles
        type(self).contador_inmuebles+=1
        self.__duenyo = duenyo
        self.__habitaciones = habitaciones
        self.__zona = zona
        self.__descripcion = descripcion
        self.__nombre= nombre
        self.__precio = precio

    @abstractmethod
    def tipo(self) -> str:
        """
        Método abstracto que define el tipo de inmueble.
        """
        pass

    def __len__(self):
        """
        Implementacion de __len__

        Devuelve
        -------
        : int
            entero que representa el n
        """

        return len(self.__habitaciones)

    def __str__(self) -> str:
        """
        Implementacion de __str__

        Devuelve
        --------
        : str
            un string de varias lineas exponiendo las caracteristicas del
            inmueble
        """

        return (f"Inmueble ID: {self.__id}\n"
                f"Nombre: {self.__nombre}\n"
                f"Descripción: {self.__descripcion}\n"
                f"Dueño: {self.__duenyo.nombre}\n"
                f"Zona: {self.__zona.nombre}\n"
                f"Nº habitaciones: {len(self)}\n"
                f"Precio: {self.__precio} €"
                )

    def get_id(self):
        return self.__id

    @property
    def duenyo(self):
        return self.__duenyo

    @property
    def zona(self):
        return self.__zona

    @property
    def habitaciones(self):
        return self.__habitaciones

    @property
    def nombre(self):
        return self.__nombre

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def precio(self):
        return self.__precio