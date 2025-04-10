import requests
from API import inmuebles
from serializacion.pickling import cargar_data, guardar_data

BASE_URL = 'http://127.0.0.1:5000/'  # URL de la API Flask

def mostrar_menu() -> int:
    """
    Función para mostrar las opciones al usuario y validar su elección

    El propósito de esta función es mostrar al usuario las opciones que tiene
    en este script de ejemplo, y pedirle que elija una

    Retorna
    -------
    eleccion: int
        - la eleccion del usuario (1-9)
    """

    while True:
        print(f"\n{'-'*10}", 'Menu de Opciones', '-'*10)
        print("1. Ver todos los inmuebles")
        print("2. Ver inmueble por ID")
        print("3. Registrar usuario")
        print("4. Iniciar sesión")
        print("5. Ver comentarios de un inmueble")
        print("6. Escribir comentario sobre un inmueble")
        print("7. Añadir un nuevo inmueble")
        print("8. Actualizar un inmueble")
        print("9. Eliminar un inmueble")
        print("0. Salir")

        try:
            eleccion = int(input('Opcion: '))

            if eleccion in range(10):
                break
            else:
                print('Error: opción inválida')
        except ValueError:
            print('Error: la elección debe ser un número')

    return eleccion

# FUNCIONES PARA LLAMARLAS EN EL BUCLE
def ver_inmuebles() -> None:
    """
    Función para mostrar la información de todos los inmuebles guardados

    Esta función ejemplifica cómo obtener información sobre todos los
    inmuebles guardados en la 'base de datos' de la API. Utiliza el endpoint
    '/inmuebles' y el metodo http GET
    """
    response = requests.get(f"{BASE_URL}inmuebles")
    if response.status_code == 200:
        inmuebles = response.json()
        for inmueble in inmuebles:
            print(inmueble)
    else:
        print("Error al obtener los inmuebles")


def ver_inmueble_por_id() -> str:
    """
    Muestra los detalles de un inmueble a partir de su ID.

    Solicita al usuario el ID de un inmueble y realiza una solicitud GET a la API para obtener la información 
    del inmueble correspondiente. Si la operación es exitosa, devuelve los detalles del inmueble. Si el inmueble 
    no es encontrado, devuelve un mensaje de error.

    Parameteros
    ----------
    Ninguno

    devuelve:
    -str
        Detalles del inmueble si la solicitud es exitosa, o un mensaje de error si no se encuentra el inmueble.
    
    Nota
    -----
    La función realiza una solicitud GET a la API para obtener los detalles de un inmueble usando su ID.
    """
    inmueble_id: str = input("Introduce el ID del inmueble: ")
    response = requests.get(f"{BASE_URL}inmuebles/{inmueble_id}")

    if response.status_code == 200:
        return response.json()  # Devuelve los detalles del inmueble.
    else:
        return "Inmueble no encontrado"


def registrar_usuario() -> str:
    """
    Registra un nuevo usuario en la plataforma.

    Solicita al usuario su nombre de usuario, contraseña y tipo de usuario (comprador, vendedor, administrador).
    Luego, envía esta información a la API para crear una nueva cuenta de usuario. Si la operación es exitosa,
    devuelve un mensaje de confirmación. En caso de error, devuelve el mensaje de error correspondiente.

    Parametros
    ----------
    ninguno

    devuelve:
    -str
        Mensaje que indica si el registro del usuario fue exitoso o si ocurrió un error en el proceso de registro.

    Nota
    -----
    El tipo de usuario debe ser uno de los siguientes: 'comprador', 'vendedor', 'administrador'.
    """
    nombre: str = input("Introduce tu nombre de usuario: ")
    contrasenya: str = input("Introduce tu contraseña: ")
    tipo: str = input("Introduce el tipo de usuario (comprador, vendedor, administrador): ")

    data: dict = {
        'nombre': nombre,
        'contrasenya': contrasenya,
        'tipo': tipo
    }

    response = requests.post(f"{BASE_URL}register", json=data)

    if response.status_code == 201:
        return "Usuario registrado con éxito."
    else:
        return f"Error al registrar el usuario: {response.json().get('error', 'Error desconocido.')}"


def iniciar_sesion() -> str:
    """
    Permite al usuario iniciar sesión con su nombre de usuario y contraseña.

    Esta función solicita al usuario su nombre de usuario y contraseña, y luego envía una solicitud POST
    a la API para autenticar al usuario. Si la autenticación es exitosa, devuelve un mensaje de confirmación.
    En caso de error, devuelve el mensaje de error correspondiente.

    Parametros
    ----------
    ninguno

    devuelve:
    -str
        Mensaje que indica si el inicio de sesión fue exitoso o si ocurrió un error en el proceso de autenticación.

    Nota
    -----
    La función realiza una solicitud POST con el nombre de usuario y la contraseña al endpoint de autenticación de la API.
    """
    nombre: str = input("Introduce tu nombre de usuario: ")
    contrasenya: str = input("Introduce tu contraseña: ")

    data: dict = {
        'nombre': nombre,
        'contrasenya': contrasenya
    }

    response = requests.post(f"{BASE_URL}login", json=data)

    if response.status_code == 200:
        return "Inicio de sesión exitoso."
    else:
        return f"Error al iniciar sesión: {response.json().get('error', 'Error desconocido.')}"


