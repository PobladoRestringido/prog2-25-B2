# excepciones.py
from __future__ import annotations
from typing import Any


class ProyectoError(Exception):
    """
    Excepción base de la aplicación Inmobiliaria
    """
    def __init__(self, message: str, *, field: str | None = None, value: Any = None) -> None:
        super().__init__(message)
        self.message =  message
        self.field: str | None = field
        self.value: Any = value

    def __str__(self) -> str:
        base = self.message
        if self.field is not None:
            base += f' | campo: {self.field}'
        if self.value is not None:
            base += f' | valor: {self.value}'
        return base

class DatosInvalidosError(ProyectoError):
    """Los datos suministrados no cumplen los requisitos mínimos"""

class SuperficieInvalidaError(DatosInvalidosError):
    """La superficie de una habitación debe ser > 0 m2"""

class PrecioInvalidoError(DatosInvalidosError):
    """El precio de un inmueble debe ser un número positivo"""


class UsuarioError(ProyectoError):
    """Base para errores de la parte de usuarios"""

class UsuarioNombreInvalidoError(UsuarioError):
    """El nombre de usuario está vacío o solo contiene espacios"""

class UsuarioYaExisteError(UsuarioError):
    """Se intenta registrar un usuario cuyo nombre ya existe"""

class ContrasenyaInvalidaError(UsuarioError):
    """Contraseña vacía o que no cumple requisitos básicos"""

class ContrasemyaIncorrectaError(UsuarioError):
    """La contrasenya proporcionada no coincide con la almacenada"""


class InmuebleError(ProyectoError):
    """Base para errores relativos a inmuebles"""

class InmuebleYaExisteError(InmuebleError):
    """Se intenta añadir un inmueble que ya está registrado"""

class InmuebleNoEncontradoError(InmuebleError):
    """No se encontró el inmueble solicitado"""