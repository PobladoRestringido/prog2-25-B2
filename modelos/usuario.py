import hashlib

class Usuario:
    """
    Clase base que representa un usuario del sistema.

    Atributos privados:
        __nombre (str): Nombre del usuario.
        __contrasenya (str): Contraseña del usuario encriptada con SHA-256.

    Métodos:
        __init__(nombre, contrasenya): Constructor que crea un usuario con nombre y contraseña encriptada.
        nombre: Propiedad para acceder al nombre del usuario.
        _encriptar_contrasenya(contrasenya): Encriptar la contraseña usando SHA-256.
        verificar_contrasenya(contrasenya): Verifica si la contraseña ingresada coincide con la almacenada.
    """

    def __init__(self, nombre: str, contrasenya: str):
        """
        Inicializa una nueva instancia de Usuario con nombre y contraseña.

        Parámetros:
            nombre (str): Nombre del usuario.
            contrasenya (str): Contraseña en texto plano, que será encriptada.
        """
        self.__nombre = nombre
        self.__contrasenya = self._encriptar_contrasenya(contrasenya)

    @property
    def nombre(self):
        """
        Devuelve el nombre del usuario.
        """
        return self.__nombre

    def _encriptar_contrasenya(self, contrasenya: str) -> str:
        """
        Encripta una contraseña usando el algoritmo SHA-256.

        Parámetros:
            contrasenya (str): Contraseña en texto plano.

        Retorna:
            str: Contraseña encriptada.
        """
        return hashlib.sha256(contrasenya.encode()).hexdigest()

    def verificar_contrasenya(self, contrasenya: str) -> bool:
        """
        Verifica si una contraseña proporcionada coincide con la contraseña encriptada del usuario.

        Parámetros:
            contrasenya (str): Contraseña en texto plano a verificar.

        Retorna:
            bool: True si la contraseña es correcta, False en caso contrario.
        """
        return self.__contrasenya == self._encriptar_contrasenya(contrasenya)
