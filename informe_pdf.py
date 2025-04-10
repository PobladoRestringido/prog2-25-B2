# informe_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class InformePDF():
    """
    Una clase usaada para crear un objeto informe que luego se puede usar para generar un informe PDF a partir de una lista de inmuebles

    Atributos
    ---------
    nombre_archivo : str
        el nombre del archivo

    Métodos
    -------
    generar_informe(inmuebles : list)
        Genera un informe PDF en base a una lista de inmuebles proporcionada
    """
    def __init__(self, nombre_archivo : str = 'informe'):
        """
        Parámetros
        nombre_archivo : str
            El nombre del archivo
        """
        self.nombre_archivo = nombre_archivo

    def generar_informe(self, inmuebles : list):
        """
        Genera el informe con la lista de inmuebles proporcionada

        Parámetros
        ----------
        inmuebles : list
            Lista de objetos de tipo Inmueble
        """
        c = canvas.Canvas(self.nombre_archivo, pagesize=A4)
        c.setTitle("Informe de Inmuebles")

        # Encabezado
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 800, "Informe de Inmuebles")

        # Línea divisoria
        c.line(100, 795, 500, 795)

        # Listado de inmuebles
        c.setFont("Helvetica", 12)
        y_pos = 770

        for idx, inmueble in enumerate(inmuebles, start=1):
            c.drawString(100, y_pos, f"{idx}.{inmueble}")
            y_pos -= 15

            # Salto de página si no cabe más texto
            if y_pos < 50:
                c.showPage()
                y_pos = 800
                c.setFont("Helvetica", 12)

        # guardar pdf
        c.save()
        print(f"Informe generado exitosamente: {self.nombre_archivo}")