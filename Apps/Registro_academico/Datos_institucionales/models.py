from django.db import models
from Apps.Usuario.models import Usuario

# Create your models here.

class Facultad(models.Model):
    nombreFacultad = models.CharField(max_length=100)

class Carrera(models.Model):
    nombreCarrera = models.CharField(max_length=100)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE)

class Aignatura(models.Model):
    nombreAsignatura = models.CharField(max_length=100)

class Curso(models.Model):
    nombreCurso = models.CharField(max_length=100)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Aignatura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)