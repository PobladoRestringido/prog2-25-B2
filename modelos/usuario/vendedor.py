from modelos.usuario.usuario import Usuario

class Vendedor(Usuario):

    def __init__(self, nombre, contrasenya):
        super().__init__(nombre, contrasenya, "vendedor")
