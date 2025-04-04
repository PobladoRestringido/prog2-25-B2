
from flask import Flask, request #Importamos la biblioteca

app = Flask(__name__) #Creamos la aplicación Flask

#INMUEBLES DE EJEMPLO,ESTO SE QUITARÁ (dejando un diccionario vacío)CUANDO CREEMOS INMUEBLES Y SE IMPORTARÁ
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


@app.route('/')#Ruta inicial de la api
def hola():
    '''
       Función de inicio de la API. Esta función maneja la ruta raíz y
       devuelve un mensaje de bienvenida.

       Devuélve
       --------------
           str: Un mensaje de texto dando la bienvenida a la API.
    '''
    return 'Bienvenido a la API de inmuebles'


@app.route('/inmuebles', methods=['GET'])  # Ruta para ver todos los inmuebles
def get_inmuebles():
    '''
        Función que obtiene y devuelve la lista de todos los inmuebles registrados.

        Devuelve
        --------------
            list[dict]: Una lista de diccionarios donde cada diccionario contiene
                        los detalles de un inmueble (id, dueño, habitaciones, zona).

            código de estado: 200 si la solicitud funciona sin ningún problema.
    '''
    resultado = []
    for id, datos in inmuebles.items():
        inmueble = {"id": id}
        for clave, valor in datos.items():
            inmueble[clave] = valor
        resultado.append(inmueble)

    return resultado, 200


@app.route('/inmuebles/<id>', methods=['GET'])#Ruta para ver un inmueble utilizando su id
def get_inmueble_id(id:int):
    '''
    Función que nos muestra un inmueble por su ID

    Parámetros
    ------------
    id:ID del inmueble que queramos consultar

    Devuélve
    ------------
    Diccionario con los detalles del inmueble si existe, si no existe nos salta un error.
    '''

    try:
        inmueble = inmuebles[id]
        inmueble_id = {"id": id}
        for clave, valor in inmueble.items():
            inmueble_id[clave] = valor
        return inmueble_id, 200
    except KeyError:
        return f'Inmueble {id} no encontrado', 404


@app.route('/inmuebles/<id>', methods=['POST'])#Crea un nuevo inmueble
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



