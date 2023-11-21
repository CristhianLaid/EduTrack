from django.forms import ModelForm
from django import forms
# from django.contrib.auth.models import User
from .models import Usuario
from .lib.roles.rol import Roles
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class RegisterUserForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['telefono', 'cedula', 'direccion', 'foto']

class CustomUserChangeForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class RegisterAuthForm(forms.Form):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50, label='Password')
    password2 = forms.CharField(max_length=50, label= 'Confirmar Contraseña')
    rol = forms.ChoiceField(choices=Roles)