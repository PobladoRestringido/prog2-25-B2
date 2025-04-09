from auth.auth import registrar_usuario, iniciar_sesion, usuarios_registrados
from utils.filtros import filtrar_inmuebles

from API import inmuebles
resenyas = {} # clave: id_inmueble, valor: lista de dicts con reseñas

def mostrar_menu_principal():
    print("\n--- MENÚ ---")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver usuarios registrados")
    print("4. Salir")

def mostrar_menu_comprador():
    print("\n--- MENÚ DEL COMPRADOR ---")
    print("1. Ver inmuebles disponibles")
    print("2. Reservar inmueble")
    print("3. Ver mis reservas")
    print("4. Cancelar una reserva")
    print("5. Añadir reseñas")
    print("6. Ver reseñas")
    print("7. Cerrar sesión")

def añadir_resenya(id_inmueble, usuario):
    """ Función para añadir una reseña a un inmueble """
    resenya = input("Escribe tu reseña a continuación: ")

    # Si el inmueble ya tiene reseñas, las agregamos a la lista
    if id_inmueble not in resenyas:
        resenyas[id_inmueble] = []

    resenyas[id_inmueble].append({
        'usuario': usuario.nombre,
        'reseña': resenya
    })
    print("Reseña añadida correctamente.")


def ver_resenyas(id_inmueble):
    """ Función para ver las reseñas de un inmueble """
    if id_inmueble in resenyas:
        print(f"\nReseñas de la vivienda {id_inmueble}:")
        for resenya in resenyas[id_inmueble]:
            print(f"- {resenya['usuario']}: {resenya['reseña']}")
    else:
        print("Este inmueble aún no tiene reseñas.")


def aplicar_filtros():
    print("\nPuedes filtrar por zona, número de habitaciones o por precio.")

    print("\n¿Estás buscando para compra o alquiler?")
    tipo_propiedad = input("Selecciona 'compra' o 'alquiler': ").lower()

    if tipo_propiedad not in ['compra', 'alquiler']:
        print("Tipo de propiedad no válido. Solo se permite 'compra' o 'alquiler'.")
        return

    zona = input("Filtrar por zona (o Enter para ignorar): ").lower()

    habitaciones = input("Filtrar por número de habitaciones (o Enter para ignorar): ")

    precio_max = input(
        f"Filtrar inmuebles para {tipo_propiedad} con precios menores de: (deja en blanco para no filtrar): ")
    try:
        if precio_max:
            precio_max = float(precio_max)
        else:
            precio_max = None
    except ValueError:
        print("Entrada inválida para precio.")
        return

    encontrados = False
    for id_inmueble, datos in inmuebles.items():

        precio_key = f"Precio de {tipo_propiedad}/por mes" if tipo_propiedad == "alquiler" else "Precio de venta"

        cumple_precio = not precio_max or datos.get(precio_key, float('inf')) <= precio_max

        cumple_zona = not zona or datos.get("zona", "").lower() == zona

        cumple_hab = not habitaciones or str(datos.get("habitaciones", datos.get("habitacion", ""))) == habitaciones
        if cumple_zona and cumple_hab and cumple_precio:
            encontrados = True
            print(f"\nID: {id_inmueble}")
            for clave, valor in datos.items():
                print(f"  {clave.capitalize()}: {valor}")
    if not encontrados:
        print("No se encontraron inmuebles con esos filtros.")


