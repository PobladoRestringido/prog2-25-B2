import random
import time
from openai import OpenAI
from comentarios_inmu import comentarios_casas, comentarios_pisos
from flask import Flask, request #Importamos la biblioteca

app = Flask(__name__) #Creamos la aplicación Flask

#INMUEBLES DE EJEMPLO,ESTO SE QUITARÁ (dejando un diccionario vacío)CUANDO CREEMOS INMUEBLES Y SE IMPORTARÁ
inmuebles = {
    '1': {
        'dueño': 'María García',
        'habitaciones': 3,
        'zona': 'Centro'
    },
    '2': {
        'dueño': 'Juan Pérez',
        'habitaciones': 2,
        'zona': 'Norte'
    },
    '3': {
        'dueño': 'Laura Martínez',
        'habitaciones': 4,
        'zona': 'Sur'
    },
    '4': {
        'dueño': 'Carlos López',
        'habitaciones': 1,
        'zona': 'Este'
    },
    '5': {
        'dueño': 'Ana Torres',
        'habitaciones': 2,
        'zona': 'Oeste'
    },
    '6': {
        'dueño': 'Raúl Gómez',
        'habitaciones': 3,
        'zona': 'Noreste',
        'tiene_piscina': False,
        'jardin': None
    },
    '7': {
        'dueño': 'Miguel Rodríguez',
        'habitaciones': 5,
        'zona': 'Área metropolitana',
        'tiene_piscina': True,
        'jardin': None
    },
    '8': {
        'dueño': 'Sofia Díaz',
        'habitaciones': 4,
        'zona': 'Noroeste',
        'tiene_piscina': True,
        'jardin': None
    },
    '9': {
        'dueño': 'Laura Martínez',
        'habitaciones': 2,
        'zona': 'Este',
        'tiene_piscina': False,
        'jardin': None
    },
    '10': {
        'dueño': 'Ana Torres' ,
        'habitaciones': 3,
        'zona': 'Sur' ,
        'tiene_piscina': False,
        'jardin': None
    }
}


def deepseek_generatecontent(tipo, habitaciones):
    # Generar un número aleatorio de metros dentro de un rango razonable
    dimensiones = random.randint(50, 150)  # Puedes ajustar el rango según tus necesidades

    # Generar el mensaje para Deepseek, todos los inmuebles son nuevos
    message = client.chat.completions.create(model="deepseek-chat",
        messages=[
                    {"role": "system", "content": "Eres un asistente inmobiliario"},
                    {"role": "user","content": f"Genera un comentario aleatorio acerca de un {tipo} nuevo a la venta. El inmueble tiene {habitaciones} habitaciones y {dimensiones} metros cuadrados. Debe ser un comentario que imite un anuncio inmobiliario de carácter corto, de unos 200 caracteres máximo. No añadas hashtags ni la longitud del mensaje en la respuesta."},
                    ],
                    stream=False)
    return message.choices[0].message.content

client = OpenAI(api_key="sk-02fe7bac884b43478829814148287e55", base_url="https://api.deepseek.com")

@app.route('/')#Ruta inicial de la api
def hola():
    '''
       Función de inicio de la API. Esta función maneja la ruta raíz y
       devuelve un mensaje de bienvenida.

       Devuélve
       --------------
        -str: Un mensaje de texto dando la bienvenida a la API.
    '''
    return 'Bienvenido a la API de inmuebles'


