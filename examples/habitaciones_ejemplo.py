from modelos.habitacion.dormitorio import Dormitorio
from modelos.habitacion.cocina import Cocina
from modelos.habitacion.banyo import Banyo
from modelos.habitacion.salon import Salon

# 🛏 Dormitorios
dormitorio1 = Dormitorio(12.5, tiene_cama=True, tiene_mesa_estudio=True)
dormitorio2 = Dormitorio(10.0, tiene_cama=True, tiene_lampara=True)
dormitorio3 = Dormitorio(14.2, tiene_cama=True, tiene_mesa_estudio=False)
dormitorio4 = Dormitorio(8.0)

# 🍳 Cocinas
cocina1 = Cocina(9.5, tiene_frigorifico=True, tiene_fregadero=True, tiene_horno=True)
cocina2 = Cocina(11.0, tiene_frigorifico=True, tiene_microondas=True, tiene_mesa=True)
cocina3 = Cocina(7.8)

# 🚿 Baños
banyo1 = Banyo(6.0, tiene_ducha=True, tiene_lavabo=True, tiene_vater=True)
banyo2 = Banyo(7.0, tiene_banyera=True, tiene_vater=True)
banyo3 = Banyo(5.5)

# 🛋 Salones
salon1 = Salon(16.0, tiene_televisor=True, tiene_sofa=True)
salon2 = Salon(20.0, tiene_sofa=True, tiene_mesa_recreativa=True)
salon3 = Salon(12.0)

# Combinaciones útiles para inmuebles
habitaciones_piso1 = [dormitorio1, cocina1, banyo1, salon1]
habitaciones_piso2 = [dormitorio2, cocina2, banyo2, salon2]
habitaciones_casa1 = [dormitorio3, cocina3, banyo3, salon3, dormitorio4]

# Exportar listas si quieres importar muchas de golpe
todas_las_habitaciones = habitaciones_piso1 + habitaciones_piso2 + habitaciones_casa1
