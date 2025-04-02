# auth.py
# Funciones de login y registro

from modelos.usuario import Usuario
from modelos.comprador import Comprador
from modelos.vendedor import Vendedor
from modelos.administrador import Administrador

usuarios_registrados = []

def registrar_usuario(nombre: str, contrasenya: str, tipo: str = "comprador") -> Usuario:
    """
    Registra un nuevo usuario si el nombre no está en uso.
    Parámetros:
        - nombre: nombre de usuario único
        - contrasenya: clave secreta
        - tipo: tipo de usuario (comprador, vendedor, administrador)
    Retorna:
        - instancia de Usuario
    """
    usuario_existente = False

    for u in usuarios_registrados:
        if u.nombre == nombre:
            usuario_existente = True
            break

    if usuario_existente:
        raise ValueError("El nombre de usuario ya está en uso.")

    if tipo == "comprador":
        usuario = Comprador(nombre, contrasenya)
    elif tipo == "vendedor":
        usuario = Vendedor(nombre, contrasenya)
    elif tipo == "administrador":
        usuario = Administrador(nombre, contrasenya)
    else:
        raise ValueError("Tipo de usuario no válido. Debe ser comprador, vendedor o administrador.")

    usuarios_registrados.append(usuario)
    return usuario

def iniciar_sesion(nombre: str, contrasenya: str) -> Usuario:
    """
    Verifica las credenciales de un usuario para iniciar sesión.
    Parámetros:
        - nombre: nombre de usuario
        - contrasenya: clave secreta
    Retorna:
        - instancia de Usuario si es válido, None si no
    """
    for usuario in usuarios_registrados:
        if usuario.nombre == nombre and usuario.verificar_contrasenya(contrasenya):
            return usuario
    raise ValueError("Nombre de usuario o contraseña incorrectos.")
