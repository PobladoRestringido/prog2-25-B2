from modelos.usuario.usuario import Usuario

class Administrador(Usuario):

    def __init__(self, nombre, contrasenya):
        super().__init__(nombre, contrasenya, "administrador")
