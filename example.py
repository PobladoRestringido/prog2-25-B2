import requests
import webbrowser
import urllib.parse

BASE_URL = "http://127.0.0.1:5000"
token = None

def set_token(new_token):
    global token
    token = new_token

def get_headers():
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        return {}

def registrar():
    nombre = input("Nuevo nombre de usuario: ")
    contrasenya = input("Nueva contraseña: ")
    rol = input("Rol (comprador, vendedor, administrador): ")
    resp = requests.post(f"{BASE_URL}/register", json={"nombre": nombre, "contrasenya": contrasenya, "rol": rol})
    if resp.status_code == 201:
        print("Usuario registrado correctamente.")
    else:
        print("Error:", resp.json())

def login():
    global token
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")

    response = requests.post(f"{BASE_URL}/login", json={"nombre": nombre, "contrasenya": contrasenya})

    if response.status_code == 200:
        token = response.json()['access_token']
        print("Login exitoso. Token guardado.")
    else:
        print("Error en login:", response.json())


def ver_inmuebles():
    resp = requests.get(f"{BASE_URL}/inmuebles")
    if resp.status_code == 200:
        inmuebles = resp.json()
        for i, inmueble in enumerate(inmuebles, 1):
            print(f"{i}. {inmueble['nombre']} - {inmueble['precio']}€ - Zona: {inmueble['zona']} - Dueño: {inmueble['duenyo']} - Dirección: {inmueble['direccion']}")
    else:
        print("Error al obtener inmuebles:", resp.text)


def ver_inmueble_por_id():
    if not token:
        print("Debes hacer login primero")
        return
    id = input("ID del inmueble: ")
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(f"{BASE_URL}/inmuebles/{id}", headers=headers)
    if resp.status_code == 200:
        inmueble = resp.json()
        print("Detalles inmueble:")
        for k, v in inmueble.items():
            print(f"  {k}: {v}")
        
        direccion = inmueble.get("direccion") or inmueble.get("zona")
        if direccion:
            if input("\n¿Abrir en Google Maps? (s/n): ").strip().lower() == 's':
                query = urllib.parse.quote(direccion)
                url = f"https://www.google.com/maps/search/?api=1&query={query}"
                webbrowser.open(url)

    else:
        print("Error:", resp.text)


def añadir_inmueble():
    if not token:
        print("Debes hacer login primero")
        return
    headers = {'Authorization': f'Bearer {token}'}
    tipo = input("Tipo (piso/vivienda_unifamiliar): ").strip()
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    zona = input("Zona: ")
    duenyo = input("Dueño (nombre): ")

    # Para simplicidad, habitaciones mínimas
    habitaciones = []
    n_hab = int(input("Número de habitaciones: "))
    for _ in range(n_hab):
        tipo_hab = input("  Tipo habitación (dormitorio/cocina/banyo/salon): ")
        superficie = float(input("  Superficie: "))
        hab = {"tipo": tipo_hab, "superficie": superficie}
        habitaciones.append(hab)

    datos = {
        "tipo": tipo,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "zona": zona,
        "duenyo": duenyo,
        "habitaciones": habitaciones,
    }
    if tipo == "piso":
        planta = int(input("Planta: "))
        ascensor = input("Ascensor (True/False): ").lower() == "true"
        datos["planta"] = planta
        datos["ascensor"] = ascensor
    elif tipo == "vivienda_unifamiliar":
        tiene_piscina = input("Tiene piscina (True/False): ").lower() == "true"
        datos["tiene_piscina"] = tiene_piscina
        datos["jardin"] = None  # Por simplicidad

    resp = requests.post(f"{BASE_URL}/inmuebles", json=datos, headers=headers)
    if resp.status_code == 201:
        print("Inmueble añadido correctamente.")
    else:
        print("Error al añadir inmueble:", resp.text)


def eliminar_inmueble():
    if not token:
        print("Debes hacer login primero")
        return
    try:
        id = int(input("ID del inmueble a eliminar: "))
    except ValueError:
        print("El ID debe ser un número entero.")
        return

    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.delete(f"{BASE_URL}/inmuebles/{id}", headers=headers)
    if resp.status_code == 200:
        print("Inmueble eliminado.")
    else:
        print("Error:", resp.text)


def añadir_comentario():
    global token
    if not token:
        print("Debes hacer login primero para poder comentar.")
        return

    try:
        id_inmueble = int(input("Introduce el ID del inmueble para comentar: "))
    except ValueError:
        print("ID inválido.")
        return

    comentario = input("Escribe tu comentario: ").strip()
    if not comentario:
        print("El comentario no puede estar vacío.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {"comentario": comentario}

    url = f"{BASE_URL}/inmueble/{id_inmueble}/escribir"

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print("Comentario añadido con éxito!")
    else:
        print("Error al añadir comentario:", response.json())


def menu():
    while True:
        print("\n--- Menú API Inmuebles ---")
        print("1. Login")
        print("2. Ver todos los inmuebles")
        print("3. Ver inmueble por ID (admin sólo)")
        print("4. Añadir inmueble")
        print("5. Eliminar inmueble")
        print("6. Añadir comentario a inmueble")
        print("7. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            login()
        elif opcion == "2":
            ver_inmuebles()
        elif opcion == "3":
            ver_inmueble_por_id()
        elif opcion == "4":
            añadir_inmueble()
        elif opcion == "5":
            eliminar_inmueble()
        elif opcion == "6":
            añadir_comentario()
        elif opcion=="7":
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()
