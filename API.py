from comentarios_inmu import comentarios_casas, comentarios_pisos,comentarios_usuario
from modelos.usuario.comprador import Comprador
from modelos.usuario.administrador import Administrador
from modelos.usuario.vendedor import Vendedor
from modelos.inmueble.piso import Piso
from modelos.inmueble.vivienda_unifamiliar import ViviendaUnifamiliar
from modelos.habitacion.dormitorio import Dormitorio
from modelos.habitacion.cocina import Cocina
from modelos.habitacion.banyo import Banyo
from modelos.habitacion.salon import Salon

from examples.inmuebles_ejemplo import inmuebles
from examples.vendedor_ejemplo import vendedores
from examples.Zonas_ejemplo import zonas

from serializacion.pickling import cargar_data

import random

from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import sqlite3

app = Flask(__name__) #Creamos la aplicación Flask
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'  #Clave para autentificar
jwt = JWTManager(app)
usuarios_registrados = []

@app.route('/') #Ruta inicial de la api
def casa():
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

    # Conectar a la base de datos.
    conn = sqlite3.connect('base_datos/base_datos.db')
    cursor = conn.cursor()

    # Verificar que el usuario no exista.
    cursor.execute("SELECT nombre FROM Usuario WHERE nombre = ?", (nombre,))
    if cursor.fetchone() is not None:
        conn.close()
        return jsonify({'error': 'El nombre de usuario ya está en uso.'}), 409

    # Insertar en la tabla Usuario.
    try:
        cursor.execute(
            "INSERT INTO Usuario (nombre, contrasenya) VALUES (?, ?)",
            (nombre, contrasenya)
        )

        # Insertar en la tabla correspondiente según el rol.
        if rol == "comprador":
            cursor.execute("INSERT INTO Comprador (nombre) VALUES (?)", (nombre,))
        elif rol == "vendedor":
            cursor.execute("INSERT INTO Vendedor (nombre) VALUES (?)", (nombre,))
        elif rol == "administrador":
            cursor.execute("INSERT INTO Administrador (nombre) VALUES (?)", (nombre,))
        else:
            conn.close()
            return jsonify({'error': f"Rol de usuario '{rol}' no válido."}), 400

        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Error al registrar el usuario',
                        'detalle': str(e)}), 500

    conn.close()

    if rol == "comprador":
        usuario = Comprador(nombre, contrasenya)
    elif rol == "vendedor":
        usuario = Vendedor(nombre, contrasenya)
    elif rol == "administrador":
        usuario = Administrador(nombre, contrasenya)
    else:
        return jsonify({'error': f"Rol de usuario '{rol}' no válido."}), 400

    access_token = create_access_token(
        identity=usuario.nombre,
        additional_claims={"rol": usuario.rol}
    )

    return jsonify({'usuario': usuario.to_dict(), 'access_token': access_token}), 201


@app.route('/inmuebles', methods=['GET'])
def get_inmuebles() -> tuple[Response, int]:
    """
    Función que obtiene y devuelve la lista de todos los inmuebles registrados.

    Returns
    -------
    tuple[Response, int]
        JSON con la lista de inmuebles y HTTP 200 si la operación fue correcta.
    """
    return jsonify([inmueble.to_dict() for inmueble in inmuebles]), 200

'''
SQL
'''
@app.route('/inmuebles/<id>', methods=['GET'])#Ruta para ver un inmueble utilizando su id
@jwt_required()
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
    rol = get_jwt().get('rol')

    if rol != 'administrador':
        return jsonify({"error": "Acceso denegado, solo administradores pueden acceder"}), 403

    inmueble = next((inm for inm in inmuebles if inm.get_id() == id), None)
    if inmueble is None:
        return jsonify({"error": "Inmueble no encontrado"}), 404

    return jsonify(inmueble.to_dict()), 200


