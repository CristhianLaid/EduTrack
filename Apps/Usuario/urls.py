from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterPerfilRostro, name='EditPerfilRostro'),
    path('login/', views.Login, name='login'),
    path('register/', views.Register, name='register'),
    path('logout/', views.Logout, name='logout'),
    path('perfil/', views.ViewUsuario, name='perfil'),
    # path('asistencia', )
]