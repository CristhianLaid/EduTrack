from django.db import models
# Create your models here.



class Asignatura(models.Model):
    nombreAsignatura = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombreAsignatura}'

    class Meta:
        db_table = 'Asignatura'

class Curso(models.Model):
    nombreCurso = models.CharField(max_length=100, blank=False)
    carrera = models.CharField(max_length=150, null=True)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, blank=False)
    descripcion = models.TextField(max_length=250, blank=False, null=True)
    horaEntrada = models.TimeField(help_text="Hora de inicio del curso", null=True, blank=True)
    horaSalida = models.TimeField(help_text="Hora de salida del curso", null=True, blank=True)
    def __str__(self):
        return f'{self.nombreCurso} - {self.carrera} - {self.asignatura}'

    class Meta:
        db_table = 'Curso'

