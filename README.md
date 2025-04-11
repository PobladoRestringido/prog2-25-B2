# PROG2-25-B2
La más maravillosa API de gestión de una inmobiliaria de la historia.

## Autores
* (Coordinador) [Pablo Reig Sánchez](https://github.com/PobladoRestringido)
* [Adrián Díez Agulló](https://github.com/Adrian-Diez-Agullo)
* [Lucía Monteagudo Castellanos](https://github.com/Luciamcs)
* [David Muñoz Torró](https://github.com/oppangangnamsta)
* [Blanca Xifra Melendo](https://github.com/blancaxifra)
* [Sama Al Adib Hawari](https://github.com/Sama14b)

## Profesor
[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
[//]: # (Indicad aquí los requisitos de vuestra aplicación, así como el alumno responsable de cada uno de ellos)

* Permitirá descargar una foto del mapa de la zona seleccionada (haciendo uso de la API de Google Maps). (Adrian Díez) 

* Redirigirá al usuario directamente a la url correspondiente de Google Maps, si éste así lo desea. (Sama Al Adib) 

* Permitirá al usuario filtrar los distintos inmuebles especificando características como el precio, la zona, el tamaño, tipo de alquiler, capacidad (en personas), etc. (Blanca Xifra) 

* Permitirá al usuario iniciar sesión y registrarse. (Blanca Xifra) 

* Generará reseñas automáticamente haciendo uso de una IA generativa (API de deepseek/openAI). (Lucia M) 

* Permitirá al usuario escribir sus propias reseñas. (Sama Al Adib) 

* Accederá a la API de alguna otra inmobiliaria/red social para mostrar y guardar precios reales. (Adrian Díez) 

* Almacenará toda la información relativa a los inmuebles, los usuarios y las reseñas en una base de datos relacional. (Pablo Reig) 

* Expondrá una API de consultas de inmuebles. (Lucia M)   

* Emitirá informes en formato PDF de los inmuebles guardados, con fotografía incluída. (David Muñoz) 

* Permitirá conceder y revocar permisos a los distintos usuarios del sistema (compradores/vendedores, administradores), controlando el nivel de seguridad de los usuarios. (David Muñoz)

## Instrucciones de instalación y ejecución
[//]: # (Indicad aquí qué habría que hacer para ejecutar vuestra aplicación)
*Under construction*

## Resumen de la API
[//]: # (Cuando tengáis la API, añadiréis aquí la descripción de las diferentes llamadas.)
[//]: # (Para la evaluación por pares, indicaréis aquí las diferentes opciones de vuestro menú textual, especificando para qué sirve cada una de ellas)
*Nuestra API dispone de varias funciones:
*-Permite al usuario registrarse e iniciar sesión (iniciar_sesion,registrar_usuario)
*-Permite consultar los inmuebles, ya sea para ver el total de estos o si queremos filtrar por id y ver uno en especifico(get_inmuebles,get_inmueble_id)
*-Permite poder eliminar, actualizar o añadir un inmueble(anyadir_inmuebles,actualizar_inmueble,eliminar_inmueble)
*-Permite ver los comentarios que hay sobre un inmueble y el tipo de inmueble que es (mostrar_comentarios)
*-Permite hacer tu propio comentario y mostrarlo en los comentarios del inmueble elegido(escribir_comentario)
