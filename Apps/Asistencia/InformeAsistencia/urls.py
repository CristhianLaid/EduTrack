from django.urls import path
from .views import generar_informe_pdf

urlpatterns = [
    # Otras URL de tu aplicación
    path('generar-informe-pdf/', generar_informe_pdf, name='generar_informe_pdf'),
]