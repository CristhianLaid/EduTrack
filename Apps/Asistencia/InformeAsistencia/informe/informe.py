from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from datetime import datetime

# Función para obtener la fecha actual
def obtener_fecha_actual():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return fecha_actual

# Función para ingresar los datos
def ingresar_datos():
    asistencia = []
    while True:
        nombre = input("Ingrese el nombre completo (o escriba 'fin' para terminar): ")
        if nombre.lower() == 'fin':
            break
        apellidos = input("Ingrese los apellidos: ")
        curso = input("Ingrese el curso: ")
        hora_entrada = input("Ingrese la hora de entrada: ")
        hora_salida = input("Ingrese la hora de salida: ")
        imagen_path = input("Ingrese la ruta de la imagen (o dejar en blanco si no hay): ")
        tipo = input("Ingrese el tipo: ")
        estado = input("Ingrese el estado: ")

        registro = {
            "Nombre": nombre + " " + apellidos,
            "Curso": curso,
            "Hora_entrada": hora_entrada,
            "Hora_salida": hora_salida,
            "Imagen": imagen_path,
            "Tipo": tipo,
            "Estado": estado
        }
        asistencia.append(registro)

    return asistencia

# Función para generar el informe en PDF
def generar_informe(asistencia, fecha):
    pdf_filename = "informe_asistencia.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Título del PDF
    titulo = "Informe de asistencia automatizada"
    c.setFont("Helvetica-Bold", 16)
    titulo_ancho = c.stringWidth(titulo)
    c.drawString((letter[0] - titulo_ancho) / 2, 750, titulo)

    # Crear tabla con las nuevas columnas "Tipo" y "Estado"
    data = [["Foto", "Nombre", "Curso", "Hora de entrada", "Hora de salida", "Tipo", "Estado"]]
    for registro in asistencia:
        imagen_path = registro["Imagen"]
        imagen = Image(imagen_path, width=50, height=50) if imagen_path else ""
        data.append([
            imagen, registro["Nombre"], registro["Curso"],
            registro["Hora_entrada"], registro["Hora_salida"],
            registro["Tipo"], registro["Estado"]
        ])

    t = Table(data)
    t.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar horizontalmente
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Centrar verticalmente
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white)
    ]))

    # Dibujar tabla en PDF con altura dinámica
    width, height = letter
    table_height = t.wrapOn(c, width, height)[1]  # Obtener la altura de la tabla después del ajuste

    max_table_height = 650  # Altura máxima para la tabla

    if table_height < max_table_height:
        table_y = 650 - table_height  # Ajuste la posición de la tabla si es menor que la altura máxima
        t.drawOn(c, 72, table_y)
    else:
        # La tabla es más grande que la altura máxima
        # Puedes manejar este caso según tu preferencia
        pass  # Aquí puedes implementar la lógica necesaria para este caso

    # Fecha actual encima de la tabla
    c.setFont("Helvetica", 10)
    c.drawString(72, 700, f"Fecha: {fecha}")  # Posición de la fecha encima de la tabla

    # Guardar el PDF y cerrar
    c.save()
    print(f"Informe de asistencia generado: {pdf_filename}")

# Obtener fecha actual y generar el informe
fecha_actual = obtener_fecha_actual()
datos_ingresados = ingresar_datos()
generar_informe(datos_ingresados, fecha_actual)