from django.db import models
from django.contrib.auth.models import User
from .lib.roles.rol import Roles

# Create your models here.
class Rol(models.Model):
    rol = models.CharField(max_length=20, choices=Roles, verbose_name='Rol')

    def __str__(self):
        return f"${self.rol}"

    class Meta:
        db_table = 'TipoUsuario'

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='photos', blank=True, null=False)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    cedula = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'${self.usuario} - ${self.rol}'

    class Meta:
        db_table = 'Usuario'

