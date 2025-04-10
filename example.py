import requests
from API import inmuebles
from serializacion.pickling import cargar_data, guardar_data

BASE_URL = 'http://127.0.0.1:5000/'  # URL de la API Flask


def mostrar_menu():
    print("\nMenu de Opciones:")
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


# FUNCIONES PARA LLAMARLAS EN EL BUCLE
def ver_inmuebles():
    response = requests.get(f"{BASE_URL}inmuebles")
    if response.status_code == 200:
        inmuebles = response.json()
        for inmueble in inmuebles:
            print(inmueble)
    else:
        print("Error al obtener los inmuebles")


def ver_inmueble_por_id():
    inmueble_id = input("Introduce el ID del inmueble: ")
    response = requests.get(f"{BASE_URL}inmuebles/{inmueble_id}")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Inmueble no encontrado")


def registrar_usuario():
    nombre = input("Introduce tu nombre de usuario: ")
    contrasenya = input("Introduce tu contraseña: ")
    tipo = input("Introduce el tipo de usuario (comprador, vendedor, administrador): ")
    data = {
        'nombre': nombre,
        'contrasenya': contrasenya,
        'tipo': tipo
    }
    response = requests.post(f"{BASE_URL}register", json=data)
    if response.status_code == 201:
        print("Usuario registrado con éxito.")
    else:
        print(response.json().get('error'))


def iniciar_sesion():
    nombre = input("Introduce tu nombre de usuario: ")
    contrasenya = input("Introduce tu contraseña: ")
    data = {
        'nombre': nombre,
        'contrasenya': contrasenya
    }
    response = requests.post(f"{BASE_URL}login", json=data)
    if response.status_code == 200:
        print("Inicio de sesión exitoso.")
    else:
        print(response.json().get('error'))


def ver_comentarios_inmueble():
    inmueble_id = input("Introduce el ID del inmueble para ver los comentarios: ")
    response = requests.get(f"{BASE_URL}inmueble/{inmueble_id}/comentarios")
    if response.status_code == 200:
        print(response.json())
    else:
        print("Inmueble no encontrado")


def escribir_comentario():
    inmueble_id = input("Introduce el ID del inmueble sobre el que deseas escribir: ")
    comentario = input("Introduce tu comentario: ")

    if not comentario:
        print("El comentario no puede estar vacío.")
        return

    # Enviar el comentario a la API
    response = requests.post(f"{BASE_URL}inmueble/{inmueble_id}/escribir", json={"comentario": comentario})

    if response.status_code == 200:
        print("Comentario agregado con éxito!")
    else:
        print("Error al agregar el comentario:", response.json().get('error'))

def anyadir_inmueble():
    inmueble_id = input("Introduce el ID del nuevo inmueble: ")
    dueño = input("Introduce el dueño del inmueble: ")
    habitaciones = input("Introduce el número de habitaciones: ")
    zona = input("Introduce la zona del inmueble: ")
    data = {
        'dueño': dueño,
        'habitaciones': habitaciones,
        'zona': zona
    }
    response = requests.post(f"{BASE_URL}inmuebles/{inmueble_id}", json=data)
    if response.status_code == 200:
        print(f"Inmueble {inmueble_id} añadido correctamente.")
    else:
        print(response.json().get('error'))


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
    str
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
    str
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
        nada
        """
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            ver_inmuebles()
        elif opcion == '2':
            ver_inmueble_por_id()
        elif opcion == '3':
            registrar_usuario()
        elif opcion == '4':
            iniciar_sesion()
        elif opcion == '5':
            ver_comentarios_inmueble()
        elif opcion == '6':
            escribir_comentario()  # Nueva opción
        elif opcion == '7':
            anyadir_inmueble()
        elif opcion == '8':
            actualizar_inmueble()
        elif opcion == '9':
            eliminar_inmueble()
        elif opcion == '0':
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")


if __name__ == "__main__":
    main()

