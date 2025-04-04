from flask import (Flask, jsonify, request)

app = Flask(__name__)
# datos de prueba (base de datos)
inmuebles = [
    {"id": 2, "nombre": "Apartamento en la ciudad", "precio": 150000},
]
# Ruta principal
@app.route("/")
def home():
    return jsonify({"mensaje": "Bienvenido a la API de la inmobiliaria"}), 200

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