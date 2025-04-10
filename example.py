import requests

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


def actualizar_inmueble():
    inmueble_id = input("Introduce el ID del inmueble a actualizar: ")
    dueño = input("Introduce el nuevo dueño: ")
    habitaciones = input("Introduce el nuevo número de habitaciones: ")
    zona = input("Introduce la nueva zona: ")
    data = {
        'dueño': dueño,
        'habitaciones': habitaciones,
        'zona': zona
    }
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