'''
SQL
'''
@app.route('/inmuebles/<int:id>', methods=['POST'])
@jwt_required()
def anyadir_inmuebles():
    """
    Función que permite añadir un inmueble que no esté registrado


    Devuelve
    -----------
    -Diccionario con los detalles que introduzcamos del inmueble si existe, si no nos sale un error

    -código de estado: 200 si la solicitud funciona sin ningún problema
                       404 si la solicitud tiene algún problema
    """

    rol = get_jwt().get('rol')
    if rol not in ['administrador', 'vendedor']:
        return jsonify({"error": "No tienes permiso para añadir inmuebles"}), 403

    datos = request.get_json()
    tipo = datos.get('tipo')
    if not tipo:
        return jsonify({'error': 'Falta el campo tipo (piso o vivienda_unifamiliar)'}), 400

    # Comprobar campos básicos que todas las viviendas deben tener
    campos_basicos = ['nombre', 'descripcion', 'habitaciones', 'precio', 'zona', 'duenyo']
    if not all(campo in datos for campo in campos_basicos):
        return jsonify({'error': f'Faltan campos básicos: {campos_basicos}'}), 400

    # Buscar la zona y el dueño en tus datos importados, por ejemplo:
    zona = zonas.get(datos['zona'])
    duenyo = None
    for vendedor in vendedores:
        if vendedor.nombre == datos['duenyo']:
            duenyo = vendedor
            break
    if not duenyo:
        return jsonify({'error': 'Dueño no encontrado'}), 400

    # Asume que las habitaciones vienen como lista de dicts con tipo y atributos
    habitaciones_json = datos['habitaciones']
    habitaciones_obj = []
    for hab in habitaciones_json:
        tipo_hab = hab.get('tipo')
        superficie = hab.get('superficie')
        if tipo_hab == 'dormitorio':
            habitaciones_obj.append(
                Dormitorio(superficie, hab.get('tiene_cama', False), hab.get('tiene_lampara', False),
                           hab.get('tiene_mesa_estudio', False)))
        elif tipo_hab == 'cocina':
            habitaciones_obj.append(
                Cocina(superficie, hab.get('tiene_frigorifico', False), hab.get('tiene_horno', False),
                       hab.get('tiene_microondas', False), hab.get('tiene_fregadero', False),
                       hab.get('tiene_mesa', False)))
        elif tipo_hab == 'banyo':
            habitaciones_obj.append(Banyo(superficie, hab.get('tiene_ducha', False), hab.get('tiene_banyera', False),
                                          hab.get('tiene_vater', False), hab.get('tiene_lavabo', True)))
        elif tipo_hab == 'salon':
            habitaciones_obj.append(Salon(superficie, hab.get('tiene_televisor', False), hab.get('tiene_sofa', False),
                                          hab.get('tiene_mesa_recreativa', False)))
        else:
            return jsonify({'error': f'Tipo de habitación {tipo_hab} no reconocido'}), 400

    # Crear el inmueble según tipo
    if tipo == 'piso':
        planta = datos.get('planta')
        ascensor = datos.get('ascensor', False)
        inmueble = Piso(datos['nombre'], habitaciones_obj, zona, datos['descripcion'], datos['precio'], duenyo, planta,
                        ascensor)
    elif tipo == 'vivienda_unifamiliar':
        tiene_piscina = datos.get('tiene_piscina', False)
        jardin = datos.get('jardin', None)
        inmueble = ViviendaUnifamiliar(duenyo, datos['descripcion'], datos['precio'], datos['nombre'], habitaciones_obj,
                                       zona, tiene_piscina, jardin)
    else:
        return jsonify({'error': f'Tipo de inmueble {tipo} no válido'}), 400

    inmuebles.append(inmueble)
    zona.agregar_inmueble(inmueble)

    return jsonify({'mensaje': 'Inmueble añadido correctamente', 'inmueble': inmueble.to_dict()}), 201


'''
SQL
'''
@app.route('/inmuebles/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_inmueble(id: int):
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

    rol = get_jwt().get('rol')
    usuario_actual = get_jwt_identity()

    inmueble = next((i for i in inmuebles if i.get_id() == id), None)
    if inmueble is None:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404

    if rol == 'administrador':
        pass  # administrador puede actualizar cualquier inmueble
    elif rol == 'vendedor':
        if inmueble.duenyo.nombre != usuario_actual:
            return jsonify({"error": "No tienes permiso para modificar este inmueble"}), 403
    else:
        return jsonify({"error": "No tienes permiso para modificar inmuebles"}), 403

    datos = request.get_json()

    # Validar que vienen algunos campos obligatorios, si quieres
    campos_permitidos = {'nombre', 'descripcion', 'precio', 'habitaciones', 'zona'}
    if not datos or not any(key in datos for key in campos_permitidos):
        return jsonify({"error": f"Debes proporcionar al menos uno de los campos: {campos_permitidos}"}), 400

    # Actualizamos solo los campos que se reciban
    if 'nombre' in datos:
        inmueble._Inmueble__nombre = datos['nombre']
    if 'descripcion' in datos:
        inmueble._Inmueble__descripcion = datos['descripcion']
    if 'precio' in datos:
        inmueble._Inmueble__precio = datos['precio']
    if 'habitaciones' in datos:
        inmueble._Inmueble__habitaciones = datos[
            'habitaciones']  # Idealmente convertir a objetos Habitacion si vienen dicts
    if 'zona' in datos:
        inmueble._Inmueble__zona = datos['zona']  # Idealmente asignar un objeto ZonaGeografica

    return jsonify({"mensaje": f"Inmueble {id} actualizado correctamente"}), 200


'''
SQL (AUN NO MODIFICADA)
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

    rol = get_jwt().get('rol')
    if rol not in ['vendedor', 'administrador']:
        return jsonify({"error": "No tienes permiso para eliminar inmuebles"}), 403

    if id in inmuebles:
        del inmuebles[id]
        return jsonify({"mensaje": f"Inmueble {id} eliminado"}), 200
    else:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404

'''
A PARTIR DE AQUI REVISAR EL CODIGO QUE FALTA--------
'''
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