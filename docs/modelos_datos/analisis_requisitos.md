**Autor:** Pablo Reig
**Fecha:** 2 mayo 2025

# Análisis de requisitos

La base de datos guardará información sobre los usuarios y los inmuebles.
De cada usuario se conocerá su nombre de usuario, que servirá para
identificarlo, y su contraseña. De cada inmueble se conocerá su id, que
será único, su nombre, su descripción, su precio y la zona geográfica a la
que pertenece.

Existirán varios tipos de usuarios: compradores, vendedores y
administradores. De los compradores se conocerán los comentarios que han
dejado, así como los inmuebles que les interesan y los que han adquirido.
De los vendedores se conocerán las publicaciones que han creado, así como
los inmuebles que les pertenecen. De los administradores no se necesitará
información adicional.

Asimismo existirán varios tipos de inmueble: pisos y viviendas 
unifamiliares. De los pisos se guardará la planta en la que están, así como 
información adicional que ayude a identificarlos (puerta, ascensor, etc.). 
De las viviendas unifamiliares se guardará si tienen piscina, e información 
sobre su jardín.

Cada inmueble tendrá una lista de habitaciones, de las cuales también 
querremos guardar información. Cada habitación se identificará por un id, 
el cual será único en relación al inmueble al que pertenecen. También 
querremos conocer la superficie (en $m^2$) de cada habitación.
Habrá varios tipos de habitaciones, de los cuales querremos información 
adicional: salones, baños, cocinas y dormitorios. De cada salón querremos 
saber si tiene televisor, si tiene sofá y si tiene alguna mesa recreativa. 
De los baños, querremos saber si tienen ducha, bañera, lavabo o váter. De 
las cocinas, querremos saber si tienen frigorífico, horno, microondas, 
fregadero o mesa. De los dormitorios, querremos conocer si tienen cama, 
lámpara y/o mesa de estudio.
