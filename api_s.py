from flask import Flask, jsonify, request, Response
from modelos.usuario import Usuario

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
@app.route('/usuario', methods=['POST'])
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