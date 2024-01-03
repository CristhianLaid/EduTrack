from django.db import models

from Apps.Usuario.models import Usuario


# Create your models here.

class TipoRegistro(models.Model):
    tipo_registro = models.CharField(max_length=250, choices=[('Manual', 'Manual'),
                                                              ('Automatico', 'Automatico')])
    class Meta:
        db_table='TipoRegistro'

    def __str__(self):
        return f'{self.tipo_registro}'

class RegistroAsistencia(models.Model):
    class Evento(models.TextChoices):
        CLASE = 'Clase', 'Clase'
        REUNION = 'Reunion', 'Reunion'
        CONFERENCIA = 'Conferencia', 'Confrencia'

    class EstadoAsistencia(models.TextChoices):
        A_TIEMPO = 'A Tiempo', 'A Tiempo'
        ATRASADO = 'Atrasado', 'Atrasado'
        ASISTENCIA_COMPLETA = 'Asistencia Completa', 'Asistencia Completa'
        MEDIA_ASISTENCIA = 'Media Asistencia', 'Media Asistencia'
        SIN_REGISTRO = 'Sin Registro', 'Sin Registro'

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoRegistro, on_delete=models.CASCADE)
    curso = models.CharField(max_length=250, null=True)
    fecha_asistencia = models.DateField()
    hora_asistencia = models.TimeField()
    hora_salida = models.TimeField(null=True, blank=True)
    evento = models.CharField(max_length=20, choices=Evento.choices)
    estado_asistencia = models.CharField(max_length=50, choices=EstadoAsistencia.choices, default=EstadoAsistencia.SIN_REGISTRO)


    class Meta:
        db_table='RegistroAsistencia'

    def __str__(self):
        return f'{self.usuario} - {self.evento} - {self.fecha_asistencia}'