def ver_comentarios_inmueble() -> str:
    """
    Muestra los comentarios asociados a un inmueble.

    Solicita al usuario el ID de un inmueble y realiza una solicitud GET a la API para obtener los comentarios
    de dicho inmueble. Si la operación es exitosa, devuelve los comentarios. Si el inmueble no es encontrado,
    devuelve un mensaje de error.

    Parametros
    ----------
    ninguno

    devuelve:
    str
        Los comentarios del inmueble si la solicitud es exitosa, o un mensaje de error si no se encuentra el inmueble.

    Nota
    -----
    La función realiza una solicitud GET a la API para obtener los comentarios del inmueble especificado por el usuario.
    """
    inmueble_id: str = input("Introduce el ID del inmueble para ver los comentarios: ")
    response = requests.get(f"{BASE_URL}inmueble/{inmueble_id}/comentarios")

    if response.status_code == 200:
        return response.json()  # Devuelve los comentarios como un diccionario o lista de comentarios.
    else:
        return "Inmueble no encontrado"


def escribir_comentario() -> str:
    """
    Permite al usuario escribir un comentario sobre un inmueble y enviarlo a la API.

    Esta función solicita al usuario el ID de un inmueble y un comentario. Si el comentario no está vacío,
    se envía a la API asociada al inmueble correspondiente.

    Si la operación es exitosa, devuelve un mensaje de confirmación. En caso de error, devuelve un mensaje de error.

    Parametros
    ----------
    None

    Returns
    -------
    str
        Mensaje indicando si el comentario fue agregado con éxito o si ocurrió un error.

    Nota
    -----
    El comentario no puede estar vacío, y si es así, la función devuelve un mensaje de error.
    """
    inmueble_id: str = input("Introduce el ID del inmueble sobre el que deseas escribir: ")
    comentario: str = input("Introduce tu comentario: ")

    if not comentario:
        return "El comentario no puede estar vacío."

    # Enviar el comentario a la API
    response = requests.post(f"{BASE_URL}inmueble/{inmueble_id}/escribir", json={"comentario": comentario})

    if response.status_code == 200:
        return "Comentario agregado con éxito!"
    else:
        return f"Error al agregar el comentario: {response.json().get('error')}"


def anyadir_inmueble() -> str:
    """
    Función para añadir un nuevo inmueble solicitando los datos por consola.

    Valida lo siguiente:
    - El ID no debe ser repetido.
    - Los campos de "habitaciones", "precio de venta" y "precio de alquiler" deben ser numéricos.
    - El campo "dueño" no debe ser numérico.

    Parametros
    ------------------
    ninguno

    Devuelve:
    -str
        Un mensaje de confirmación si el inmueble fue añadido correctamente, o un mensaje de error si ocurrió un fallo.
    """
    inmueble_id: str = input("Introduce el ID del nuevo inmueble: ")
    if inmueble_id in inmuebles:
        return f"Error: El inmueble con ID {inmueble_id} ya existe."

    dueño: str = input("Introduce el dueño del inmueble: ")
    if dueño.isdigit():
        return "Error: El campo 'dueño' no puede ser un número."

    habitaciones: str = input("Introduce el número de habitaciones: ")
    if not habitaciones.isdigit():
        return "Error: El campo 'habitaciones' debe ser un número entero."

    zona: str = input("Introduce la zona del inmueble: ")

    precio_venta: str = input("Introduce el precio de venta: ")
    try:
        precio_venta_float = float(precio_venta)
    except ValueError:
        return "Error: El campo 'precio de venta' debe ser un número válido."

    precio_alquiler: str = input("Introduce el precio de alquiler por mes: ")
    try:
        precio_alquiler_float = float(precio_alquiler)
    except ValueError:
        return "Error: El campo 'precio de alquiler' debe ser un número válido."

    data: dict = {
        'dueño': dueño,
        'habitaciones': int(habitaciones),
        'zona': zona,
        'precio de venta': precio_venta_float,
        'precio de alquiler/por mes': precio_alquiler_float
    }

    response = requests.post(f"{BASE_URL}inmuebles/{inmueble_id}", json=data)
    if response.status_code == 200:
        return f"Inmueble {inmueble_id} añadido correctamente."
    else:
        return response.json().get('error', "Error desconocido.")


