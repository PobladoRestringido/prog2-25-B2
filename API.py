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
from openai import OpenAI
import time

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

    Parámetros
    ----------
    - nombre: str
        Nombre de usuario.
    - contrasenya: str
        Clave secreta del usuario.

    Retorna
    -------
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

    # Intentamos conectarnos a la base de datos.
    try:
        with sqlite3.connect('base_datos/base_datos.db') as conn:
            conn.row_factory = sqlite3.Row  # Se extraen las filas como diccionarios.
            cursor = conn.cursor()

            # Ejecutamos la consulta dentro de un bloque try/except
            try:
                cursor.execute("""
                    SELECT u.nombre, u.contrasenya,
                           CASE
                               WHEN c.nombre IS NOT NULL THEN 'Comprador'
                               WHEN v.nombre IS NOT NULL THEN 'Vendedor'
                               WHEN a.nombre IS NOT NULL THEN 'Administrador'
                               ELSE 'Sin rol'
                           END AS rol
                    FROM Usuario u
                    LEFT JOIN Comprador c ON u.nombre = c.nombre
                    LEFT JOIN Vendedor v ON u.nombre = v.nombre
                    LEFT JOIN Administrador a ON u.nombre = a.nombre
                    WHERE u.nombre = ?
                """, (nombre,))
            except sqlite3.Error as exec_err:
                return jsonify({
                    "error": "Error al ejecutar la consulta en la base de datos.",
                    "message": str(exec_err)
                }), 500

            db_row = cursor.fetchone()

    except sqlite3.Error as conn_err:
        return jsonify({
            "error": "Error al conectar con la base de datos.",
            "message": str(conn_err)
        }), 500

    # Comprobamos que el usuario existe.
    if db_row is None:
        return jsonify({'error': 'El nombre de usuario no existe.'}), 400

    # Comprobamos que la contraseña es correcta.
    elif db_row['contrasenya'] != contrasenya:
        return jsonify({'error': 'La contraseña proporcionada es incorrecta.'}), 400

    # Si las credenciales son correctas, devolvemos el token de acceso.
    else:
        access_token = create_access_token(identity=nombre,
                                           additional_claims={"rol": db_row['rol']})
        return jsonify({"access_token": access_token}), 200

