from django.shortcuts import render, redirect
from .forms import RegisterUserForm, RegisterAuthForm, CustomUserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Usuario, Rol
from django.db import IntegrityError

# Create your views here.
def Login(request):
    if request.method == 'GET':
        return render(request, 'seccion/login.html', {'login': AuthenticationForm})
    AuthUser = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if AuthUser is None:
        return render(request, 'seccion/login.html', {'login': AuthenticationForm, 'error': 'Usuario no encontrado'})
    try:
        print(AuthUser)
        login(request, AuthUser)

        return redirect('perfil')
    except:
        return render(request, 'seccion/login.html', {'login': AuthenticationForm, 'error': 'Error en la base de datos'})

def Register(request):
    if request.method == 'GET':
        return render(request, 'seccion/register.html', {'register': RegisterAuthForm})

    if request.POST['password1'] != request.POST['password2']:
        return render(request, 'seccion/register.html', {'register': RegisterAuthForm, 'error': 'Invalid password'})

    if User.objects.filter(email=request.POST['email']).exists():
        return render(request, 'seccion/register.html', {'register': RegisterAuthForm, 'error': 'Ingrese otro email'})
    try:
        Auth = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password1']
        )
        rolUser = Rol.objects.get(rol=request.POST['rol'])
        user = Usuario.objects.create(usuario=Auth, rol=rolUser)
        user.save()
        login(request, Auth)
        return redirect('perfil')

    except IntegrityError:
        return render(request, 'seccion/register.html', {'register': RegisterAuthForm, 'error': 'Ponga otro Username'})

def Logout(request):
    logout(request)
    return redirect('login')

@login_required
def RegisterPerfilRostro(request):
    user = request.user.usuario
    registerUserFrom = RegisterUserForm(request.POST, request.FILES, instance=user)
    customUserFrom = CustomUserChangeForm(request.POST, instance=request.user)

    if request.method == 'GET':
        return render(request, 'registroPerfilRostro/registroPerfilRostro.html', {'forms': registerUserFrom, 'formsUser': customUserFrom})
    else:
        try:
            if registerUserFrom.is_valid() and customUserFrom.is_valid():
                print(registerUserFrom)
                registerUserFrom.save()
                customUserFrom.save()
                return redirect('EditPerfilRostro')

        except:
            return render(request, 'registroPerfilRostro/registroPerfilRostro.html', {'forms': registerUserFrom, 'formsUser': customUserFrom, 'error': 'Error al enviar datos'})

@login_required
def ViewUsuario(request):
    if request.method == 'GET':
        return render(request, 'registroPerfilRostro/viewPerfil.html')
    else:
        return render(request, 'registroPerfilRostro/viewPerfil.html')


