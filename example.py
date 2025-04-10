import requests
from API import inmuebles
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


def anyadir_inmueble() -> None:
    """
    Función para añadir un nuevo inmueble solicitando los datos por consola.

    Valida lo siguiente:
    - El ID no debe ser repetido.
    - Los campos de "habitaciones", "precio de venta" y "precio de alquiler" deben ser numéricos.
    - El campo "dueño" no debe ser numérico.
    """
    inmueble_id: str = input("Introduce el ID del nuevo inmueble: ")

    # Validar que el ID no se repita
    if inmueble_id in inmuebles:
        print(f"Error: El inmueble con ID {inmueble_id} ya existe.")
        return

    dueño: str = input("Introduce el dueño del inmueble: ")

    # Validar que el dueño no sea un número
    if dueño.isdigit():
        print("Error: El campo 'dueño' no puede ser un número.")
        return

    habitaciones: str = input("Introduce el número de habitaciones: ")

    # Validar que las habitaciones sean un número entero
    if not habitaciones.isdigit():
        print("Error: El campo 'habitaciones' debe ser un número entero.")
        return

    zona: str = input("Introduce la zona del inmueble: ")

    # Validar que el precio de venta sea un número flotante o entero
    precio_venta: str = input("Introduce el precio de venta: ")
    if not precio_venta.replace('.', '', 1).isdigit() or precio_venta.count('.') > 1:
        print("Error: El campo 'precio de venta' debe ser un número válido.")
        return

    # Validar que el precio de alquiler sea un número flotante o entero
    precio_alquiler: str = input("Introduce el precio de alquiler por mes: ")
    if not precio_alquiler.replace('.', '', 1).isdigit() or precio_alquiler.count('.') > 1:
        print("Error: El campo 'precio de alquiler' debe ser un número válido.")
        return

    # Crear el diccionario con los datos del inmueble
    data: dict = {
        'dueño': dueño,
        'habitaciones': int(habitaciones),
        'zona': zona,
        'precio de venta': float(precio_venta),
        'precio de alquiler/por mes': float(precio_alquiler)
    }

    # Enviar la solicitud POST para añadir el inmueble
    response = requests.post(f"{BASE_URL}inmuebles/{inmueble_id}", json=data)
    if response.status_code == 200:
        print(f"Inmueble {inmueble_id} añadido correctamente.")
    else:
        print(response.json().get('error'))


def actualizar_inmueble() -> None:
    """
    Solicita datos al usuario para actualizar un inmueble existente y envía la solicitud a la API.

    Esta función recoge por consola los nuevos datos de un inmueble (dueño, habitaciones, zona,
    precio de venta y precio de alquiler mensual) e intenta actualizar el inmueble en la API
    utilizando una solicitud PUT.

    Devuelve:
    -str
        mensaje de confirmación de actualizacion o mensaje de error 
    """
    inmueble_id: str = input("Introduce el ID del inmueble a actualizar: ")


    if inmueble_id not in inmuebles:
        print(f"Error: No se encuentra un inmueble con ID {inmueble_id}.")
        return

    dueño: str = input("Introduce el nuevo dueño: ")


    if dueño.isdigit():
        print("Error: El campo 'dueño' no puede ser un número.")
        return

    habitaciones: str = input("Introduce el nuevo número de habitaciones: ")


    if not habitaciones.isdigit():
        print("Error: El campo 'habitaciones' debe ser un número entero.")
        return

    zona: str = input("Introduce la nueva zona: ")


    precio_venta: str = input("Introduce el nuevo precio de venta: ")
    if not precio_venta.replace('.', '', 1).isdigit() or precio_venta.count('.') > 1:  # Verifica que el precio de venta sea un número válido y que tenga, como máximo, un solo punto decimal.
        print("Error: El campo 'precio de venta' debe ser un número válido.")
        return


    precio_alquiler: str = input("Introduce el nuevo precio de alquiler por mes: ")
    if not precio_alquiler.replace('.', '', 1).isdigit() or precio_alquiler.count('.') > 1:# Verifica que el precio de venta sea un número válido y que tenga, como máximo, un solo punto decimal.
        print("Error: El campo 'precio de alquiler' debe ser un número válido.")
        return


    data: dict = {
        'dueño': dueño,
        'habitaciones': int(habitaciones),
        'zona': zona,
        'precio de venta': float(precio_venta),
        'precio de alquiler/por mes': float(precio_alquiler)
    }

    # Enviar la solicitud PUT para actualizar el inmueble
    response = requests.put(f"{BASE_URL}inmuebles/{inmueble_id}", json=data)
    if response.status_code == 200:
        print(f"Inmueble {inmueble_id} actualizado correctamente.")
    else:
        print(response.json().get('error'))


def eliminar_inmueble():
    inmueble_id = input("Introduce el ID del inmueble a eliminar: ")
    response = requests.delete(f"{BASE_URL}inmuebles/{inmueble_id}")
    if response.status_code == 200:
        print(f"Inmueble {inmueble_id} eliminado correctamente.")
    else:
        print(response.json().get('error'))


def main():
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

