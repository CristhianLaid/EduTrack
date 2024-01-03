from django.urls import path
from .views import RegistroAsistenciaAutomatizada, VisualizarAsistencia

urlpatterns = [
    path('VisualizarAsistencia/', VisualizarAsistencia.as_view(), name='ViewAttendance'),
    path('registrar_asistencia_automatizada/', RegistroAsistenciaAutomatizada.as_view(), name='registrar_asistencia_automatizada')
]