# Autor: Pablo Reig Sánchez
# Fecha: 19 - 05 - 25

"""
El propósito de este fichero es crear la base de datos a partir del modelo
relacional en ``docs/modelos_datos/modelo_relacional.sql``. Solo está
pensado para ser ejecutado una vez.
"""

import sqlite3

conn = sqlite3.connect("base_datos.db")
cursor = conn.cursor()

with open("../docs/modelos_datos/modelo_relacional.sql", "r") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.commit()
conn.close()
