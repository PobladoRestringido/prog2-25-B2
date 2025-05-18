# inmuebles_ejemplo.py
from modelos.habitacion.dormitorio import Dormitorio
from modelos.habitacion.cocina import Cocina
from modelos.habitacion.banyo import Banyo
from modelos.habitacion.salon import Salon
from modelos.inmueble.piso import Piso
from modelos.inmueble.vivienda_unifamiliar import ViviendaUnifamiliar

from examples.Zonas_ejemplo import zonas
from examples.vendedor_ejemplo import vendedores

# Crear habitaciones para piso
habitaciones_piso = [
    Dormitorio(12.0, tiene_cama=True, tiene_lampara=True),
    Cocina(8.0, tiene_frigorifico=True, tiene_horno=True),
    Banyo(5.0, tiene_ducha=True, tiene_lavabo=True),
    Salon(20.0, tiene_televisor=True, tiene_sofa=True)
]

# Crear habitaciones para vivienda unifamiliar
habitaciones_casa = [
    Dormitorio(15.0, tiene_cama=True),
    Cocina(10.0, tiene_frigorifico=True),
    Banyo(7.0, tiene_banyera=True, tiene_lavabo=True),
    Salon(25.0, tiene_sofa=True),
    Dormitorio(10.0, tiene_mesa_estudio=True)
]

# Crear inmueble Piso
piso1 = Piso(
    nombre="Piso Luminoso",
    descripcion="Piso céntrico con buenas vistas",
    habitaciones=habitaciones_piso,
    precio=180000,
    zona=zonas["centro_madrid"],
    duenyo=vendedores[0],
    planta=3,
    ascensor=True
)

# Crear inmueble Vivienda Unifamiliar
casa1 = ViviendaUnifamiliar(
    duenyo=vendedores[1],
    descripcion="Casa unifamiliar con jardín y piscina",
    precio=350000,
    nombre="Casa Rural",
    habitaciones=habitaciones_casa,
    zona=zonas["norte_madrid"],
    tiene_piscina=True,
    jardin=None
)

# Añadir inmuebles a las zonas correspondientes
zonas["centro_madrid"].agregar_inmueble(piso1)
zonas["norte_madrid"].agregar_inmueble(casa1)

# Lista de inmuebles para trabajar
inmuebles = [piso1, casa1]

for i, inmueble in enumerate(inmuebles, 1):
    print(f"Inmueble {i}: {inmueble.nombre} - Precio: {inmueble.precio} € - Zona: {inmueble.zona}")
    print(f"Dueño: {inmueble.duenyo.nombre}")
    print("Habitaciones:")
    for hab in inmueble.habitaciones:
        print(f" - {hab}")
    print()

