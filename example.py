"""
El propósito de este fichero es mostrar un menú interactivo mediante el cual el usuario pueda interactuar con la API
sin necesidad de saber nada sobre programación
"""

from auth.auth import registrar_usuario, iniciar_sesion, usuarios_registrados
from utils.filtros import filtrar_inmuebles

def mostrar_menu_principal() -> None:
    """
    Función que muestra el menú principal con todas las cosas que puede hacer el usuario
    """
    print("\n--- MENÚ ---")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Ver publicaciones de inmuebles")
    print("4. Salir")

def mostrar_menu_comprador():
    print("\n--- MENÚ DEL COMPRADOR ---")
    print("1. Ver inmuebles disponibles (filtrar)")
    print("2. Reservar o comprar inmueble")
    print("3. Ver mis reservas")
    print("4. Cerrar sesión")

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
            print(">> Aquí se podría implementar lógica para reservar o comprar.")
            # Podrías permitir elegir una publicación por ID

        elif opcion == "3":
            print(">> Aquí podrías mostrar las reservas vinculadas al usuario.")

        elif opcion == "4":
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
