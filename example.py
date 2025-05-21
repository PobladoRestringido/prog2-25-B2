import requests

API_URL = "https://pobladorestringido.pythonanywhere.com"
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
    resp = requests.post(f"{API_URL}/register", json={"nombre": nombre, "contrasenya": contrasenya, "rol": rol})
    if resp.status_code == 201:
        print("Usuario registrado correctamente.")
    else:
        print("Error:", resp.json())

def login():
    nombre = input("Nombre de usuario: ")
    contrasenya = input("Contraseña: ")
    resp = requests.post(f"{API_URL}/login", json={"nombre": nombre, "contrasenya": contrasenya})
    if resp.status_code == 200:
        set_token(resp.json()["access_token"])
        print("Login correcto!")
    else:
        print("Error:", resp.json())

def listar_inmuebles():
    resp = requests.get(f"{API_URL}/inmuebles", headers=get_headers())
    if resp.status_code == 200:
        inmuebles = resp.json()
        for i, inmueble in enumerate(inmuebles, 1):
            print(f"Inmueble {i}: {inmueble.get('nombre', 'Sin nombre')} - Precio: {inmueble.get('precio', 'N/A')} €")
    else:
        print("Error:", resp.json())

def buscar_inmueble_id():
    id_inmueble = input("ID del inmueble: ")
    resp = requests.get(f"{API_URL}/inmuebles/{id_inmueble}", headers=get_headers())
    if resp.status_code == 200:
        inmueble = resp.json()
        print(inmueble)
    else:
        print("Error:", resp.json())

def añadir_inmueble():
    print("Introduce datos del inmueble:")
    tipo = input("Tipo (piso / vivienda_unifamiliar): ")
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    precio = float(input("Precio: "))
    zona = input("Zona (clave): ")
    duenyo = input("Nombre del dueño: ")

    habitaciones = []
    n_habs = int(input("Número de habitaciones: "))
    for i in range(n_habs):
        print(f"Datos habitación {i+1}:")
        tipo_hab = input("  Tipo (dormitorio, cocina, banyo, salon): ")
        superficie = float(input("  Superficie: "))
        hab_data = {"tipo": tipo_hab, "superficie": superficie}
        habitaciones.append(hab_data)

    planta = None
    ascensor = False
    tiene_piscina = False
    jardin = None

    if tipo == "piso":
        planta = int(input("Planta: "))
        ascensor = input("¿Tiene ascensor? (s/n): ").lower() == 's'
    elif tipo == "vivienda_unifamiliar":
        tiene_piscina = input("¿Tiene piscina? (s/n): ").lower() == 's'

    datos = {
        "tipo": tipo,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "zona": zona,
        "duenyo": duenyo,
        "habitaciones": habitaciones
    }
    if planta is not None:
        datos["planta"] = planta
    if ascensor:
        datos["ascensor"] = ascensor
    if tiene_piscina:
        datos["tiene_piscina"] = tiene_piscina
    if jardin:
        datos["jardin"] = jardin

    resp = requests.post(f"{API_URL}/inmuebles", json=datos, headers=get_headers())
    if resp.status_code in [200, 201]:
        print("Inmueble añadido correctamente.")
    else:
        print("Error:", resp.json())

def actualizar_inmueble():
    id_inmueble = input("ID del inmueble a actualizar: ")
    print("Introduce los campos a actualizar (deja vacío para no cambiar):")
    nombre = input("Nuevo nombre: ")
    descripcion = input("Nueva descripción: ")
    precio = input("Nuevo precio: ")
    zona = input("Nueva zona (clave): ")

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if descripcion:
        datos["descripcion"] = descripcion
    if precio:
        datos["precio"] = float(precio)
    if zona:
        datos["zona"] = zona

    if not datos:
        print("No hay datos para actualizar.")
        return

    resp = requests.put(f"{API_URL}/inmuebles/{id_inmueble}", json=datos, headers=get_headers())
    if resp.status_code == 200:
        print("Inmueble actualizado correctamente.")
    else:
        print("Error:", resp.json())

def eliminar_inmueble():
    id_inmueble = input("ID del inmueble a eliminar: ")
    resp = requests.delete(f"{API_URL}/inmuebles/{id_inmueble}", headers=get_headers())
    if resp.status_code == 200:
        print("Inmueble eliminado correctamente.")
    else:
        print("Error:", resp.json())

def escribir_comentario():
    id_inmueble = input("ID del inmueble: ")
    comentario = input("Comentario: ")
    resp = requests.post(f"{API_URL}/inmueble/{id_inmueble}/escribir", json={"comentario": comentario})
    if resp.status_code == 200:
        print("Comentario agregado con éxito.")
    else:
        print("Error:", resp.json())

def mostrar_comentarios():
    id_inmueble = input("ID del inmueble: ")
    resp = requests.get(f"{API_URL}/inmueble/{id_inmueble}/comentarios")
    if resp.status_code == 200:
        comentarios = resp.json()
        print("Comentarios:")
        for c in comentarios.get("comentarios_usuario", []):
            print(f" - {c['comentario']}")
    else:
        print("Error:", resp.json())

def obtener_descripcion(inmueble_id: int):
    try:
        response = requests.get(f"{API_URL}/inmueble/{inmueble_id}/descripcion")
        if response.status_code == 200:
            print("\n Descripción generada:")
            print(response.json()["descripcion"])
        else:
            print(f"\nError {response.status_code}: {response.json().get('error', 'Desconocido')}")
    except requests.exceptions.ConnectionError:
        print("\nNo se pudo conectar con la API. ¿Está corriendo Flask?")


def menu():
    while True:
        print("\n--- Menú API Inmuebles ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Listar inmuebles")
        print("4. Buscar inmueble por ID")
        print("5. Añadir inmueble")
        print("6. Actualizar inmueble")
        print("7. Eliminar inmueble")
        print("8. Escribir comentario")
        print("9. Mostrar comentarios")
        print("10. Descripción del inmueble")
        print("11. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            listar_inmuebles()
        elif opcion == "4":
            buscar_inmueble_id()
        elif opcion == "5":
            añadir_inmueble()
        elif opcion == "6":
            actualizar_inmueble()
        elif opcion == "7":
            eliminar_inmueble()
        elif opcion == "8":
            escribir_comentario()
        elif opcion == "9":
            mostrar_comentarios()
        elif opcion=="10":
            try:
                inmueble_id = int(input("Introduce el ID del inmueble: "))
                obtener_descripcion(inmueble_id)
            except ValueError:
                print("ID inválido. Debe ser un número.")
        elif opcion == "11":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
