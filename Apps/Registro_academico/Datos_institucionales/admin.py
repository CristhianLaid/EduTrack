from django.contrib import admin
from .models import Carrera, Inscripcion, Asignatura, Curso
# Register your models here.
admin.site.register(Carrera)
admin.site.register(Asignatura)
admin.site.register(Curso)
admin.site.register(Inscripcion)