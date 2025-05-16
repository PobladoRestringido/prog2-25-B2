**Autor:** Pablo Reig
**Fecha:** 2 mayo 2025

# Análisis de requisitos

_(La **NEGRITA** en mayúsculas indica conjuntos de entidades. El texto en 
``bloques`` de
código indica atributos. La **negrita** en cursiva indica relaciones)._

La base de datos guardará información sobre los usuarios e inmuebles de nuestra
aplicación.

De cada **USUARIO** se conocerá su ``nombre`` de usuario, que servirá para
identificarlo, y su ``contraseña``. También querremos conocer _**los 
inmuebles de los 
que son propietarios**_.
Existirán varios tipos de **USUARIO**: compradores, vendedores y
administradores. De los **COMPRADORES** se conocerán _**los comentarios que han
dejado**_, así como **_los inmuebles que les interesan_** y . De
los **VENDEDORES** se conocerán **_las publicaciones que han creado_**. De los **ADMINISTRADORES** no se necesitará
información adicional.

De cada **INMUEBLE** se conocerá su ``id``, que será único, **_las
habitaciones que lo conforman_** y la ``zona`` geográfica a la que pertenece.

Asimismo existirán varios tipos de inmueble: pisos y viviendas unifamiliares.
De los **PISOS** se guardará la ``planta`` en la que están, así como
información adicional que ayude a identificarlos (``puerta``, ``ascensor``,
etc.). De las **VIVIENDAS UNIFAMILIARES** se guardará si tienen ``piscina``, e
información sobre su ``jardin``.

Como comentamos, cada inmueble tendrá una lista de **HABITACIONES**, de las
cuales también querremos guardar información. Cada habitación se identificará
por un ``id``, el cual será único relativo al inmueble al que pertenecen (i.e.
dependencia de identificador). También querremos conocer la
``superficie`` (en $m^2$) de cada habitación.

Habrá varios tipos de habitaciones, de los cuales querremos información
adicional: salones, baños, cocinas y dormitorios. De cada **SALÓN**
querremos saber si tiene ``televisor``, si tiene ``sofá`` y si tiene alguna
``mesa_recreativa``. De los **BAÑOS**, querremos saber si tienen ``ducha``,
``bañera``, ``lavabo`` y/o
``váter``. De las **COCINAS**, querremos saber si tienen ``frigorífico``,
``horno``,
``microondas``, ``fregadero`` o ``mesa``. De los **DORMITORIOS**, querremos
conocer si tienen
``cama``, ``lámpara`` y/o ``mesa_de_estudio``.

En cuanto a las **PUBLICACIONES**, cada uno se identificará por un
``identificador`` numérico. También querremos conocer la persona que las ha creado,
así como **_el inmueble que en ella se publicita_**, **_los comentarios dejados bajo
estas_**, y el``precio`` con el que se ha listado el inmueble en la publicación (un inmueble no tiene valor intrínseco, sino que depende del precio que desee
ponerle la persona en cada publicación). Finalmente, también querremos poder
guardar cualquier aclaración o ``descripción`` adicional que el vendedor
considere adecuada, así como la ``fecha`` en la que se creó la publicación.

Del mismo modo, de los **COMENTARIOS** querremos guardar qué usuarios los han
dejado, la ``fecha`` y el ``contenido`` (en texto) de los mismos. Cada
comentario se identificará en función de la publicación a la que pertenecen
(dependencia de identificador).
