from auth.auth import registrar_usuario, iniciar_sesion, usuarios_registrados
from utils.filtros import filtrar_inmuebles

resenyas = {}

def mostrar_menu_principal():
    print("\n--- MENÚ ---")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver usuarios registrados")
    print("4. Salir")

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

def menu_comprador(usuario, publicaciones):
    reservas = []  # Puedes vincular esto al usuario si implementas base de datos

    while True:
        mostrar_menu_comprador()
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == "1":
            if not publicaciones:
                print("No hay publicaciones disponibles.")
                continue

            try:
                precio_max = float(input("Precio máximo (€): ") or 0)
                zona = input("Zona: ") or None
                superficie_min = float(input("Superficie mínima (m²): ") or 0)
                tipo_alquiler = input("Tipo de alquiler: ") or None
                capacidad_min = int(input("Capacidad mínima (personas): ") or 0)

                precio_max = precio_max if precio_max > 0 else None
                superficie_min = superficie_min if superficie_min > 0 else None
                capacidad_min = capacidad_min if capacidad_min > 0 else None

                resultados = filtrar_inmuebles(
                    publicaciones,
                    precio_max=precio_max,
                    zona=zona,
                    superficie_min=superficie_min,
                    tipo_alquiler=tipo_alquiler,
                    capacidad_min=capacidad_min
                )

                if resultados:
                    print(f"\nSe encontraron {len(resultados)} publicación(es):\n")
                    for pub in resultados:
                        print(pub)  # puedes usar pub.__str__ si está implementado
                else:
                    print("No se encontraron resultados.")

            except ValueError:
                print("Entrada inválida. Intenta de nuevo.")

        elif opcion == "2":
            if not publicaciones:
                print("No hay publicaciones disponibles para reservar.")
                continue

            print("\nInmuebles disponibles:")
            for pub in publicaciones:
                print(f"ID: {pub['id']} - {pub['titulo']} - {pub['precio']}€")

            id_reserva = input("Introduce el ID del inmueble que quieres reservar: ")

            seleccionado = next((p for p in publicaciones if p["id"] == id_reserva), None)
            if seleccionado:
                usuario.reservas.append(seleccionado)
                print("Inmueble reservado con éxito.")
            else:
                print("ID no válido.")

        elif opcion == "3":
            if usuario.reservas:
                print("\n📦 Tus reservas:")
                for r in usuario.reservas:
                    print(f"- {r['titulo']} ({r['zona']}) - {r['precio']}€")
            else:
                print("No tienes reservas todavía.")

        elif opcion == "4":
            # Aquí añadimos una reseña
            id_inmueble = input("Introduce el ID del inmueble para añadir las reseñas: ")
            añadir_resenya(id_inmueble, usuario)

        elif opcion == "5": # accedo con el id del inmueble
            # Ver las reseñas de un inmueble
            id_inmueble = input("Introduce el ID del inmueble para ver las reseñas: ")
            ver_resenyas(id_inmueble)

        elif opcion == "6":
            print("Sesión cerrada.")
            break

        else:
            print("Opción no válida.")

def main():
    publicaciones = []  # Aquí puedes cargar publicaciones de prueba
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-4): ")

        if opcion == "1":
            nombre = input("Nombre de usuario: ")
            contrasenya = input("Contraseña: ")
            tipo = input("Tipo de usuario (comprador, vendedor, administrador): ").lower()
            try:
                usuario = registrar_usuario(nombre, contrasenya, tipo)
                print(f"Usuario registrado correctamente: {usuario.nombre} ({tipo})")
            except ValueError as e:
                print("Error:", e)

        elif opcion == "2":
            nombre = input("Nombre de usuario: ")
            contrasenya = input("Contraseña: ")
            try:
                usuario = iniciar_sesion(nombre, contrasenya)
                print(f"Bienvenido, {usuario.nombre} ({usuario.__class__.__name__})")

                # Solo mostramos el menú si es comprador
                if usuario.__class__.__name__.lower() == "comprador":
                    menu_comprador(usuario, publicaciones)
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

