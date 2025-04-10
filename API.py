import random
from comentarios_inmu import comentarios_casas, comentarios_pisos,comentarios_usuario
from flask import Flask, jsonify, request, Response
from modelos.usuario import Usuario
from modelos.comprador import Comprador
from modelos.administrador import Administrador
from modelos.vendedor import Vendedor
from serializacion.pickling import cargar_data, guardar_data

app = Flask(__name__) #Creamos la aplicación Flask

#INMUEBLES DE EJEMPLO,ESTO SE QUITARÁ (dejando un diccionario vacío) CUANDO CREEMOS INMUEBLES Y SE IMPORTARÁ
inmuebles = {
    '1': {
        'dueño': 'María García',
        'habitaciones': 3,
        'zona': 'Centro',
        'Precio de venta': 350.000,
        'Precio de alquiler/por mes': 500
    },
    '2': {
        'dueño': 'Juan Pérez',
        'habitaciones': 2,
        'zona': 'Norte',
        'Precio de venta': 200.000,
        'Precio de alquiler/por mes': 350
    },
    '3': {
        'dueño': 'Laura Martínez',
        'habitaciones': 4,
        'zona': 'Sur',
        'Precio de venta': 250.000,
        'Precio de alquiler/por mes': 425
    },
    '4': {
        'dueño': 'Carlos López',
        'habitaciones': 1,
        'zona': 'Este',
        'Precio de venta': 375.000,
        'Precio de alquiler/por mes': 360
    },
    '5': {
        'dueño': 'Ana Torres',
        'habitaciones': 2,
        'zona': 'Oeste',
        'Precio de venta': 440.000,
        'Precio de alquiler/por mes': 490
    },
    '6': {
        'dueño': 'Raúl Gómez',
        'habitaciones': 3,
        'zona': 'Noreste',
        'tiene_piscina': False,
        'jardin': None,
        'Precio de venta': 240.000,
        'Precio de alquiler/por mes': 480
    },
    '7': {
        'dueño': 'Miguel Rodríguez',
        'habitaciones': 5,
        'zona': 'Área metropolitana',
        'tiene_piscina': True,
        'jardin': None,
        'Precio de venta': 490.000,
        'Precio de alquiler/por mes': 600
    },
    '8': {
        'dueño': 'Sofia Díaz',
        'habitaciones': 4,
        'zona': 'Noroeste',
        'tiene_piscina': True,
        'jardin': None,
        'Precio de venta': 460.000,
        'Precio de alquiler/por mes': 500
    },
    '9': {
        'dueño': 'Laura Martínez',
        'habitaciones': 2,
        'zona': 'Este',
        'tiene_piscina': False,
        'jardin': None,
        'Precio de venta': 300.000,
        'Precio de alquiler/por mes': 400
    },
    '10': {
        'dueño': 'Ana Torres' ,
        'habitaciones': 3,
        'zona': 'Sur' ,
        'tiene_piscina': False,
        'jardin': None,
        'Precio de venta': 390.000,
        'Precio de alquiler/por mes': 470
    },
    '11': {
        'dueño': 'Lucía Fernández',
        'habitaciones': 2,
        'zona': 'Centro',
        'tiene_piscina': False,
        'jardin': True,
        'Precio de venta': 310_000,
        'Precio de alquiler/por mes': 450
    },
    '12': {
        'dueño': 'Andrés Morales',
        'habitaciones': 4,
        'zona': 'Sur',
        'tiene_piscina': True,
        'jardin': True,
        'Precio de venta': 520_000,
        'Precio de alquiler/por mes': 620
    },
    '13': {
        'dueño': 'Nuria Blanco',
        'habitaciones': 1,
        'zona': 'Norte',
        'tiene_piscina': False,
        'jardin': False,
        'Precio de venta': 190_000,
        'Precio de alquiler/por mes': 320
    },
    '14': {
        'dueño': 'David Ruiz',
        'habitaciones': 3,
        'zona': 'Centro',
        'tiene_piscina': False,
        'jardin': True,
        'Precio de venta': 340_000,
        'Precio de alquiler/por mes': 490
    },
    '15': {
        'dueño': 'Elena Navarro',
        'habitaciones': 5,
        'zona': 'Área metropolitana',
        'tiene_piscina': True,
        'jardin': True,
        'Precio de venta': 610_000,
        'Precio de alquiler/por mes': 750
    },
    '16': {
        'dueño': 'Mario Jiménez',
        'habitaciones': 2,
        'zona': 'Noroeste',
        'tiene_piscina': False,
        'jardin': True,
        'Precio de venta': 280_000,
        'Precio de alquiler/por mes': 410
    },
    '17': {
        'dueño': 'Sara Castillo',
        'habitaciones': 3,
        'zona': 'Este',
        'tiene_piscina': True,
        'jardin': False,
        'Precio de venta': 370_000,
        'Precio de alquiler/por mes': 460
    },
    '18': {
        'dueño': 'Víctor Romero',
        'habitaciones': 4,
        'zona': 'Oeste',
        'tiene_piscina': True,
        'jardin': True,
        'Precio de venta': 490_000,
        'Precio de alquiler/por mes': 630
    },
    '19': {
        'dueño': 'Patricia Vega',
        'habitaciones': 1,
        'zona': 'Noreste',
        'tiene_piscina': False,
        'jardin': False,
        'Precio de venta': 210_000,
        'Precio de alquiler/por mes': 330
    },
    '20': {
        'dueño': 'Jorge Delgado',
        'habitaciones': 3,
        'zona': 'Sur',
        'tiene_piscina': False,
        'jardin': True,
        'Precio de venta': 355_000,
        'Precio de alquiler/por mes': 490
    }
}

