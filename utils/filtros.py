from modelos.publicacion import Publicacion

def filtrar_inmuebles(publicaciones, precio_max=None, zona=None,
                      superficie_min=None, tipo_alquiler=None,
                      capacidad_min=None):
    """
    Filtra publicaciones según distintos criterios opcionales.
    
    Parámetros:
        - publicaciones: lista de objetos Publicacion
        - precio_max: precio máximo permitido
        - zona: nombre de la zona deseada
        - superficie_min: superficie mínima total (m²)
        - tipo_alquiler: string o etiqueta (p. ej., 'mensual', 'vacacional')
        - capacidad_min: número mínimo de personas
    
    Retorna:
        - lista de publicaciones filtradas
    """
    resultados = []
    for pub in publicaciones:
        inmueble = pub._Publicacion__inmueble  # acceso directo si es privado
        cumple = True

        if precio_max is not None and pub._Publicacion__precio > precio_max:
            cumple = False

        if zona is not None and inmueble._Inmueble__zona._ZonaGeografica__nombre.lower() != zona.lower():
            cumple = False

        if superficie_min is not None:
            total_superficie = sum([hab._Habitacion__superficie for hab in inmueble._Inmueble__habitaciones])
            if total_superficie < superficie_min:
                cumple = False

        if tipo_alquiler is not None and getattr(pub, "tipo_alquiler", None) != tipo_alquiler:
            cumple = False

        if capacidad_min is not None:
            # Asumimos que cada cama = 1 persona, por ejemplo
            capacidad = 0
            for hab in inmueble._Inmueble__habitaciones:
                if hab.__class__.__name__.lower() == "dormitorio" and getattr(hab, "_dormitorio__tiene_cama", False):
                    capacidad += 1
            if capacidad < capacidad_min:
                cumple = False

        if cumple:
            resultados.append(pub)

    return resultados
