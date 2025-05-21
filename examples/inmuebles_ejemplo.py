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
habitaciones_piso2 = [
    Dormitorio(11.0, tiene_cama=True, tiene_lampara=False),
    Cocina(7.5, tiene_frigorifico=True, tiene_microondas=True),
    Banyo(4.0, tiene_ducha=True),
    Salon(18.0, tiene_televisor=False, tiene_sofa=True)
]
habitaciones_piso3 = [
    Dormitorio(10.0, tiene_cama=True, tiene_mesa_estudio=True),
    Cocina(6.0, tiene_frigorifico=True),
    Banyo(4.5, tiene_banyera=True, tiene_lavabo=True),
    Salon(16.0, tiene_sofa=True)
]

# Crear habitaciones para vivienda unifamiliar
habitaciones_casa = [
    Dormitorio(15.0, tiene_cama=True),
    Cocina(10.0, tiene_frigorifico=True),
    Banyo(7.0, tiene_banyera=True, tiene_lavabo=True),
    Salon(25.0, tiene_sofa=True),
    Dormitorio(10.0, tiene_mesa_estudio=True)
]
habitaciones_casa2 = [
    Dormitorio(16.0, tiene_cama=True),
    Dormitorio(12.0, tiene_cama=False, tiene_mesa_estudio=True),
    Cocina(9.0, tiene_frigorifico=True, tiene_horno=True),
    Banyo(6.0, tiene_ducha=True, tiene_lavabo=True),
    Salon(22.0, tiene_sofa=True, tiene_televisor=True)
]
habitaciones_casa3 = [
    Dormitorio(14.0, tiene_cama=True),
    Dormitorio(11.0, tiene_cama=True),
    Cocina(9.5, tiene_horno=True),
    Banyo(5.0, tiene_ducha=True),
    Salon(20.0, tiene_sofa=True, tiene_televisor=True)
]

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
piso2 = Piso(
    nombre="Piso Moderno",
    descripcion="Piso reformado con cocina americana",
    habitaciones=habitaciones_piso2,
    precio=210000,
    zona=zonas["sur_madrid"],
    duenyo=vendedores[2],
    planta=5,
    ascensor=False
)
piso3 = Piso(
    nombre="Piso Familiar",
    descripcion="Ideal para familias con niños",
    habitaciones=habitaciones_piso3,
    precio=165000,
    zona=zonas["oeste_madrid"],
    duenyo=vendedores[4],
    planta=2,
    ascensor=True
)


casa1 = ViviendaUnifamiliar(
    duenyo=vendedores[1],
    descripcion="Casa unifamiliar con jardín y piscina",
    precio=350000,
    nombre="Casa Rural",
    habitaciones=habitaciones_casa1,
    zona=zonas["norte_madrid"],
    tiene_piscina=True,
    jardin=None
)
casa2 = ViviendaUnifamiliar(
    duenyo=vendedores[3],
    descripcion="Chalet adosado en zona residencial tranquila",
    precio=420000,
    nombre="Chalet Tranquilo",
    habitaciones=habitaciones_casa2,
    zona=zonas["este_madrid"],
    tiene_piscina=False,
    jardin="Pequeño jardín delantero"
)
casa3 = ViviendaUnifamiliar(
    duenyo=vendedores[0],
    descripcion="Casa amplia con gran patio trasero",
    precio=390000,
    nombre="Casa Familiar",
    habitaciones=habitaciones_casa3,
    zona=zonas["norte_madrid"],
    tiene_piscina=True,
    jardin="Gran patio con árboles frutales"
)

# Añadir inmuebles a las zonas correspondientes
zonas["centro_madrid"].agregar_inmueble(piso1)
zonas["norte_madrid"].agregar_inmueble(casa1)

zonas["sur_madrid"].agregar_inmueble(piso2)
zonas["este_madrid"].agregar_inmueble(casa2)

zonas["oeste_madrid"].agregar_inmueble(piso3)
zonas["norte_madrid"].agregar_inmueble(casa3)

# Lista de inmuebles para trabajar
inmuebles = [piso1, casa1, piso2, casa2, piso3, casa3]

for i, inmueble in enumerate(inmuebles, 1):
    print(f"Inmueble {i}: {inmueble.nombre} - Precio: {inmueble.precio} € - Zona: {inmueble.zona.nombre}")
    print(f"Dueño: {inmueble.duenyo.nombre}")
    print("Habitaciones:")
    for hab in inmueble.habitaciones:
        print(f" - {hab}")
    print()