def actualizar_inmueble() -> str:
    """
    Solicita datos al usuario para actualizar un inmueble existente y envía la solicitud a la API.

    Esta función recoge por consola los nuevos datos de un inmueble (dueño, habitaciones, zona,
    precio de venta y precio de alquiler mensual) e intenta actualizar el inmueble en la API
    utilizando una solicitud PUT.

    Si la actualización es exitosa, devuelve un mensaje indicando que el inmueble ha sido actualizado.
    Si ocurre un error, devuelve el mensaje de error recibido de la API.

    Parametros
    --------------
    ninguno

    Devuelve:
    -str
        Un mensaje de confirmación si el inmueble fue actualizado correctamente, o un mensaje de error si ocurrió un fallo.
    """
    inmueble_id: str = input("Introduce el ID del inmueble a actualizar: ")

    if inmueble_id not in inmuebles:
        return f"Error: No se encuentra un inmueble con ID {inmueble_id}."

    dueño: str = input("Introduce el nuevo dueño: ")

    if dueño.isdigit():
        return "Error: El campo 'dueño' no puede ser un número."

    habitaciones: str = input("Introduce el nuevo número de habitaciones: ")

    if not habitaciones.isdigit():
        return "Error: El campo 'habitaciones' debe ser un número entero."

    zona: str = input("Introduce la nueva zona: ")

    precio_venta: str = input("Introduce el nuevo precio de venta: ")
    try:
        precio_venta_float = float(precio_venta)
    except ValueError:
        return "Error: El campo 'precio de venta' debe ser un número válido."

    precio_alquiler: str = input("Introduce el nuevo precio de alquiler por mes: ")
    try:
        precio_alquiler_float = float(precio_alquiler)
    except ValueError:
        return "Error: El campo 'precio de alquiler' debe ser un número válido."

    data: dict = {
        'dueño': dueño,
        'habitaciones': int(habitaciones),
        'zona': zona,
        'precio de venta': precio_venta_float,
        'precio de alquiler/por mes': precio_alquiler_float
    }

    response = requests.put(f"{BASE_URL}inmuebles/{inmueble_id}", json=data)
    if response.status_code == 200:
        return f"Inmueble {inmueble_id} actualizado correctamente."
    else:
        return response.json().get('error', "Error desconocido.")


def eliminar_inmueble() -> str:
    """
    Elimina un inmueble dado su ID y devuelve un mensaje de confirmación o error.

    Solicita al usuario que ingrese el ID del inmueble que desea eliminar. Luego, realiza una
    solicitud HTTP DELETE a la API para eliminar el inmueble correspondiente.

    Si la eliminación es exitosa, devuelve un mensaje indicando que el inmueble ha sido eliminado.
    Si ocurre un error, devuelve el mensaje de error recibido de la API.

    Parametros
    --------------
    ninguno

    devuelve:
    -str
        Un mensaje de confirmación si el inmueble fue eliminado correctamente, o un mensaje de error si ocurrió un fallo.
    """
    inmueble_id = input("Introduce el ID del inmueble a eliminar: ")
    response = requests.delete(f"{BASE_URL}inmuebles/{inmueble_id}")

    if response.status_code == 200:
        return f"Inmueble {inmueble_id} eliminado correctamente."
    else:
        return response.json().get('error', "Error desconocido.")


def main()-> None:
    """
        Muestra un menú interactivo para que el usuario seleccione una opción de las disponibles.

        En función de la opción seleccionada, ejecuta diferentes funciones que permiten interactuar
        con los inmuebles, usuarios y comentarios en el sistema inmobiliario.

        Las opciones incluyen:
            1. Ver inmuebles disponibles.
            2. Ver un inmueble específico por ID.
            3. Registrar un nuevo usuario.
            4. Iniciar sesión como usuario.
            5. Ver los comentarios de un inmueble.
            6. Escribir un nuevo comentario en un inmueble.
            7. Añadir un nuevo inmueble.
            8. Actualizar un inmueble existente.
            9. Eliminar un inmueble.
            0. Salir de la aplicación.

        El bucle continuará ejecutándose hasta que el usuario seleccione la opción de salir (0).

        Parametros
        -----------
        ninguno

        Devuelve:
        -nada
        """
    while True:
        opcion = mostrar_menu()

        if opcion == 1:
            ver_inmuebles()
        elif opcion == 2:
            ver_inmueble_por_id()
        elif opcion == 3:
            registrar_usuario()
        elif opcion == 4:
            iniciar_sesion()
        elif opcion == 5:
            ver_comentarios_inmueble()
        elif opcion == 6:
            escribir_comentario()  # Nueva opción
        elif opcion == 7:
            anyadir_inmueble()
        elif opcion == 8:
            actualizar_inmueble()
        elif opcion == 9:
            eliminar_inmueble()
        elif opcion == 0:
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()