@app.route('/')#Ruta inicial de la api
def hola():
    """
       Función de inicio de la API. Esta función maneja la ruta raíz y
       devuelve un mensaje de bienvenida.

       Devuélve
       --------------
        -str: Un mensaje de texto dando la bienvenida a la API.
    """
    return 'Bienvenido a la API de inmuebles'

usuarios_registrados : list[Usuario, ...] = [] # todo implementar pickling
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


@app.route('/inmuebles', methods=['GET'])
def get_inmuebles() -> tuple[Response, int]:
    """
    Función que obtiene y devuelve la lista de todos los inmuebles registrados.

    Returns
    -------
    tuple[Response, int]
        JSON con la lista de inmuebles y HTTP 200 si la operación fue correcta.
    """
    data = cargar_data()  # de-serializamos los inmuebles
    return jsonify(data['inmuebles']), 200

@app.route('/inmuebles/<id>', methods=['GET'])#Ruta para ver un inmueble utilizando su id
def get_inmueble_id(id:int):
    """
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
    """

    try:
        inmueble = inmuebles[id]
        inmueble_id = {"id": id}
        for clave, valor in inmueble.items():
            inmueble_id[clave] = valor
        return jsonify(inmueble_id), 200
    except KeyError:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404


@app.route('/inmuebles/<id>', methods=['POST'])#Ruta para crear un nuevo inmueble en la base de datos
def anyadir_inmuebles(id:int):
    """
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
    """

    if id not in inmuebles:
        datos = request.get_json()

        necesario = {'dueño', 'habitaciones', 'zona'}
        if not datos or not necesario.issubset(datos.keys()):
            return jsonify({'error': 'Faltan campos obligatorios (dueño, habitaciones, zona)'}), 400

        inmuebles[id] = {
            'dueño': datos['dueño'],
            'habitaciones': datos['habitaciones'],
            'zona': datos['zona']
        }
        return jsonify({'mensaje': f'Inmueble {id} añadido correctamente'}), 200
    else:
        return jsonify({'error': f'Inmueble {id} ya existe'}), 409

@app.route('/inmuebles/<id>', methods=['PUT'])#Ruta para actualizar los inmuebles
def actualizar_inmueble(id:int):
    """
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
    """

    if id in inmuebles:

        datos = request.get_json()

        requerido = {"dueño", "habitaciones", "zona"}
        if not datos or not requerido.issubset(datos.keys()):
            return jsonify({"error": "Faltan campos obligatorios (dueño, habitaciones, zona)"}), 400

        inmuebles[id] = {
            "dueño": datos["dueño"],
            "habitaciones": datos["habitaciones"],
            "zona": datos["zona"]
        }
        return jsonify({"mensaje": f"Inmueble {id} actualizado correctamente"}), 200
    else:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404


@app.route('/inmuebles/<id>', methods=['DELETE'])#Ruta para eliminar un inmueble por su id
def eliminar_inmueble(id:int):
    """
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
    """

    if id in inmuebles:
        del inmuebles[id]
        return jsonify({"mensaje": f'Inmueble {id} eliminado'}), 200
    else:
        return jsonify({"error": f'Inmueble {id} no encontrado'}), 404


@app.route('/inmueble/<int:id>/escribir', methods=['POST'])
def escribir_comentario(id):
    """
    Permite a un usuario escribir un comentario sobre un inmueble.

    Parámetros
    ----------
    id : int
        El identificador del inmueble para el cual se desea agregar el comentario.

    Datos del cuerpo de la solicitud:
    -------------------------------
    comentario : str
        El comentario que el usuario desea dejar.

    Respuesta
    ---------
    Se devuelve una confirmación de que el comentario fue agregado correctamente.
    """
    # Obtener el comentario del cuerpo de la solicitud
    comentario = request.json.get("comentario")

    if not comentario:
        return jsonify({"error": "Comentario no puede estar vacío"}), 400

    # Guardar el comentario en la lista (con el ID del inmueble)
    comentarios_usuario.append({"inmueble_id": id, "comentario": comentario})

    return jsonify({"message": "Comentario agregado con éxito!"}), 200

@app.route('/inmueble/<id>/comentarios',methods=['GET'])
def mostrar_comentarios(id:int):
    """
       Muestra los comentarios asociados a un inmueble basado en su tipo (casa o piso).

       Según el tipo de inmueble (determinado por la presencia de ciertas características como jardín o piscina),
       se seleccionan 5 comentarios aleatorios de la lista correspondiente.

       Parámetros
       ----------
       id : int
           El identificador único del inmueble.

       Excepciones
       ------------
       Si el inmueble con el ID proporcionado no existe, se genera una respuesta de error con un código 404.

       Devuelve
       --------
       tuple
           Una tupla que contiene:
           - un diccionario con los detalles del inmueble, incluyendo su tipo y los comentarios aleatorios seleccionados.
           - un código de estado HTTP (200 si todo está correcto, 404 si no se encuentra el inmueble).

       """
    inmueble = inmuebles.get(id)

    if not inmueble:
        return jsonify({"error": "Inmueble no encontrado"}), 404

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
    inmueble['comentarios_usuario']=comentarios_usuario

    return jsonify(inmueble), 200

if __name__ == '__main__':
    app.run(debug=True)


