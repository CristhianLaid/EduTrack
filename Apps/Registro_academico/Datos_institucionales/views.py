from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Curso, Asignatura
from ...Usuario.models import Usuario, Inscripcion, Carrera
from .forms import CreateCourseForm
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def es_profesor(user):
    return user.is_authenticated and user.usuario.rol.rol == 'Profesor'

@login_required
@user_passes_test(es_profesor)
def CreateCourse(request):
    if request.method == 'GET':
        return render(request, 'curso/createCourse.html', {'form': CreateCourseForm})

    try:
        curso = CreateCourseForm(request.POST)
        if curso.is_valid():
            nameCourse = request.POST.get('nombreCurso')
            nameCarrera = request.POST.get('carrera')

            if not Carrera.objects.filter(nombreCarrera=nameCarrera).exists():
                return render(request, 'curso/createCourse.html',
                              {'form': CreateCourseForm,
                               'error': 'No se puede registrar el curso, el nombre de la carrera no se encuentra en las base de la institucion.'})

            if Curso.objects.filter(nombreCurso=nameCourse, carrera=nameCarrera).exists():
                return render(request, 'curso/createCourse.html',
                              {'form': CreateCourseForm,
                               'error': 'No puede ingresar el mismo nombre de curso, ponga otro.'})

            newCurso = curso.save(commit=False)
            newCurso.save()
            newInscription = Inscripcion.objects.create(curso=newCurso, usuario=request.user.usuario,
                                                        facultad=request.user.usuario.facultad.nombreFacultad)
            newInscription.save()
            return redirect('viewsCourse')

        return render(request, 'curso/createCourse.html',
                      {'form': CreateCourseForm, 'error': 'El formulario es invalido'})

    except ValueError:
        return render(request, 'curso/createCourse.html',
                      {'form': CreateCourseForm, 'error': 'Error al crear el curso'})


@login_required
def ViewsCourse(request):
    if request.method == 'GET':
        cursoDelate = []
        try:
            cursos_con_inscripcion = []
            inscripciones = Inscripcion.objects.filter(usuario__facultad=request.user.usuario.facultad)
            cursos = Curso.objects.filter(inscripcion__in=inscripciones,
                                          carrera=request.user.usuario.carrera).distinct()
            for curso in cursos:
                esta_inscrito = inscripciones.filter(curso=curso, usuario=request.user.usuario).exists()
                cursos_con_inscripcion.append({'curso': curso, 'esta_inscrito': esta_inscrito})

            if request.user.usuario.rol.rol == 'Profesor':
                cursoDelate = cursos.filter(cursos_usuario__rol__rol=request.user.usuario.rol.rol, cursos_usuario__usuario=request.user.usuario.usuario)
                print(cursoDelate)


            return render(request, 'curso/viewCourse.html', {'cursos': cursos_con_inscripcion, 'cursoDelate': cursoDelate})

        except Inscripcion.DoesNotExist:
            return render(request, 'curso/viewCourse.html', {'cursos': [],  'cursoDelate': cursoDelate})
    else:
        try:
            curso_id = request.POST.get('curso_id')
            curso = get_object_or_404(Curso, pk=curso_id)
            # Verificar si ya está inscrito como profesor en el curso
            if request.user.usuario.rol.rol == 'Profesor':
                messages.error(request, 'Los profesores no pueden unirse a cursos.')
                return redirect('viewsCourse')

            # Verificar si ya está inscrito como estudiante en el curso
            if Inscripcion.objects.filter(usuario=request.user.usuario, curso=curso).exists():
                messages.error(request, 'Ya estás inscrito en este curso.')
                return redirect('viewsCourse')

            newInscripcion = Inscripcion.objects.create(usuario=request.user.usuario, curso=curso,
                                                        facultad=request.user.usuario.facultad.nombreFacultad)
            newInscripcion.save()


            return redirect('viewsCourse')
        except ValueError:
            return render(request, 'curso/viewCourse.html', {'cursos': []})


@login_required
def OneViewCourse(request, id_course):
    curso = get_object_or_404(Curso, pk=id_course)
    inscripciones = curso.inscripcion_set.all()  # Accede a las inscripciones relacionadas
    creador = None

    if inscripciones.exists():
        creador = inscripciones.first().usuario

    return render(request, 'curso/oneViewCourse.html', {'curso': curso, 'creador': creador})


@login_required
# def AllCourseParticipants(request):
#     try:
#         curso_id = request.GET.get('curso_id')
#         search_query = request.GET.get('area-buscar') or ''
#
#         participants = Inscripcion.objects.filter(
#             facultad=request.user.usuario.facultad.nombreFacultad
#         )
#
#         if curso_id is not None:
#             participants = participants.filter(curso__id=curso_id)
#
#         unique_usernames = set()
#         unique_participants = []
#         for participants in unique_participants:
#             username = participants.usuario.usuario.username
#             print(username)
#             if username not in unique_usernames:
#                 unique_usernames.add(username)
#                 unique_participants.append(participants)
#
#         if search_query:
#             # Filtrar por nombre de usuario solo si se proporciona una cadena de búsqueda
#             unique_participants = [p for p in unique_participants if search_query.lower() in p.usuario.usuario.username.lower()]
#
#         print(f'Search Query: {search_query}')
#         print(f'Número de participantes encontrados: {participants.count()}')
#         print(f'Número de participantes encontrados: {len(unique_participants)}')
#
#         return render(request, 'participante/allParticipant.html',
#                       {'participants': participants, 'search_query': search_query})
#     except ValueError:
#         return render(request, 'participante/allParticipant.html',
#                       {'participants': []})


def AllCourseParticipants(request):
    try:
        curso_id = request.GET.get('curso_id')
        search_query = request.GET.get('area-buscar') or ''

        participants = Inscripcion.objects.filter(
            facultad=request.user.usuario.facultad.nombreFacultad
        )

        if curso_id is not None:
            participants = participants.filter(curso__id=curso_id)

        unique_usernames = set()  # Usaremos un conjunto para almacenar nombres de usuario únicos
        unique_participants = []

        for participant in participants:
            username = participant.usuario.usuario.username
            if username not in unique_usernames:
                unique_usernames.add(username)
                unique_participants.append(participant)

        if search_query:
            # Filtrar por nombre de usuario solo si se proporciona una cadena de búsqueda
            unique_participants = [p for p in unique_participants if search_query.lower() in p.usuario.usuario.username.lower()]


        return render(request, 'participante/allParticipant.html',
                      {'participants': unique_participants, 'search_query': search_query})
    except ValueError:
        return render(request, 'participante/allParticipant.html',
                      {'participants': []})

