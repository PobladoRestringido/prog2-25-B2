from modelos.comentario import Comentario
from examples.comprador_ejemplo import compradores

comentario1 = Comentario(
    contenido="Muy buena ubicación, aunque algo ruidoso.",
    autor=compradores[0],
    fecha_publicacion="2025-05-10"
)

comentario2 = Comentario(
    contenido="Me encantó el barrio y la distribución del piso.",
    autor=compradores[1],
    fecha_publicacion="2025-05-12"
)

# Comentarios para inmueble2 (Casa Norte)
comentario3 = Comentario(
    contenido="El jardín es espectacular, ideal para familias.",
    autor=compradores[2],
    fecha_publicacion="2025-05-15"
)

comentario4 = Comentario(
    contenido="La casa estaba limpia y bien cuidada. Volvería a visitarla.",
    autor=compradores[0],
    fecha_publicacion="2025-05-16"
)
