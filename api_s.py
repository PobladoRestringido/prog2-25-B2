from flask import Flask, jsonify, request, Response
from modelos.usuario import Usuario
from modelos.comprador import Comprador
from modelos.administrador import Administrador
from modelos.vendedor import Vendedor

app = Flask(__name__)
# datos de prueba (base de datos)
inmuebles = [
    {"id": 2, "nombre": "Apartamento en la ciudad", "precio": 150000},
]

# Ruta principal
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido a la API de la inmobiliaria"}), 200


usuarios_registrados : list[Usuario, ...] = []
# inicio sesión
@app.route('/login', methods=['POST'])
def iniciar_sesion() -> tuple[Response, int]:
    """
    Verifica las credenciales de un usuario para iniciar sesión.

    Parámetros (esperados en formato JSON):
    - nombre: str
        Nombre de usuario.
    - contrasenya: str
        Clave secreta del usuario.

    Retorna:
    - JSON con la representación del usuario y HTTP 200 si el log-in es
    correcto.
    - JSON con un mensaje de error y HTTP 401 si el log-in falla.
    - JSON con un mensaje de error y HTTP 400 si faltan las credenciales.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')

    # Verifica que se hayan proporcionado los campos requeridos.
    if not nombre or not contrasenya:
        return jsonify({"error": "Faltan credenciales."}), 400

    for usuario in usuarios_registrados:
        if (usuario.nombre == nombre and
                usuario.verificar_contrasenya(contrasenya)):
            return jsonify(usuario), 200

    return (jsonify({"error": "Nombre de usuario o contraseña incorrectos."}),
            401)


@app.route('/register', methods=['POST'])
def registrar_usuario() -> tuple[Response, int]:
    """
    Registra un nuevo usuario si el nombre no está en uso.

    Parámetros esperados en el JSON:
        - nombre: nombre de usuario único
        - contrasenya: clave secreta
        - tipo: tipo de usuario (comprador, vendedor, administrador)

    Retorna:
        - JSON con la representación del usuario y HTTP 201 si el sign-up
        fue correcto.
        - JSON con un mensaje de error y HTTP 409 si el nombre de usuario
        ya existe.
        - JSON con un mensaje de error y HTTP 400 si se pide crear un tipo
        de usuario inexistente.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')
    tipo = data.get('tipo')

    # Validación básica de entrada.
    if not nombre or not contrasenya:
        return jsonify({'error': 'Faltan credenciales.'}), 400

    # Verificar que el nombre de usuario no esté en uso.
    for u in usuarios_registrados:
        if u.nombre == nombre:
            return (jsonify({'error': 'El nombre de usuario ya está en uso.'}),
                    409)

    if tipo == "comprador":
        usuario = Comprador(nombre, contrasenya)
    elif tipo == "vendedor":
        usuario = Vendedor(nombre, contrasenya)
    elif tipo == "administrador":
        usuario = Administrador(nombre, contrasenya)
    else:
        return jsonify({'error': f"Tipo de usuario '{tipo}' no válido."}), 400

    usuarios_registrados.append(usuario)
    return jsonify({'usuario': usuario}), 201


# Obtener todos los inmuebles
@app.route("/inmuebles", methods=["GET"])
def get_inmuebles():
    return jsonify(inmuebles), 200

# Agregar un nuevo inmueble
@app.route("/inmuebles", methods=["POST"])
def add_inmueble():
    nuevo_inmueble = request.json
    inmuebles.append(nuevo_inmueble)
    return jsonify({"mensaje": "Inmueble agregado", "data": nuevo_inmueble}), 201

# Obtener un inmueble por ID
@app.route("/inmuebles/<int:id>", methods=["GET"])
def get_inmueble(id):
    inmueble = next((i for i in inmuebles if i["id"] == id), None)
    if inmueble:
        return jsonify(inmueble), 200
    return jsonify({"error": "Inmueble no encontrado"}), 404

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)