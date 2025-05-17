# inmuebles_ejemplo.py

"""
Creación inmuebles de ejemplo

El propósito de este script es crear un set inicial de inmuebles con el único
propósito de ser serializados, de modo que 'example.py' ofrezca una experiencia
más interesante (y funcional)
"""
from modelos.inmueble.piso import Piso
from modelos.inmueble.vivienda_unifamiliar import ViviendaUnifamiliar
from vendedor_ejemplo import vendedor1, vendedor2, vendedor3
from Zonas_ejemplo import zonas
from habitaciones_ejemplo import habitaciones_piso1, habitaciones_piso2, habitaciones_casa1

piso1 = Piso(
    nombre="Piso 1",
    descripcion="Bonito piso céntrico",
    habitaciones=habitaciones_piso1,
    precio=180000,
    zona=zona_centro_madrid,  
    duenyo=vendedor1,
    planta=3,
    ascensor=True
)

zonas["centro_madrid"].agregar_inmueble(piso1)

# Crear Piso 2
piso2 = Piso(
    nombre="Piso Familiar en Zona Norte",
    descripcion="Ideal para familias grandes, zona tranquila y bien conectada.",
    precio=210000,
    habitaciones=habitaciones_piso2,
    zona=zonas["norte_madrid"],
    duenyo=vendedor2,
    planta=3,
    ascensor=True
)
zonas["norte_madrid"].agregar_inmueble(piso2)

# Crear Vivienda Unifamiliar
casa1 = ViviendaUnifamiliar(
    nombre="Chalet con Jardín y Piscina",
    descripcion="Casa espaciosa con jardín privado y piscina.",
    precio=350000,
    habitaciones=habitaciones_casa1,
    zona=zonas["rural_asturias"],
    duenyo=vendedor3,
    tiene_piscina=True,
    jardin="Jardín de 100m² con césped natural y árboles"
)
zonas["rural_asturias"].agregar_inmueble(casa1)

inmuebles = [piso1, casa1]

if __name__ == "__main__":
    for inmueble in inmuebles:
        print(type(inmueble.zona))  # Debería mostrar <class 'modelos.zona_geografica.ZonaGeografica'>
        print(inmueble.nombre, inmueble.zona.nombre)


