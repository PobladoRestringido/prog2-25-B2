import requests
import webbrowser
import urllib.parse

BASE_URL = "http://127.0.0.1:5000"
token = None  # Token global para autorización

# --- Gestión del token ---
def set_token(new_token):
    global token
    token = new_token

def get_headers():
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        return {}

# --- Registro de usuario ---
def registrar():
    nombre = input("Nuevo nombre de usuario: ")
    contrasenya = input("Nueva contraseña: ")
    rol = input("Rol (comprador, vendedor, administrador): ")

    resp = requests.post(
        f"{BASE_URL}/register",
        json={"nombre": nombre, "contrasenya": contrasenya, "rol": rol}
    )

    if resp.status_code == 201:
        print("Usuario registrado correctamente.")
    else:
        try:
            error_info = resp.json()
        except Exception:
            error_info = resp.text or "Respuesta vacía"
        print("Error:", error_info)


# --- Login ---
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

# --- Ver todos los inmuebles ---
def ver_inmuebles():
    resp = requests.get(f"{BASE_URL}/inmuebles")
    if resp.status_code == 200:
        inmuebles = resp.json()
        for i, inmueble in enumerate(inmuebles, 1):
            print(
                f"{i}. {inmueble['nombre']} - {inmueble['precio']}€ - Zona: {inmueble['zona']} - Dueño: {inmueble['duenyo']} - Dirección: {inmueble.get('direccion', 'N/A')}")
    else:
        print("Error al obtener inmuebles:", resp.text)

# --- Ver inmueble por ID (requiere token) ---
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
            print(f" {k}: {v}")

        direccion = inmueble.get("direccion") or inmueble.get("zona")
        if direccion:
            if input("\n¿Abrir en Google Maps? (s/n): ").strip().lower() == 's':
                query = urllib.parse.quote(direccion)
                url = f"https://www.google.com/maps/search/?api=1&query={query}"
                webbrowser.open(url)
    else:
        print("Error:", resp.text)

# --- Añadir inmueble (requiere token) ---
def añadir_inmueble():
    if not token:
        print("Debes hacer login primero")
        return
    headers = {'Authorization': f'Bearer {token}'}
    tipo = input("Tipo (piso/vivienda_unifamiliar): ").strip()
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    zona = input("Zona(centro_madrid/norte_madrid/sur_madrid/,\n"
                 "casco_toledo/playa_valencia/rural_asturias/,\n"
                 "centro_barcelona/monte_bilbao/residencial_sevilla/costa_malaga)")
    duenyo = input("Dueño (lucia/juan/marta/adminvivienda/laura/carlos/ines/pedro/alba/sergio): ")

    # Para simplicidad, habitaciones mínimas
    habitaciones = []
    n_hab = int(input("Número de habitaciones: "))
    for _ in range(n_hab):
        tipo_hab = input(" Tipo habitación (dormitorio/cocina/banyo/salon): ")
        superficie = float(input(" Superficie: "))
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

# --- Eliminar inmueble (requiere token) ---
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

# --- Añadir comentario a inmueble ---
def añadir_comentario():
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

# --- Ver comentarios de inmueble ---
def ver_comentarios():
    try:
        id_inmueble = int(input("Introduce el ID del inmueble para ver comentarios: "))
    except ValueError:
        print("ID inválido. Debe ser un número entero.")
        return

    url = f"{BASE_URL}/inmuebles/{id_inmueble}/comentarios"

    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            datos = resp.json()
            comentarios = datos.get("comentarios", [])
            if comentarios:
                print(f"Comentarios para inmueble {id_inmueble}:")
                for i, comentario in enumerate(comentarios, 1):
                    print(f" {i}. {comentario}")
            else:
                print(f"No hay comentarios para el inmueble {id_inmueble}.")
        elif resp.status_code == 404:
            print(f"Inmueble con ID {id_inmueble} no encontrado.")
        else:
            print(f"Error inesperado: {resp.status_code}")
    except requests.exceptions.RequestException as e:
        print("Error al conectar con la API:", e)

# --- Menú interactivo ---
def menu():
    while True:
        print("\n--- Menú API Inmuebles ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver todos los inmuebles")
        print("4. Ver inmueble por ID (admin sólo)")
        print("5. Añadir inmueble")
        print("6. Eliminar inmueble")
        print("7. Añadir comentario a inmueble")
        print("8. Ver comentarios de un inmueble")
        print("9. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_inmuebles()
        elif opcion == "4":
            ver_inmueble_por_id()
        elif opcion == "5":
            añadir_inmueble()
        elif opcion == "6":
            eliminar_inmueble()
        elif opcion == "7":
            añadir_comentario()
        elif opcion == "8":
            ver_comentarios()
        elif opcion == "9":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()