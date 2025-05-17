import random
from comentarios_inmu import comentarios_casas, comentarios_pisos,comentarios_usuario
from flask import Flask, jsonify, request, Response
from modelos.usuario.usuario import usuarios
from modelos.usuario.comprador import Comprador
from modelos.usuario.administrador import Administrador
from modelos.usuario.vendedor import Vendedor
from serializacion.pickling import cargar_data
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt

app = Flask(__name__) #Creamos la aplicación Flask
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'  #Clave para autentificar
jwt = JWTManager(app)
usuarios_registrados = []

@app.route('/') #Ruta inicial de la api
def hola():
    """
       Función de inicio de la API. Esta función maneja la ruta raíz y
       devuelve un mensaje de bienvenida.

       Devuélve
       --------------
        -str: Un mensaje de texto dando la bienvenida a la API.
    """
    return 'Bienvenido a la API de inmuebles'

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
            access_token = create_access_token(
                identity=usuario.nombre,
                additional_claims={"rol": usuario.rol}
            )
            return jsonify({"access_token": access_token}), 200

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
    rol = data.get('rol')

    # Validación básica de entrada.
    if not nombre or not contrasenya:
        return jsonify({'error': 'Faltan credenciales.'}), 400

    # Verificar que el nombre de usuario no esté en uso.
    for u in usuarios_registrados:
        if u.nombre == nombre:
            return (jsonify({'error': 'El nombre de usuario ya está en uso.'}),
                    409)

    if rol == "comprador":
        usuario = Comprador(nombre, contrasenya)
    elif rol == "vendedor":
        usuario = Vendedor(nombre, contrasenya)
    elif rol == "administrador":
        usuario = Administrador(nombre, contrasenya)
    else:
        return jsonify({'error': f"Rol de usuario '{rol}' no válido."}), 400

    usuarios_registrados.append(usuario)
    access_token = create_access_token(
        identity=usuario.nombre,
        additional_claims={"rol": usuario.rol}
    )

    return jsonify({'usuario': usuario.to_dict(),'access_token': access_token}), 201

'''
VINCULARLO CON LA BASE DE DATOS FUNCIONAL
'''
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

'''
VINCULARLO CON LA BASE DE DATOS FUNCIONAL
'''
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

'''
VINCULARLO CON LA BASE DE DATOS FUNCIONAL
'''
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

'''
VINCULARLO CON LA BASE DE DATOS FUNCIONAL
'''
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


'''
VINCULARLO CON LA BASE DE DATOS FUNCIONAL
'''
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


