from django.db import models
from django.contrib.auth.models import User
from .lib.roles.rol import Roles
from ..Registro_academico.Datos_institucionales.models import Curso


# Create your models here.
class Rol(models.Model):
    rol = models.CharField(max_length=20, choices=Roles, verbose_name='Rol')

    def __str__(self):
        return f"${self.rol}"

    class Meta:
        db_table = 'TipoUsuario'

class Facultad(models.Model):
    nombreFacultad = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return f'{self.nombreFacultad}'
    class Meta:
        db_table = 'Facultad'

class Carrera(models.Model):
    nombreCarrera = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.nombreCarrera}'

    class Meta:
        db_table= 'Carrera'

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='photos', blank=True, null=False)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    cedula = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, null=True)
    cursos = models.ManyToManyField(Curso, through='Inscripcion', related_name='cursos_usuario')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.usuario}'

    class Meta:
        db_table = 'Usuario'

class Inscripcion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    facultad = models.TextField(max_length=250,  null=True)


    class Meta:
        db_table='Inscripcion'

    def __str__(self):
        return f'{self.usuario}-{self.curso}'