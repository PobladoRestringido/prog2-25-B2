import hashlib

import hashlib

class Usuario:
    def __init__(self, nombre: str, contrasenya: str):
        self.__nombre = nombre
        self.__contrasenya = self._encriptar_contrasenya(contrasenya)

    @property
    def nombre(self):
        return self.__nombre

    def _encriptar_contrasenya(self, contrasenya: str) -> str:
        return hashlib.sha256(contrasenya.encode()).hexdigest()

    def verificar_contrasenya(self, contrasenya: str) -> bool:
        return self.__contrasenya == self._encriptar_contrasenya(contrasenya)

    def to_dict(self) -> dict:
        """
        Devuelve una representación en diccionario del usuario.
        Nota: Por razones de seguridad, normalmente NO incluiríamos la
        contraseña.
        """
        return {
            "nombre": self.__nombre,
            "contrasenya": self.__contrasenya
        }
