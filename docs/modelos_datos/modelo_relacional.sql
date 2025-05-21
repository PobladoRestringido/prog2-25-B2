CREATE TABLE IF NOT EXISTS Usuario (
    nombre VARCHAR(50),
    contrasenya VARCHAR(100),
    PRIMARY KEY (nombre)
);

        CREATE TABLE IF NOT EXISTS Comprador (
            nombre VARCHAR(50),
            PRIMARY KEY (nombre),
            FOREIGN KEY (nombre) REFERENCES Usuario(nombre)
        );

        CREATE TABLE IF NOT EXISTS Vendedor (
            nombre VARCHAR(50),
            PRIMARY KEY (nombre),
            FOREIGN KEY (nombre) REFERENCES Usuario(nombre)
        );

        CREATE TABLE IF NOT EXISTS Administrador (
            nombre VARCHAR(50),
            PRIMARY KEY (nombre),
            FOREIGN KEY (nombre) REFERENCES Usuario(nombre)
        );

CREATE TABLE IF NOT EXISTS Inmueble (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zona VARCHAR(50),
    nombre_propietario VARCHAR(50),
    FOREIGN KEY (nombre_propietario) REFERENCES Usuario(nombre)
);

        CREATE TABLE IF NOT EXISTS Piso (
            id_inmueble INT(11),
            ascensor VARCHAR(8),
            planta INT(2),
            puerta INT(2),
            PRIMARY KEY (id_inmueble),
            FOREIGN KEY (id_inmueble) REFERENCES Inmueble(id)
        );

        CREATE TABLE IF NOT EXISTS ViviendaUnifamiliar (
            id_inmueble INT(11),
            piscina BIT(1),
            superficie_jardin DECIMAL(12, 2),
            PRIMARY KEY (id_inmueble),
            FOREIGN KEY (id_inmueble) REFERENCES Inmueble(id)
        );

CREATE TABLE IF NOT EXISTS InteresInmuebles (
    nombre_comprador VARCHAR(50),
    id_inmueble INT(11),
    PRIMARY KEY (nombre_comprador, id_inmueble),
    FOREIGN KEY (nombre_comprador) REFERENCES Comprador(nombre),
    FOREIGN KEY (id_inmueble) REFERENCES Inmueble(id)
);

CREATE TABLE IF NOT EXISTS Publicacion (
    id INT(11),
    precio_listado DECIMAL(12, 2),
    descripcion VARCHAR(500),
    fecha TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Comentario (
    id INT(11),
    fecha TIMESTAMP,
    contenido VARCHAR(500),
    nombre_comprador VARCHAR(50),
    id_publicacion INT(11),
    PRIMARY KEY (id, id_publicacion),
    FOREIGN KEY (nombre_comprador) REFERENCES Comprador(nombre),
    FOREIGN KEY (id_publicacion) REFERENCES Publicacion(id)
);

CREATE TABLE IF NOT EXISTS SeOfertaEn (
    id_publicacion INT(11),
    id_inmueble INT(11),
    PRIMARY KEY (id_publicacion),
    FOREIGN KEY (id_publicacion) REFERENCES Publicacion(id),
    FOREIGN KEY (id_inmueble) REFERENCES Inmueble(id)
);

CREATE TABLE IF NOT EXISTS Habitacion (
    id INT(11),
    id_inmueble INT(11),
    superficie DECIMAL(12, 2),
    PRIMARY KEY (id, id_inmueble),
    FOREIGN KEY (id_inmueble) REFERENCES Inmueble(id)
);

        CREATE TABLE IF NOT EXISTS Salon (
            id_habitacion INT(11),
            id_inmueble INT(11),
            televisor BIT(1),
            sofa BIT(1),
            mesa_recreativa BIT(1),
            PRIMARY KEY (id_habitacion, id_inmueble),
            FOREIGN KEY (id_habitacion, id_inmueble) REFERENCES Habitacion(id, id_inmueble)
        );

        CREATE TABLE IF NOT EXISTS Banyo (
            id_habitacion INT(11),
            id_inmueble INT(11),
            ducha BIT(1),
            banyera BIT(1),
            lavabo BIT(1),
            vater BIT(1),
            PRIMARY KEY (id_habitacion, id_inmueble),
            FOREIGN KEY (id_habitacion, id_inmueble) REFERENCES Habitacion(id, id_inmueble)
        );

        CREATE TABLE IF NOT EXISTS Cocina (
            id_habitacion INT(11),
            id_inmueble INT(11),
            frigorifico BIT(1),
            horno BIT(1),
            microondas BIT(1),
            fregadero BIT(1),
            mesa BIT(1),
            PRIMARY KEY (id_habitacion, id_inmueble),
            FOREIGN KEY (id_habitacion, id_inmueble) REFERENCES Habitacion(id, id_inmueble)
        );

        CREATE TABLE IF NOT EXISTS Dormitorio (
            id_habitacion INT(11),
            id_inmueble INT(11),
            frigorifico BIT(1),
            cama BIT(1),
            lampara BIT(1),
            mesa_estudio BIT(1),
            PRIMARY KEY (id_habitacion, id_inmueble),
            FOREIGN KEY (id_habitacion, id_inmueble) REFERENCES Habitacion(id, id_inmueble)
        );
