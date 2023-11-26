from django.db import models
from Apps.Usuario.models import Usuario

# Create your models here.



class Carrera(models.Model):
    nombreCarrera = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombreCarrera}'

    class Meta:
        db_table= 'Carrera'

class Asignatura(models.Model):
    nombreAsignatura = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombreAsignatura}'

    class Meta:
        db_table = 'Asignatura'

class Curso(models.Model):
    nombreCurso = models.CharField(max_length=100)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nombreCurso} - {self.carrera} - {self.asignatura}'

    class Meta:
        db_table = 'Curso'

class Inscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        db_table='Inscripcion'

    def __str__(self):
        return f'{self.usuario}-{self.curso}'