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
habitaciones_piso1 = [
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

habitaciones_piso4 = [
    Dormitorio(13.0, tiene_cama=True),
    Cocina(9.0, tiene_frigorifico=True, tiene_horno=True, tiene_microondas=True),
    Banyo(5.5, tiene_ducha=True, tiene_lavabo=True),
    Salon(21.0, tiene_televisor=True, tiene_sofa=True)
]
habitaciones_piso5 = [
    Dormitorio(14.0, tiene_cama=True, tiene_mesa_estudio=True),
    Cocina(7.0, tiene_frigorifico=True),
    Banyo(4.0, tiene_ducha=True, tiene_lavabo=True),
    Salon(19.0, tiene_sofa=True, tiene_televisor=True)
]

# Crear habitaciones para vivienda unifamiliar
habitaciones_casa1 = [
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
habitaciones_casa4 = [
    Dormitorio(13.0, tiene_cama=True),
    Dormitorio(10.0, tiene_mesa_estudio=True),
    Cocina(8.0, tiene_frigorifico=True, tiene_microondas=True),
    Banyo(6.0, tiene_ducha=True, tiene_lavabo=True),
    Salon(23.0, tiene_sofa=True, tiene_televisor=True)
]
habitaciones_casa5 = [
    Dormitorio(17.0, tiene_cama=True, tiene_lampara=True),
    Dormitorio(14.0, tiene_cama=True),
    Cocina(11.0, tiene_frigorifico=True, tiene_horno=True),
    Banyo(7.0, tiene_banyera=True, tiene_lavabo=True),
    Salon(26.0, tiene_sofa=True, tiene_televisor=True)
]

piso1 = Piso(
    nombre="Piso Luminoso",
    descripcion="Piso céntrico con buenas vistas",
    habitaciones=habitaciones_piso1,
    precio=180000,
    zona=zonas["centro_madrid"],
    duenyo=vendedores[0],
    direccion="Calle Mayor, 1",
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
    direccion="Avenida de la Paz, 45",
    planta=5,
    ascensor=False
)
piso3 = Piso(
    nombre="Piso Familiar",
    descripcion="Ideal para familias con niños",
    habitaciones=habitaciones_piso3,
    precio=165000,
    zona=zonas["casco_toledo"],
    duenyo=vendedores[4],
    direccion="Calle Toledo, 10",
    planta=2,
    ascensor=True
)
piso4 = Piso(
    nombre="Piso Equipado",
    descripcion="Perfecto para parejas jóvenes",
    habitaciones=habitaciones_piso4,
    precio=195000,
    zona=zonas["rural_asturias"],
    duenyo=vendedores[1],
    direccion="Calle del Río, 20",
    planta=4,
    ascensor=True
)

piso5 = Piso(
    nombre="Piso Económico",
    descripcion="Buena opción para inversión",
    habitaciones=habitaciones_piso5,
    precio=145000,
    zona=zonas["sur_madrid"],
    duenyo=vendedores[3],
    direccion="Calle de la Libertad, 30",
    planta=1,
    ascensor=False
)


casa1 = ViviendaUnifamiliar(
    duenyo=vendedores[1],
    descripcion="Casa unifamiliar con jardín y piscina",
    precio=350000,
    nombre="Casa Rural",
    habitaciones=habitaciones_casa1,
    zona=zonas["norte_madrid"],
    direccion="Calle del Bosque, 5",
    tiene_piscina=True,
    jardin=None
)
casa2 = ViviendaUnifamiliar(
    duenyo=vendedores[3],
    descripcion="Chalet adosado en zona residencial tranquila",
    precio=420000,
    nombre="Chalet Tranquilo",
    habitaciones=habitaciones_casa2,
    zona=zonas["residencial_sevilla"],
    direccion="Calle de la Paz, 15",
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
    direccion="Calle del Sol, 25",
    tiene_piscina=True,
    jardin="Gran patio con árboles frutales"
)
casa4 = ViviendaUnifamiliar(
    duenyo=vendedores[2],
    descripcion="Casa moderna con terraza y garaje",
    precio=410000,
    nombre="Casa Moderna",
    habitaciones=habitaciones_casa4,
    zona=zonas["centro_madrid"],
    direccion="Calle de la Libertad, 12",
    tiene_piscina=False,
    jardin="Terraza amplia con vistas"
)

casa5 = ViviendaUnifamiliar(
    duenyo=vendedores[4],
    descripcion="Casa rústica con encanto natural",
    precio=370000,
    nombre="Casa Rústica",
    habitaciones=habitaciones_casa5,
    zona=zonas["rural_asturias"],
    direccion="Calle del Campo, 8",
    tiene_piscina=True,
    jardin="Jardín con vegetación autóctona"
)


# Añadir inmuebles a las zonas correspondientes
zonas["centro_madrid"].agregar_inmueble(piso1)
zonas["rural_asturias"].agregar_inmueble(casa5)

zonas["norte_madrid"].agregar_inmueble(casa1)
zonas["norte_madrid"].agregar_inmueble(casa3)

zonas["sur_madrid"].agregar_inmueble(piso2)
zonas["sur_madrid"].agregar_inmueble(piso5)
zonas["centro_madrid"].agregar_inmueble(casa4)

zonas["rural_asturias"].agregar_inmueble(piso4)
zonas["residencial_sevilla"].agregar_inmueble(casa2)

zonas["casco_toledo"].agregar_inmueble(piso3)

# Lista de inmuebles para trabajar
inmuebles = [piso1, casa1, piso2, casa2, piso3, casa3, piso4, casa4, piso5, casa5]


