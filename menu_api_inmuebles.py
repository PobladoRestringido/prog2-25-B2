'''
NOTA:
Este menu se tendrá que juntar con los menus de las otras APIs  para hacer un menu común con todas las opciones
(de momento lo dejo así para tener localizada cada parte por si hay errores o algo para cambiar)
'''

import requests

API_URL = "http://127.0.0.1:5000/inmuebles"

def menu():
    while True:
        print("\n--- MENÚ DE INMUEBLES ---")
        print("1. Ver todos los inmuebles")
        print("2. Ver un inmueble por ID")
        print("3. Añadir un nuevo inmueble")
        print("4. Eliminar un inmueble")
        print("5. Actualizar un inmueble")
        print("6. Salir")

        opcion = input("Elige una opción (1-6): ")

        if opcion == '1':
            ver_todos_inmuebles()
        elif opcion == '2':
            ver_inmueble_id()
        elif opcion == '3':
            añadir_inmueble()
        elif opcion == '4':
            eliminar_inmueble()
        elif opcion == '5':
            actualizar_inmueble()
        elif opcion == '6':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


def ver_todos_inmuebles():
    response = requests.get(API_URL)
    if response.status_code == 200:
        inmuebles = response.json()
        for inmueble in inmuebles:
            print(inmueble)
    else:
        print("No se pudieron obtener los inmuebles.")


def ver_inmueble_id():
    inmueble_id = input("Introduce el ID del inmueble: ")
    response = requests.get(f"{API_URL}/{inmueble_id}")
    if response.status_code == 200:
        inmueble = response.json()
        print(inmueble)
    else:
        print(f"Error: Inmueble con ID {inmueble_id} no encontrado.")


def añadir_inmueble():
    inmueble_id = input("Introduce el ID del nuevo inmueble: ")
    dueño = input("Introduce el nombre del dueño: ")
    habitacion = int(input("Introduce el número de habitaciones: "))
    zona = input("Introduce la zona del inmueble: ")

    nuevo_inmueble = {
        "dueño": dueño,
        "habitacion": habitacion,
        "zona": zona
    }

    response = requests.post(f"{API_URL}/{inmueble_id}", json=nuevo_inmueble)
    if response.status_code == 200:
        print(response.json()["mensaje"])
    else:
        print(response.json()["error"])


def eliminar_inmueble():
    inmueble_id = input("Introduce el ID del inmueble a eliminar: ")
    response = requests.delete(f"{API_URL}/{inmueble_id}")
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error: Inmueble con ID {inmueble_id} no encontrado.")

def actualizar_inmueble():
    inmueble_id = input("Introduce el ID del inmueble a actualizar: ")

    # Verificar si el inmueble existe antes de intentar actualizarlo
    response = requests.get(f"{API_URL}/{inmueble_id}")
    if response.status_code != 200:
        print(f"Error: Inmueble con ID {inmueble_id} no encontrado.")
        return

    print("Introduce los nuevos datos para el inmueble (deja vacío si no deseas cambiarlo):")

    dueño = input(f"Nuevo dueño (actual: {response.json()['dueño']}): ")
    habitacion = input(f"Nuevo número de habitaciones (actual: {response.json()['habitacion']}): ")
    zona = input(f"Nueva zona (actual: {response.json()['zona']}): ")

    # Crear un diccionario con los nuevos datos solo si se proporcionan
    datos_actualizados = {}
    if dueño:
        datos_actualizados["dueño"] = dueño
    if habitacion:
        datos_actualizados["habitacion"] = int(habitacion)
    if zona:
        datos_actualizados["zona"] = zona

    # Si no se proporciona ningún dato, no actualizamos
    if not datos_actualizados:
        print("No se proporcionaron datos para actualizar.")
        return

    # Enviar la solicitud PUT para actualizar el inmueble
    response = requests.put(f"{API_URL}/{inmueble_id}", json=datos_actualizados)
    if response.status_code == 200:
        print(response.json()["mensaje"])
    else:
        print(f"Error al actualizar el inmueble: {response.text}")

if __name__ == "__main__":
    menu()
