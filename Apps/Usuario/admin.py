from django.contrib import admin
from .models import Rol, Usuario, Facultad

# Register your models here.
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Facultad)