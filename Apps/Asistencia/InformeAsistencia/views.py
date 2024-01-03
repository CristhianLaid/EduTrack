# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Image
from datetime import datetime

from Apps.Asistencia.RegistroAsistencia.models import RegistroAsistencia
from Apps.Registro_academico.Datos_institucionales.models import Curso
from Apps.Usuario.models import Inscripcion


def obtener_fecha_actual():
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    return fecha_actual

def generar_informe_pdf(request):
    # Obtener el curso_id de la solicitud
    curso_id = request.GET.get('curso_id')

    # Obtener el usuario y la inscripción
    user = request.user.usuario
    inscripcion = get_object_or_404(Inscripcion, usuario=user, curso=curso_id)

    # Obtener todos los registros de asistencia para el curso
    asistencia = RegistroAsistencia.objects.filter(usuario__cursos=inscripcion.curso)
    fechas_asistencia = asistencia.values('fecha_asistencia').distinct()

    # Lógica para generar el informe en PDF
    def generar_informe(asistencia, fecha, response):
        pdf_filename = f"informe_asistencia_{fecha}.pdf"
        c = canvas.Canvas(response, pagesize=letter)

        # Título del PDF
        titulo = "Informe de asistencia automatizada"
        c.setFont("Helvetica-Bold", 16)
        titulo_ancho = c.stringWidth(titulo)
        c.drawString((letter[0] - titulo_ancho) / 2, 750, titulo)

        # Crear tabla con las nuevas columnas "Tipo" y "Estado"
        data = [["Foto", "Nombre", "Curso", "Hora de entrada", "Hora de salida", "Tipo", "Estado"]]
        for registro in asistencia:
            imagen_path = registro.usuario.foto.path if registro.usuario.foto else ""
            imagen = Image(imagen_path, width=50, height=50) if imagen_path else ""

            # Asegúrate de que registro.curso sea un objeto Curso
            if isinstance(registro.curso, Curso):
                nombre_curso = registro.curso.nombreCurso
            else:
                nombre_curso = registro.curso  # Puedes ajustar esto según cómo esté definido tu modelo

            data.append([
                imagen,
                f"{registro.usuario.usuario.username} ({registro.usuario.usuario.first_name} {registro.usuario.usuario.last_name})",
                nombre_curso,
                registro.hora_asistencia,
                registro.hora_salida if registro.hora_salida else "",
                registro.tipo.tipo_registro,
                registro.estado_asistencia
            ])

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),  # Añadir bordes
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),  # Añadir bordes
            ('BOTTOMPADDING', (0, 0), (-1, 0), 20),  # Ajustar espaciado
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Aumentar el grosor de los bordes
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),  # Reducir el grosor de los bordes internos
            ('CELLSPACING', (0, 0), (-1, -1), 0),
        ])

        t = Table(data)
        t.setStyle(style)
        

        # Dibujar tabla en PDF con altura dinámica
        width, height = letter
        table_height = t.wrapOn(c, width, height)[1]  # Obtener la altura de la tabla después del ajuste

        max_table_height = 650  # Altura máxima para la tabla

        style.add('ALIGN', (0, 0), (-1, -1), 'CENTER')
        style.add('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        style.add('LEFTPADDING', (0, 0), (-1, -1), 6)  # Aumentar el espaciado izquierdo
        style.add('RIGHTPADDING', (0, 0), (-1, -1), 6)  # Aumentar el espaciado derecho

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
        c.drawCentredString(letter[0] / 2, 700, f"Fecha: {fecha}")
        # Guardar el PDF y cerrar
        c.save()
        print(f"Informe de asistencia generado: {pdf_filename}")

    fecha_actual = obtener_fecha_actual()

    # Crear una respuesta HTTP con el contenido del PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="informe_asistencia_{fecha_actual}.pdf"'

    # Llamar a la función para generar el informe y pasar la respuesta HTTP
    generar_informe(asistencia, fecha_actual, response)

    # Devolver la respuesta
    return response
