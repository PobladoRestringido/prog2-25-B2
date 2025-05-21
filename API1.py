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
from datetime import datetime
# para guardar la fecha de creación de Publicaciones y Comentarios.

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








#--------------------------------------------------de aqui para abajo escribire mis apis--------------


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
        return jsonify({"error": "No tienes permiso para ver este inmueble"}), 403

    inmueble = next((i for i in inmuebles if i.get_id() == id), None)

    if inmueble is None:
        return jsonify({"error": f"Inmueble con ID {id} no encontrado"}), 404

    resultado = {
        "id": inmueble.get_id(),
        "nombre": inmueble.nombre,
        "precio": inmueble.precio,
        "zona": inmueble.zona.nombre,
        "duenyo": inmueble.duenyo.nombre,
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
def eliminar_inmueble(id):
    """
    Elimina el inmueble con el ID dado.
    - Solo administradores o el vendedor dueño pueden eliminarlo.
    """
    rol = get_jwt().get('rol')
    usuario_actual = get_jwt_identity()

    # Buscar inmueble
    inmueble = next((i for i in inmuebles if i.get_id() == id), None)
    if inmueble is None:
        return jsonify({"error": f"Inmueble {id} no encontrado"}), 404

    # Reglas de autorización
    if rol == 'administrador':
        pass  # puede eliminar cualquiera
    elif rol == 'vendedor':
        if inmueble.duenyo.nombre != usuario_actual:
            return jsonify({"error": "No tienes permiso para eliminar este inmueble"}), 403
    else:
        return jsonify({"error": "No tienes permiso para eliminar inmuebles"}), 403

    # Eliminar de la lista
    inmuebles.remove(inmueble)
    return jsonify({"mensaje": f"Inmueble {id} eliminado correctamente"}), 200

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

if __name__ == '__main__':
    app.run(debug=True)
