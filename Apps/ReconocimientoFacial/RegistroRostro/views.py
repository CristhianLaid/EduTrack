import os
import cv2
import numpy as np
from django.http import StreamingHttpResponse
from .entrenamiento import Entrenar
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseServerError
from .capturandoRostros import CapturaRostro
from django.http import JsonResponse
from django.views import View
from .ReconocimientoFacial import ReconocimientoFacial
from .models import RegistroRostro
@method_decorator(login_required, name='dispatch')
class CapturaRostroView(View):
    template_name = 'registroRostro.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        person_name = request.user.username  # O request.user.username según lo que necesites

        if person_name:
            captura = CapturaRostro(person_name)
            count = captura.capturar()

            if count > 0:
                usuario = request.user.usuario
                for i in range(count):
                    foto_rostro = f'{person_name}/rostro_{i}.jpg'
                    registro = RegistroRostro(usuario=usuario, foto_rostro=foto_rostro)
                    registro.save()
                    data_path = 'Apps/ReconocimientoFacial/RegistroRostro/data'
                    entrenamiento = Entrenar(data_path)
                    entrenamiento.hacerEntrenamiento()
                return redirect('perfil')  # Ajusta la redirección según tus necesidades
        return render(request, self.template_name)

# @method_decorator(login_required, name='dispatch')
# class CapturaRostroView(View):
#     template_name = 'registroRostro.html'
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)
#
#     def post(self, request, *args, **kwargs):
#         print("Solicitud POST recibida")  # Agrega mensajes de registro
#         person_name = request.user.username
#         capturador_rostro = CapturaRostro(person_name)
#         success = capturador_rostro.capturar()
#
#         if success:
#             print("Captura exitosa")  # Más mensajes de registro
#             return JsonResponse({'status': 'Captura exitosa'})
#         else:
#             print("Error en la captura")  # Más mensajes de registro
#             return JsonResponse({'status': 'Error en la captura'})

