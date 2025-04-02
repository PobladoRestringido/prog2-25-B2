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
    zona : Zona
        la zona geografica a la que pertenece el inmueble

    Metodos
    -------
    __init__(self, nombre : str, descripcion : str, habitaciones : list['Habitacion', ...], precio : float, zona : 'Zona') -> None
        El constructor de la clase
    """

    contador_inmuebles = 0 # usado para asignar un identificador a cada inmueble

    def __init__(self, duenyo: 'Persona', habitaciones : list['Habitacion', ...], zona : 'ZonaGeografica') -> None:
        """
        Metodo constructor de la clase Inmueble

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

        zona : Zona
            la zona geográfica a la que pertenece el inmueble
        """
        self.__id : int = type(self).contador_inmuebles
        type(self).contador_inmuebles+=1
        self.__duenyo = duenyo
        self.__habitaciones = habitaciones
        self.__zona = zona

    def __len__(self):
        """
        Implementacion de __len__

        Devuelve
        --------
        : int
            entero que representa el n
        """

    def __str__(self) -> str:
        """
        Implementacion de __str__

        Devuelve
        --------
        : str
            un string de varias lineas exponiendo las caracteristicas del inmueble
        """
        return f'Inmueble: {self.__nombre}\nDescripcion: {self.__descripcion}\nNº habitaciones: {}'

'''
'''