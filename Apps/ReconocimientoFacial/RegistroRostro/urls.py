from django.urls import path
from .views import CapturaRostroView


urlpatterns = [
    path('capturar_rostro/', CapturaRostroView.as_view(), name='capturar_rostro')
]
