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
from modelos.usuario.usuario import usuarios
from modelos.usuario.usuario import Usuario

from examples.inmuebles_ejemplo import inmuebles
from examples.vendedor_ejemplo import vendedores
from examples.Zonas_ejemplo import zonas



import random

from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


app = Flask(__name__) #Creamos la aplicación Flask
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'  #Clave para autentificar
jwt = JWTManager(app)
usuarios_registrados = list(usuarios.values())

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




<<<<<<< HEAD
ARCHIVO_USUARIOS = "usuarios.json"


usuarios_de_prueba = {
    "ana": Usuario("ana", "1234", "comprador"),
    "jose": Usuario("jose", "abcd", "vendedor"),
    "admin": Usuario("admin", "admin", "admin"),
   "laura": Usuario("laura", "pass123", "comprador"),
    "carlos": Usuario("carlos", "venta2025", "vendedor"),
    "maria": Usuario("maria", "secure456", "comprador"),
    "luis": Usuario("luis", "vendiendo123", "vendedor"),
    "sofia": Usuario("sofia", "clave789", "comprador"),
    "raul": Usuario("raul", "adminpass", "admin"),
    "elena": Usuario("elena", "pass321", "vendedor")
}


def guardar_usuarios(usuarios):
    data = {nombre: usuario.to_dict() for nombre, usuario in usuarios.items()}
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def cargar_usuarios():
    """Carga usuarios desde archivo JSON, si no existe devuelve dict vacío"""
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        # En caso de error leyendo el archivo, devolver dict vacío
        return {}

    usuarios = {}
    for nombre, info in data.items():
        usuarios[nombre] = Usuario(
            nombre=info["nombre"],
            contrasenya=info["contrasenya"],
            rol=info["rol"],
            contrasenya_en_hash=True
        )
    return usuarios

# Si no existe el archivo, lo creamos con los usuarios por defecto
if not os.path.exists(ARCHIVO_USUARIOS):
    guardar_usuarios(usuarios_de_prueba)

# Ahora cargamos los usuarios (del archivo ya existente o recién creado)
usuarios_registrados = cargar_usuarios()


app = Flask(__name__) #Creamos la aplicación Flask
app.config['JWT_SECRET_KEY'] = 'clave_super_secreta'  #Clave para autentificar
jwt = JWTManager(app)


@app.route('/') #Ruta inicial de la api
def casa():
    """
       Función de inicio de la API. Esta función maneja la ruta raíz y
       devuelve un mensaje de bienvenida.

       Devuelve
       --------------
        -str: Un mensaje de texto dando la bienvenida a la API.
    """
    return 'Bienvenido a la API de inmuebles'