def menu_comprador(usuario, publicaciones, resenyas):
    if not hasattr(usuario, "reservas"):
        usuario.reservas = []

    while True:
        mostrar_menu_comprador()
        opcion = input("Selecciona una opción (1-7): ")

        if opcion == "1":
            filtros = input('¿Desea aplicar filtros para mostrar los inmuebles? (si/no)')
            if filtros == 'si':
                aplicar_filtros()
            else:
                for id_inmueble, datos in inmuebles.items():
                    print(f"\nID: {id_inmueble}")
                    for clave, valor in datos.items():
                        print(f"  {clave.capitalize()}: {valor}")

        elif opcion == "2":
            print("\n--- Inmuebles disponibles ---")
            for id_inmueble, datos in inmuebles.items():
                zona = datos.get("zona", "Desconocida")
                habitaciones = datos.get("habitaciones", datos.get("habitacion", "N/A"))
                print(f"ID: {id_inmueble} - Zona: {zona} - Habitaciones: {habitaciones}")

            id_reserva = input("Introduce el ID del inmueble a reservar: ")

            if id_reserva in inmuebles:
                reserva = {**inmuebles[id_reserva], "id": id_reserva}
                usuario.reservas.append(reserva)
                print("Inmueble reservado con éxito.")
            else:
                print("ID no válido.")

        elif opcion == "3":
            if usuario.reservas:
                print("\n--- Tus reservas ---:")
                for i, r in enumerate(usuario.reservas, 1):
                    zona = r.get("zona", "Desconocida")
                    habitaciones = r.get("habitaciones", r.get("habitacion", "N/A"))
                    print(f"{i}. ID: {r['id']} | Zona: {zona} | Habitaciones: {habitaciones}")

            else:
                print("No tienes reservas todavía.")


        elif opcion == "4":

            if not usuario.reservas:
                print("No tienes reservas para cancelar.")

                continue

            print("\n--- Cancelar una reserva ---")

            for r in usuario.reservas:
                print(f"- ID: {r['id']} | Zona: {r.get('zona', '')}")

            id_cancelar = input("Introduce el ID del inmueble a cancelar: ")

            for reserva in usuario.reservas:

                if reserva["id"] == id_cancelar:
                    usuario.reservas.remove(reserva)

                    print(f"Reserva cancelada: {id_cancelar}")

                    break

            else:

                print("No tienes una reserva con ese ID.")
        elif opcion == "5":

            id_inmueble = input("Introduce el ID del inmueble para añadir reseña: ")

            if id_inmueble in inmuebles:
                añadir_resenya(id_inmueble, usuario)

            else:
                print("Ese inmueble no existe.")


        elif opcion == "6":

            id_inmueble = input("Introduce el ID del inmueble para ver las reseñas: ")

            if id_inmueble in inmuebles:
                ver_resenyas(id_inmueble)
            else:
                print("Ese inmueble no existe.")


        elif opcion == "7":
            print("Sesión cerrada.")
            break

        else:
            print("Opción no válida.")

def main():
    publicaciones = []  # Aquí puedes cargar publicaciones de prueba

    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == "1": # registro de usuario
            nombre = input("Nombre de usuario: ")
            contrasenya = input("Contraseña: ")
            tipo = input("Tipo de usuario (comprador, vendedor, administrador): ").lower()
            try:
                usuario = registrar_usuario(nombre, contrasenya, tipo)
                print(f"Usuario registrado correctamente: {usuario.nombre} ({tipo})")
            except ValueError as e:
                print("Error:", e)

        elif opcion == "2": # iniciar sesión
            nombre = input("Nombre de usuario: ")
            contrasenya = input("Contraseña: ")

            try:
                usuario = iniciar_sesion(nombre, contrasenya)
                print(f"Bienvenido, {usuario.nombre} ({usuario.__class__.__name__})")

                # Solo mostramos el menú si es comprador
                if usuario.__class__.__name__.lower() == "comprador":
                    menu_comprador(usuario, publicaciones, resenyas)
                else:
                    print("Este tipo de usuario no tiene menú implementado todavía.")

            except ValueError as e:
                print("Error:", e)

        elif opcion == "3":
            if usuarios_registrados:
                print("\nUsuarios registrados:")
                for u in usuarios_registrados:
                    print(f"- {u.nombre} ({u.__class__.__name__})")
            else:
                print("No hay usuarios registrados.")

        elif opcion == "4":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
