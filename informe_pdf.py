# informe_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class InformePDF():

    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def generar_informe(self, inmuebles):
        c = canvas.Canvas(self.nombre_archivo, pagesize=A4)
        x.setTitle("Informe de Inmuebles")

        # Encabezado
        c.setFont("Helvetica-Bold", 18)
        c.drawString(100, 800, "Informe de Inmuebles")

        # Línea divisoria
        c.line(100, 795, 500, 795)

        # Listado de inmuebles
        c.setFont("Helvetica", 12)
        y_pos = 770

        for idx, inmueble in enumerate(inmuebles, start=1):
            c.drawString(100, y_pos, f"{idx}.{inmueble.nombre}")
            y_pos -= 15

            # Salto de página si no cabe más textp
            if y_pos < 50:
                c.showPage() # crear pagina
                y_pos = 800 # reiniciar posicion y
                c.setFont("Helvetica", 12) # restaurar fuente

        # guardar pdf
        c.save()
        print(f"Informe generado exitosamente: {self.nombre_archivo}")