'''
COPIAR
'''
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')
    rol = data.get('rol')

    if not nombre or not contrasenya or not rol:
        return jsonify({"msg": "Faltan datos para registro"}), 400

    if nombre in usuarios_registrados:
        return jsonify({"msg": "El usuario ya existe"}), 409

    nuevo_usuario = Usuario(nombre, contrasenya, rol)
    usuarios_registrados[nombre] = nuevo_usuario
    guardar_usuarios(usuarios_registrados)

    return jsonify({"msg": f"Usuario {nombre} registrado correctamente"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')

    if not nombre or not contrasenya:
        return jsonify({"msg": "Faltan datos para iniciar sesión"}), 400

    usuario = usuarios_registrados.get(nombre)

    if not usuario or not usuario.verificar_contrasenya(contrasenya):
        return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

    access_token = create_access_token(identity={"nombre": usuario.nombre, "rol": usuario.rol})
    return jsonify(access_token=access_token), 200


@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    identidad = get_jwt_identity()
    return jsonify(logged_in_as=identidad), 200



"""
Los usuarios se guardarán y cargarán en usuarios.json con funciones que leen y escriben en JSON.
Usaremos el método to_dict() de la clase Usuario para guardar el hash de la contraseña.
Cada vez que se registra un usuario, se actualiza el archivo en disco
El login usa los usuarios cargados del archivo.

"""

=======
>>>>>>> 5ca6dcf17e947f79260e0931f521745fc8ceca97




#--------------------------------------------------de aqui para abajo escribire mis apis--------------
'''
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre = data.get('nombre')
    contrasenya = data.get('contrasenya')

    if not nombre or not contrasenya:
        return jsonify({"error": "Faltan credenciales."}), 400

    for usuario in usuarios_registrados:
        if usuario.nombre == nombre and usuario.verificar_contrasenya(contrasenya):
            access_token = create_access_token(
                identity=usuario.nombre,
                additional_claims={"rol": usuario.rol}
            )
            return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Nombre de usuario o contraseña incorrectos."}), 401
'''
@app.route('/inmuebles', methods=['GET'])
def ver_inmuebles():
    """
    Devuelve información detallada de todos los inmuebles
    """
    resultado = []

    for i, inmueble in enumerate(inmuebles, 1):
        inmueble_info = {
            "numero": i,
            "nombre": inmueble.nombre,
            "precio": inmueble.precio,
            "zona": inmueble.zona.nombre,
            "duenyo": inmueble.duenyo.nombre,
            "direccion": inmueble.direccion,
            "habitaciones": [str(h) for h in inmueble.habitaciones]  # asumiendo que son objetos
        }
        resultado.append(inmueble_info)

    return jsonify(resultado), 200

@app.route('/inmuebles/<int:id>', methods=['GET'])
@jwt_required()
def ver_inmueble_por_id(id):
    """
    Devuelve el inmueble con el ID especificado.
    Solo accesible para administradores.
    """
    claims = get_jwt()
    rol = claims.get('rol')

    if rol != 'administrador':
        return jsonify({"error": "No tienes permiso para ver este inmueble(Admin)"}), 403

    inmueble = next((i for i in inmuebles if i.get_id() == id), None)

    if inmueble is None:
        return jsonify({"error": f"Inmueble con ID {id} no encontrado"}), 404

    resultado = {
        "id": inmueble.get_id(),
        "nombre": inmueble.nombre,
        "precio": inmueble.precio,
        "zona": inmueble.zona.nombre,
        "duenyo": inmueble.duenyo.nombre,
        "direccion": inmueble.direccion,
        "habitaciones": [str(h) for h in inmueble.habitaciones]
    }
    return jsonify(resultado), 200

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
@app.route('/inmuebles/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_inmueble(id: int):
    rol = get_jwt().get('rol')
    if rol not in ['vendedor', 'administrador']:
        return jsonify({"error": "No tienes permiso para eliminar inmuebles"}), 403

    print(f"Intentando eliminar inmueble con ID: {id}")
    print("Lista de inmuebles y sus IDs:")
    for inmueble in inmuebles:
        print(f"ID inmueble: {inmueble.get_id()}")

    inmueble_encontrado = None
    for inmueble in inmuebles:
        if inmueble.get_id() == id:
            inmueble_encontrado = inmueble
            break

    if inmueble_encontrado:
        inmuebles.remove(inmueble_encontrado)
        return jsonify({"mensaje": f"Inmueble {id} eliminado"}), 200
    else:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404

@app.route('/inmuebles', methods=['POST'])
@jwt_required()
def anyadir_inmuebles():
    rol = get_jwt().get('rol')
    if rol not in ['administrador', 'vendedor']:
        return jsonify({"error": "No tienes permiso para añadir inmuebles"}), 403

    # Obtener datos JSON
    datos = request.get_json(force=True, silent=True)
    if not datos:
        return jsonify({'error': 'Datos JSON inválidos o no enviados'}), 400

    tipo = datos.get('tipo')
    if not tipo:
        return jsonify({'error': 'Falta el campo tipo (piso o vivienda_unifamiliar)'}), 400

    campos_basicos = ['nombre', 'descripcion', 'habitaciones', 'precio', 'zona', 'duenyo']
    if not all(campo in datos for campo in campos_basicos):
        return jsonify({'error': f'Faltan campos básicos: {campos_basicos}'}), 400

    # Buscar zona y dueño en tus datos
    zona = zonas.get(datos['zona'])
    if not zona:
        return jsonify({'error': f'Zona {datos["zona"]} no encontrada'}), 400

    duenyo = next((v for v in vendedores if v.nombre == datos['duenyo']), None)
    if not duenyo:
        return jsonify({'error': f'Dueño {datos["duenyo"]} no encontrado'}), 400

    # Procesar habitaciones
    habitaciones_json = datos['habitaciones']
    habitaciones_obj = []
    for hab in habitaciones_json:
        tipo_hab = hab.get('tipo')
        superficie = hab.get('superficie')
        if tipo_hab == 'dormitorio':
            habitaciones_obj.append(Dormitorio(superficie,
                                              hab.get('tiene_cama', False),
                                              hab.get('tiene_lampara', False),
                                              hab.get('tiene_mesa_estudio', False)))
        elif tipo_hab == 'cocina':
            habitaciones_obj.append(Cocina(superficie,
                                          hab.get('tiene_frigorifico', False),
                                          hab.get('tiene_horno', False),
                                          hab.get('tiene_microondas', False),
                                          hab.get('tiene_fregadero', False),
                                          hab.get('tiene_mesa', False)))
        elif tipo_hab == 'banyo':
            habitaciones_obj.append(Banyo(superficie,
                                         hab.get('tiene_ducha', False),
                                         hab.get('tiene_banyera', False),
                                         hab.get('tiene_vater', False),
                                         hab.get('tiene_lavabo', True)))
        elif tipo_hab == 'salon':
            habitaciones_obj.append(Salon(superficie,
                                         hab.get('tiene_televisor', False),
                                         hab.get('tiene_sofa', False),
                                         hab.get('tiene_mesa_recreativa', False)))
        else:
            return jsonify({'error': f'Tipo de habitación {tipo_hab} no reconocido'}), 400

    # Crear inmueble según tipo
    if tipo == 'piso':
        planta = datos.get('planta')
        ascensor = datos.get('ascensor', False)
        inmueble = Piso(
            datos['nombre'], 
            habitaciones_obj, 
            zona, 
            datos['descripcion'], 
            datos['precio'],
            duenyo, 
            datos.get('direccion', ''),  # Usa datos['direccion'] si existe, si no, cadena vacía 
            planta, 
            ascensor
            )
    elif tipo == 'vivienda_unifamiliar':
        tiene_piscina = datos.get('tiene_piscina', False)
        jardin = datos.get('jardin', None)
        inmueble = ViviendaUnifamiliar(duenyo, datos['descripcion'], datos['precio'],
                                       datos['nombre'], habitaciones_obj, zona,
                                       tiene_piscina, jardin)
    else:
        return jsonify({'error': f'Tipo de inmueble {tipo} no válido'}), 400

    inmuebles.append(inmueble)
    zona.agregar_inmueble(inmueble)

    return jsonify({'mensaje': 'Inmueble añadido correctamente',
                    'inmueble': inmueble.to_dict()}), 201
@app.route('/inmueble/<int:id>/escribir', methods=['POST'])
def escribir_comentario(id):
    """
    Permite a un usuario escribir un comentario sobre un inmueble.

    Parámetros
    ----------
    id: int
        El identificador del inmueble para el cual se desea agregar el comentario.

    Datos del cuerpo de la solicitud:
    -------------------------------
    comentario: str
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

if __name__ == '__main__':
    app.run(debug=True)