@app.route('/inmuebles', methods=['GET'])  # Ruta para ver todos los inmuebles
def get_inmuebles():
    '''
        Función que obtiene y devuelve la lista de todos los inmuebles registrados.

        Devuelve
        --------------
        -lista[diccionario]: Una lista de diccionarios donde cada diccionario contiene
                        los detalles de un inmueble (id, dueño, habitaciones, zona).

        -código de estado: 200 si la solicitud funciona sin ningún problema.
    '''
    resultado = []
    for id, datos in inmuebles.items():
        inmueble = {'id': id}
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
    -id: int
        ID del inmueble que queramos consultar

    Devuélve
    ------------
    -Diccionario con los detalles del inmueble si existe, si no existe nos salta un error.

    -código de estado: 200 si la solicitud funciona sin ningún problema
                       404 si la solicitud tiene algún problema
    '''

    try:
        inmueble = inmuebles[id]
        inmueble_id = {"id": id}
        for clave, valor in inmueble.items():
            inmueble_id[clave] = valor
        return inmueble_id, 200
    except KeyError:
        return f'Inmueble {id} no encontrado', 404


@app.route('/inmuebles/<id>', methods=['POST'])#Ruta para crear un nuevo inmueble en la base de datos
def añadir_inmuebles(id:int):
    '''
    Función que permite añadir un inmueble que no esté registrado

    Parámetros
    ------------
    -id: int
        ID del inmueble que tendrá el inmueble que añadamos

    Devuelve
    -----------
    -Diccionario con los detalles que introduzcamos del inmueble si existe, si no nos sale un error

    -código de estado: 200 si la solicitud funciona sin ningún problema
                       404 si la solicitud tiene algún problema
    '''

    if id not in inmuebles:
        datos = request.get_json()

        necesario = {'dueño', 'habitaciones', 'zona'}
        if not datos or not necesario.issubset(datos.keys()):
            return {'error': 'Faltan campos obligatorios (dueño, habitaciones, zona)'}, 400

        inmuebles[id] = {
            'dueño': datos['dueño'],
            'habitaciones': datos['habitaciones'],
            'zona': datos['zona']
        }
        return {'mensaje': f'Inmueble {id} añadido correctamente'}, 200
    else:
        return {'error': f'Inmueble {id} ya existe'}, 409

@app.route('/inmuebles/<id>', methods=['PUT'])#Ruta para actualizar los inmuebles
def actualizar_inmueble(id:int):
    '''
    Función para actualizar los inmuebles existentes

    Parámetros
    --------------
    -id: int
        ID del inmueble que queremos actualizar

    Devuélve
    -----------
    -Diccionario con los elementos actualizados del inmueble que existe, si no nos salta un error

    -código de estado: 200 si la solicitud funciona sin ningún problema
                       404 si la solicitud tiene algún problema
    '''

    if id in inmuebles:

        datos = request.get_json()

        requerido = {"dueño", "habitaciones", "zona"}
        if not datos or not requerido.issubset(datos.keys()):
            return {"error": "Faltan campos obligatorios (dueño, habitaciones, zona)"}, 400

        inmuebles[id] = {
            "dueño": datos["dueño"],
            "habitaciones": datos["habitaciones"],
            "zona": datos["zona"]
        }
        return {"mensaje": f"Inmueble {id} actualizado correctamente"}, 200
    else:
        return {"error": f"Inmueble {id} no encontrado"}, 404


@app.route('/inmuebles/<id>', methods=['DELETE'])#Ruta para eliminar un inmueble por su id
def eliminar_inmueble(id:int):
    '''
    Función para eliminar un inmueble existente

    Parámetros
    --------------
    -id: int
        ID del inmueble que queremos borrar

    Devuélve
    ---------------
    -Una tupla que muestra si el inmueble es encontrado y eliminado correctamente o si no se
        ha encontrado

    -código de estado: 200 si la solicitud funciona sin ningún problema
                       404 si la solicitud tiene algún problema
    '''

    if id in inmuebles:
        del inmuebles[id]
        return f'Inmueble {id} eliminado', 200
    else:
        return f'Inmueble {id} No encontrado', 404

@app.route('/inmueble/<id>/comentarios',methods=['GET'])
def mostrar_comentarios(id:int):
    inmueble = inmuebles.get(id)

    if not inmueble:
        return {'error': 'Inmueble no encontrado'}, 404

    if 'jardin' in inmueble or 'tiene_piscina' in inmueble:
        tipo = 'casa'
        comentarios = random.sample(comentarios_casas, 5)
    else:
        tipo = 'piso'
        comentarios = random.sample(comentarios_pisos, 5)

    inmueble = {'id': id}
    for clave, valor in inmueble.items():
        inmueble[clave] = valor

    inmueble['tipo'] = tipo
    inmueble['comentarios'] = comentarios

    return inmueble

ultimo_acceso=0
@app.route('/inmueble/<id>/descripcion',methods=['GET'])
def mostrar_descripcion(id:int):
    global ultimo_acceso


    if id not in inmuebles:
        return {'error': 'Inmueble no encontrado'}, 404


    inmueble = inmuebles[id]
    habitaciones = inmueble.get('habitaciones', 0)
    piscina = inmueble.get('piscina', None)
    jardin = inmueble.get('jardin', None)


    if piscina or jardin:
        tipo = 'casa'
    else:
        tipo = 'piso'


    tiempo_actual = time.time()


    if (tiempo_actual - ultimo_acceso) < 3600:
        tiempo_espera = 3600 - (tiempo_actual - ultimo_acceso)
        return {"error": f"Por favor espera {int(tiempo_espera)} segundos antes de hacer otra solicitud."}, 429


    ultimo_acceso = tiempo_actual


    descripcion = deepseek_generatecontent(tipo, habitaciones)


    return {"descripcion": descripcion}, 200


if __name__ == '__main__':
    app.run(debug=True)



