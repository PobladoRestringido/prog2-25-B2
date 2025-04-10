# inmueble.py
from abc import ABC, abstractmethod

class Inmueble(ABC):
    """
    Clase abstracta que representa un inmueble

    Atributos
    ---------
    nombre : str
        el nombre del inmueble
    descripcion : str
        una descripcion opcional de las caracteristicas del inmueble
    habitaciones : list[Habitacion, ...]
        una lista con las habitaciones que forman parte del inmueble
    precio : float
        el precio de mercado (en euros €) del inmueble
    zona : ZonaGeografica
        la zona geografica a la que pertenece el inmueble
    duenyo : Persona
        persona que posee el inmueble
    """

    contador_inmuebles = 0

    def __init__(self, nombre : str, descripcion : str, habitaciones : list['Habitacion', ...], precio : float, zona : 'ZonaGeografica',  duenyo: 'Persona') -> None:
        """
        Parametros
        ----------
        nombre : str
            el nombre del inmueble
        descripcion : str
            una descripcion opcional de las caracteristicas del inmueble
        habitaciones : list
            una lista con las habitaciones que forman parte del inmueble
        precio : float
            el precio de mercado (en euros €) del inmueble
        zona : ZonaGeografica
            la zona geográfica a la que pertenece el inmueble
        duenyo : Persona
            persona que posee el inmueble
        """
        self.__id : int = type(self).contador_inmuebles
        type(self).contador_inmuebles+=1
        self.__duenyo = duenyo
        self.__habitaciones = habitaciones
        self.__zona = zona
        self.__precio = precio
        self.__descripcion = descripcion
        self.__nombre = nombre


    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @property
    def habitaciones(self) -> list:
        return self.__habitaciones

    @property
    def precio(self) -> float:
        return self.__precio

    @property
    def zona(self) -> 'ZonaGeografica':
        return self.__zona

    @property
    def duenyo(self) -> 'Persona':
        return self.__duenyo

    @precio.setter
    def precio(self, nuevo_precio : float) -> None:
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        self.__precio = nuevo_precio

    @descripcion.setter
    def descripcion(self, nueva_descripcion : str) -> None:
        if not nueva_descripcion:
            raise ValueError("La descripción no puede estar vacía")
        self.__descripcion = nueva_descripcion

    @duenyo.setter
    def duenyo(self, nuevo_duenyo : 'Persona') -> None:
        if nuevo_duenyo is None:
            raise ValueError("El inmueble debe ser de alguien")
        self.__duenyo = nuevo_duenyo