
from flask import Flask, request #Importamos la biblioteca

app = Flask(__name__)

#INMUEBLES DE EJEMPLO,ESTO SE QUITARÁ CUANDO CREEMOS INMUEBLES Y SE IMPORTARÁ
inmuebles = {
    "1": {
        "dueño": "María García",
        "habitacion": 3,
        "zona": "Centro"
    },
    "2": {
        "dueño": "Juan Pérez",
        "habitacion": 2,
        "zona": "Norte"
    },
    "3": {
        "dueño": "Laura Martínez",
        "habitacion": 4,
        "zona": "Sur"
    },
    "4": {
        "dueño": "Carlos López",
        "habitacion": 1,
        "zona": "Este"
    },
    "5": {
        "dueño": "Ana Torres",
        "habitacion": 2,
        "zona": "Oeste"
    }
}



@app.route('/')
def hola():
    return 'Bienvenido a la API de inmuebles'


@app.route('/inmuebles', methods=['GET'])
def get_inmuebles():
    resultado = [{"id": id, **datos} for id, datos in inmuebles.items()]
    return resultado, 200


@app.route('/inmuebles/<id>', methods=['GET'])
def get_inmueble_id(id):
    try:
        inmueble = inmuebles[id]
        return {"id": id, **inmueble}, 200
    except KeyError:
        return f'Inmueble {id} No encontrado', 404


@app.route('/inmuebles/<id>', methods=['POST'])
def añadir_inmuebles(id):
    if id not in inmuebles:
        datos = request.get_json()

        requerido = {"dueño", "habitacion", "zona"}
        if not datos or not requerido.issubset(datos.keys()):
            return {"error": "Faltan campos obligatorios (dueño, habitacion, zona)"}, 400

        inmuebles[id] = {
            "dueño": datos["dueño"],
            "habitacion": datos["habitacion"],
            "zona": datos["zona"]
        }
        return {"mensaje": f"Inmueble {id} añadido correctamente"}, 200
    else:
        return {"error": f"Inmueble {id} ya existe"}, 409

@app.route('/inmuebles/<id>', methods=['PUT'])
def actualizar_inmueble(id):
    if id in inmuebles:

        datos = request.get_json()

        requerido = {"dueño", "habitacion", "zona"}
        if not datos or not requerido.issubset(datos.keys()):
            return {"error": "Faltan campos obligatorios (dueño, habitacion, zona)"}, 400

        inmuebles[id] = {
            "dueño": datos["dueño"],
            "habitacion": datos["habitacion"],
            "zona": datos["zona"]
        }
        return {"mensaje": f"Inmueble {id} actualizado correctamente"}, 200
    else:
        return {"error": f"Inmueble {id} no encontrado"}, 404


@app.route('/inmuebles/<id>', methods=['DELETE'])
def eliminar_inmueble(id):
    if id in inmuebles:
        del inmuebles[id]
        return f'Inmueble {id} eliminado', 200
    else:
        return f'Inmueble {id} No encontrado', 404


if __name__ == '__main__':
    app.run(debug=True)



