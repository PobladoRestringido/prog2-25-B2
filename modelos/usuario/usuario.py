# usuario.py
import hashlib

class Usuario:
    """
    Clase que representa a un usuario con nombre y contraseña
    encriptada.

    Descripción:
    -------------
    Esta clase almacena y gestiona la información de un usuario. La
    contraseña se encripta utilizando el algoritmo SHA-256 al momento
    de la inicialización. Se puede obtener el nombre del usuario,
    verificar la contraseña y generar una representación en forma de
    diccionario.

    Atributos:
    -----------
    __nombre : str
        Nombre del usuario.
    __contrasenya : str
        Contraseña encriptada del usuario.

    Métodos:
    --------
    __init__(nombre: str, contrasenya: str)
        Inicializa la instancia del usuario encriptando la contraseña.
    nombre
        Propiedad que retorna el nombre del usuario.
    _encriptar_contrasenya(contrasenya: str) -> str
        Encripta la contraseña usando el algoritmo SHA-256.
    verificar_contrasenya(contrasenya: str) -> bool
        Verifica si la contraseña en texto plano concuerda con la
        contraseña encriptada.
    to_dict() -> dict
        Devuelve un diccionario con la información del usuario (se usará en
        pickling).
    """

    def __init__(self, nombre: str, contrasenya: str,rol:str, contrasenya_en_hash=False):
        """
        Inicializa una nueva instancia de Usuario.

        Parámetros
        ----------
        nombre : str
            Nombre del usuario.
        contrasenya : str
            Contraseña en texto plano que se encriptará.
        """
        self.__nombre = nombre
        self.__rol= rol
        if contrasenya_en_hash:
            self.__contrasenya = contrasenya
        else:
            self.__contrasenya = self._encriptar_contrasenya(contrasenya)

    @property
    def nombre(self):
        """
        Retorna el nombre del usuario.

        Retorno
        -------
        str
            Nombre del usuario.
        """
        return self.__nombre

    def _encriptar_contrasenya(self, contrasenya: str) -> str:
        """
        Encripta la contraseña utilizando SHA-256.

        Parámetros
        ----------
        contrasenya : str
            Contraseña en texto plano.

        Retorno
        -------
        str
            Contraseña encriptada en formato hexadecimal.
        """
        return hashlib.sha256(contrasenya.encode()).hexdigest()

    def verificar_contrasenya(self, contrasenya: str) -> bool:
        """
        Verifica si la contraseña proporcionada es correcta.

        Parámetros
        ----------
        contrasenya : str
            Contraseña en texto plano a verificar.

        Retorno
        -------
        bool
            True si la contraseña es correcta; False en caso contrario.
        """
        return self.__contrasenya == self._encriptar_contrasenya(contrasenya)

    @property
    def rol(self):
        """
            Obtiene el rol del usuario.

            Retorno
            -----------
            str
                El rol asignado al usuario
        """
        return self.__rol

    def to_dict(self) -> dict:
        """
        Devuelve una representación del usuario en forma de diccionario.
        Nota: Normalmente no se incluiría la contraseña por razones de
        seguridad.

        Retorno
        -------
        dict
            Diccionario con las claves "nombre" y "contrasenya".
        """
        return {
            "nombre": self.__nombre,
            "contrasenya": self.__contrasenya,
            "rol":self.__rol
        }


usuarios = {
    "ana": Usuario("ana", "1234", "comprador"),
    "jose": Usuario("jose", "abcd", "vendedor"),
    "admin": Usuario("admin", "admin", "administrador")
}