@app.route('/register', methods=['POST'])
def registrar_usuario() -> tuple[Response, int]:
    """
    Método que registra un nuevo usuario si el nombre no está ya en uso.

    Parámetros
    ----------
    nombre : str
        nombre de usuario único.
    contrasenya : str
        contraseña encriptada.
    rol : str
        tipo de usuario (comprador, vendedor, administrador).

    Retorna
    -------
    tuple[Response, int]
        JSON con la representación del usuario y el código HTTP
        correspondiente.
    """

    # primero extraemos la data del json.
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')
    rol = data.get('rol')

    # a continuación validamos la entrada.
    if not nombre or not contrasenya or not rol:
        return jsonify({'error': 'Faltan credenciales.'}), 400

    if rol not in ('comprador', 'vendedor', 'administrador'):
        return jsonify({'error': 'Tipo usuario no válido.'}), 400

    # Conectar a la base de datos.
    with sqlite3.connect('base_datos/base_datos.db') as conn:
        cursor = conn.cursor()

        # Verificar que el usuario no exista ya.
        cursor.execute("SELECT nombre FROM Usuario WHERE nombre = ?",(nombre,))
        if cursor.fetchone() is not None:
            return jsonify({'error': 'El nombre de usuario ya está en uso.'}), 400

        # Llegados a este punto las creedenciales son válidas, por lo que
        # insertamos al nuevo usuario en la DB.
        try:
            cursor.execute(
                "INSERT INTO Usuario (nombre, contrasenya) VALUES (?, ?)",
                (nombre, contrasenya)
            )

            # Insertar en la tabla correspondiente según el ``rol``.
            if rol == "comprador":
                cursor.execute("INSERT INTO Comprador (nombre) VALUES (?)",
                               (nombre,))
            elif rol == "vendedor":
                cursor.execute("INSERT INTO Vendedor (nombre) VALUES (?)",
                               (nombre,))
            elif rol == "administrador":
                cursor.execute("INSERT INTO Administrador (nombre) VALUES (?)",
                               (nombre,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            conn.close()
            return jsonify({'error': str(e)}), 500

    # Finalmente, creamos y devolvemos la representación json del usuario
    # creado.
    usuario = Comprador(nombre, contrasenya) if (rol ==
                                                 'comprador') else (
        Vendedor(nombre, contrasenya)) if rol == 'vendedor' else (
        Administrador(nombre, contrasenya))

    access_token = create_access_token(
        identity=usuario.nombre,
        additional_claims={"rol": usuario.rol}
    )

    return jsonify({'usuario': usuario.to_dict(), 'access_token': access_token}), 201


@app.route('/inmuebles', methods=['GET'])
def get_inmuebles() -> tuple[Response, int]:
    """
    Función que obtiene y devuelve la lista de todos los inmuebles registrados.

    Returna
    -------
    tuple[Response, int]
        JSON con la lista de inmuebles (como diccionarios) y HTTP 200 si la
        operación fue correcta.
        Si hubo algún error durante la conexión a la base de
        datos, devuelve HTTP 500.
    """
    try:
        with sqlite3.connect('base_datos/base_datos.db') as conn:
            cursor = conn.cursor()

            conn.row_factory = sqlite3.Row # esta línea hace que las filas
            # de la base de datos se extraigan como diccionarios. Por
            # defecto serían tuplas.

            # Extraemos los inmuebles de la base de datos
            inmuebles_list = cursor.execute("SELECT * FROM Inmueble").fetchall()

        return jsonify(inmuebles_list), 200

    except Exception as e:
        # Se captura cualquier error que ocurra y se retorna con HTTP 500
        return jsonify({'error': str(e)}), 500

@app.route('/inmuebles/<id>', methods=['GET']) # Ruta para ver un inmueble
# utilizando su id
@jwt_required()
def get_inmueble_id(id: int) -> tuple[Response, int]:
    """
    Recupera los detalles de un inmueble específico por su ID desde la base de datos.

    Solo los usuarios con rol de 'administrador' pueden acceder a esta ruta.
    Si el inmueble no se encuentra, se devuelve un error 404.
    En caso de error de conexión u otro fallo inesperado, se devuelve un error 500.

    Parameters
    ----------
    id: int
        Identificador único del inmueble a consultar.

    Returns
    -------
    tuple[Response, int]
        - Si el usuario tiene permisos y el inmueble existe:
            JSON con los datos del inmueble y código de estado HTTP 200.
        - Si el usuario no tiene permisos:
            JSON con mensaje de error y código HTTP 403.
        - Si el inmueble no existe:
            JSON con mensaje de error y código HTTP 404.
        - Si ocurre un error interno:
            JSON con mensaje de error y código HTTP 500.
    """
    rol = get_jwt().get('rol').lower()
    if rol != 'administrador':
        return jsonify({"error": "Acceso denegado, solo administradores pueden acceder"}), 403

    try:
        with sqlite3.connect('base_datos/base_datos.db') as conn:
            conn.row_factory = sqlite3.Row # esto hace que las filas de la
            # db se extraigan directamente como diccionarios.
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM Inmueble WHERE id = ?", (id,))
            row = cursor.fetchone()

            if row is None:
                return jsonify({"error": "Inmueble no encontrado"}), 404

            return jsonify(row), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

    @app.route('/inmuebles/<int:id>', methods=['POST'])
    @jwt_required()
    def anadir_inmueble(id):
        rol = get_jwt().get('rol')
        if rol != 'administrador' and rol != 'vendedor':
            return jsonify({"error": "No tienes permiso para añadir inmuebles"}), 403

        datos = request.get_json()

        # Comprobar tipo de inmueble
        if 'tipo' not in datos:
            return jsonify({'error': 'Falta el campo tipo (piso o vivienda_unifamiliar)'}), 400
        tipo = datos['tipo']

        # Comprobar campos básicos uno por uno
        if 'nombre' not in datos or 'descripcion' not in datos or 'habitaciones' not in datos or \
                'precio' not in datos or 'zona' not in datos or 'duenyo' not in datos:
            return jsonify({'error': 'Faltan campos básicos'}), 400

        # Buscar la zona
        nombre_zona = datos['zona']
        if nombre_zona in zonas:
            zona = zonas[nombre_zona]
        else:
            return jsonify({'error': 'Zona no encontrada'}), 400

        # Buscar el dueño
        duenyo = None
        for vendedor in vendedores:
            if vendedor.nombre == datos['duenyo']:
                duenyo = vendedor
                break
        if duenyo is None:
            return jsonify({'error': 'Dueño no encontrado'}), 400

        # Crear lista de habitaciones
        habitaciones_obj = []
        for hab in datos['habitaciones']:
            tipo_hab = hab['tipo']
            superficie = hab['superficie']

            if tipo_hab == 'dormitorio':
                habitaciones_obj.append(Dormitorio(superficie, hab.get('tiene_cama', False),
                                                   hab.get('tiene_lampara', False),
                                                   hab.get('tiene_mesa_estudio', False)))
            elif tipo_hab == 'cocina':
                habitaciones_obj.append(Cocina(superficie, hab.get('tiene_frigorifico', False),
                                               hab.get('tiene_horno', False),
                                               hab.get('tiene_microondas', False),
                                               hab.get('tiene_fregadero', False),
                                               hab.get('tiene_mesa', False)))
            elif tipo_hab == 'banyo':
                habitaciones_obj.append(Banyo(superficie, hab.get('tiene_ducha', False),
                                              hab.get('tiene_banyera', False),
                                              hab.get('tiene_vater', False),
                                              hab.get('tiene_lavabo', True)))
            elif tipo_hab == 'salon':
                habitaciones_obj.append(Salon(superficie, hab.get('tiene_televisor', False),
                                              hab.get('tiene_sofa', False),
                                              hab.get('tiene_mesa_recreativa', False)))
            else:
                return jsonify({'error': 'Tipo de habitación no reconocido'}), 400

        # Crear el inmueble
        if tipo == 'piso':
            planta = datos.get('planta')
            ascensor = datos.get('ascensor', False)
            inmueble = Piso(datos['nombre'], habitaciones_obj, zona, datos['descripcion'], datos['precio'],
                            duenyo, planta, ascensor)
        elif tipo == 'vivienda_unifamiliar':
            piscina = datos.get('tiene_piscina', False)
            jardin = datos.get('jardin')
            inmueble = ViviendaUnifamiliar(duenyo, datos['descripcion'], datos['precio'], datos['nombre'],
                                           habitaciones_obj, zona, piscina, jardin)
        else:
            return jsonify({'error': 'Tipo de inmueble no válido'}), 400

        # Guardar el inmueble
        inmuebles.append(inmueble)
        zona.agregar_inmueble(inmueble)

        return jsonify({
            'mensaje': 'Inmueble añadido correctamente',
            'inmueble': inmueble.to_dict()
        }), 201


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
@jwt_required()
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
def mostrar_comentarios(id: int) -> tuple[Response, int]:
    """
    Muestra los comentarios asociados a un inmueble basado en su tipo (casa o piso).

    Según el tipo de inmueble (determinado por la presencia de jardín o piscina),
    se seleccionan 5 comentarios aleatorios de la lista correspondiente.

    Parámetros
    ----------
    id: int
        El identificador único del inmueble.

    Excepciones
    ------------
    Si el inmueble con el ID proporcionado no existe, se genera una respuesta de error con un código 404.
    Si ocurre un error con la base de datos, se genera un error 500.

    Devuelve
    --------
    tuple
        Una tupla que contiene:
        - un diccionario con los detalles del inmueble, incluyendo su tipo y los comentarios aleatorios seleccionados.
        - un código de estado HTTP (200 si todo está correcto, 404 si no se encuentra el inmueble, 500 en caso de error).
    """
    try:
        with sqlite3.connect('base_datos/base_datos.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM inmuebles WHERE id = ?", (id,))
            inmueble = cursor.fetchone()

            if not inmueble:
                return jsonify({"error": "Inmueble no encontrado."}), 404

            tipo = 'casa' if inmueble['jardin'] or inmueble['tiene_piscina'] else 'piso'


            cursor.execute(
                "SELECT texto FROM comentarios WHERE tipo = ? ORDER BY RANDOM() LIMIT 5",
                (tipo,)
            )
            comentarios = [row['texto'] for row in cursor.fetchall()]

            cursor.execute(
                "SELECT texto FROM comentarios_usuario WHERE inmueble_id = ?",
                (id,)
            )
            comentarios_usuario = [row['texto'] for row in cursor.fetchall()]

            respuesta = {
                "id": inmueble['id'],
                "tipo": tipo,
                "comentarios": comentarios,
                "comentarios_usuario": comentarios_usuario
            }

            return jsonify(respuesta), 200

    except sqlite3.Error as err:
        return jsonify({
            "error": "Error al acceder a la base de datos.",
            "message": str(err)
        }), 500

'''
Cuando se termine implemento mi api de descripciones mediante IA
'''

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

app.config['ULTIMO_TIEMPO_DESCRIPCION'] = 0
@app.route('/inmueble/<id>/descripcion',methods=['GET'])
def mostrar_descripcion(id:int):


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

        # Comprobación de tiempo de espera
        tiempo_actual = time.time()
        ultimo_tiempo = app.config.get('ULTIMO_TIEMPO_DESCRIPCION', 0)
        espera = 600  # 10 minutos = 600 segundos

        if (tiempo_actual - ultimo_tiempo) < espera:
            tiempo_restante = int(espera - (tiempo_actual - ultimo_tiempo))
            return jsonify(
                {"error": f"Debes esperar {tiempo_restante} segundos antes de generar otra descripción."}), 429

        # Actualizar el tiempo de última generación
        app.config['ULTIMO_TIEMPO_DESCRIPCION'] = tiempo_actual


    descripcion = deepseek_generatecontent(tipo, habitaciones)


    return {"descripcion": descripcion}, 200

if __name__ == '__main__':
    app.run(debug=True)