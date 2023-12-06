from django.contrib import admin
from .models import Rol, Usuario, Facultad, Inscripcion, Carrera

# Register your models here.
admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Facultad)
admin.site.register(Inscripcion)
admin.site.register(Carrera)