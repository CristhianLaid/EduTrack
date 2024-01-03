from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from Apps.ReconocimientoFacial.RegistroRostro.ReconocimientoFacial import ReconocimientoFacial
from . import models
from .forms import RegistroAsistenciaForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ...Usuario.models import Inscripcion


# Create your views here.
class RegistroAsistenciaAutomatizada(View):
    # template_name = 'asistencia/registrarAsistenciaAutomatizada.html'

    def get(self, request, *args, **kwargs):
        idcurso = request.GET.get('curso_id')

        ReconocimientoFacialAsistencia = ReconocimientoFacial('Apps/ReconocimientoFacial/RegistroRostro/data', 'modeloLBPHFace.xml', idcurso)
        ReconocimientoFacialAsistencia.reconocimiento()

        messages.success(request, 'Asistencia registrada exitosamente.')

        # return render(request, self.template_name)
        return redirect('ViewAttendance')

@method_decorator(login_required, name='dispatch')
class VisualizarAsistencia(View):
    template_name = 'asistencia/visualizarAsistencia.html'
    idcurso = None

    def get(self, request, *args, **kwargs):
        try:
            self.idcurso = request.GET.get('curso_id')
            user = request.user.usuario
            inscripcion = Inscripcion.objects.get(usuario=user, curso=self.idcurso)

            # Obtener todos los registros de asistencia para el curso
            asistencia = models.RegistroAsistencia.objects.filter(usuario__cursos=inscripcion.curso)
            fechas_asistencia = asistencia.values('fecha_asistencia').distinct()
            print(fechas_asistencia)
            form = RegistroAsistenciaForm(instance=asistencia.first())

            context = {
                'asistencia': asistencia,
                'inscripcion': inscripcion,
                'fechas_asistencia': fechas_asistencia,
                'form': form,
            }
            return render(request, self.template_name, context)
        except Inscripcion.DoesNotExist:
            context = {'error': 'No hay registros de asistencia para este curso.'}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.idcurso = request.POST.get('curso_id')
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            # Obtener el ID del registro de asistencia a actualizar
            registro_id = request.POST.get('registro_id')
            try:
                print(registro_id)
                registro = models.RegistroAsistencia.objects.get(id=registro_id)
                # Actualizar el campo 'tipo' con el nuevo valor del formulario
                registro.tipo = form.cleaned_data['tipo']
                registro.estado_asistencia = form.cleaned_data['estado_asistencia']
                registro.save()
            except models.RegistroAsistencia.DoesNotExist:
                messages.success(request, 'No se puede editar.')

        return redirect('ViewAttendance')


