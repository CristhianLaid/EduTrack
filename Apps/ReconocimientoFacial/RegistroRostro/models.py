# models.py
from django.db import models
from django.utils import timezone

from Apps.Usuario.models import Usuario


class RegistroRostro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(default=timezone.now)
    foto_rostro = models.ImageField(upload_to='registros_rostro')

    def __str__(self):
        return f'Registro de {self.usuario} - {self.fecha_registro}'

