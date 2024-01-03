import cv2
import os
import numpy as np
import datetime

from Apps.Asistencia.RegistroAsistencia.models import RegistroAsistencia, TipoRegistro
from Apps.Usuario.models import Usuario, Inscripcion
from Apps.Registro_academico.Datos_institucionales.models import Curso


class Asistencia:
    def __init__(self):
        self.registros = {}
        self.atrasos = {}
        self.idcurso = None
        self.HORA_ENTRADA_DESIGNADA = None
        self.HORA_SALIDA = None
        self.MINUTOS_SALIDA = None
        self.TOLERANCIA_ANTES = 34
        self.TOLERANCIA_DESPUES = 34
        self.TOLERANCIA_SALIDA_DESPUES = 2  # 20 minutos

    def registrar_asistencia(self, usuario, inscripcion):
        hora_entero = self.HORA_ENTRADA_DESIGNADA

        # Convertir a cadena en formato HH:00:00
        hora_entrada_designada_str = f"{hora_entero:02d}:00:00"

        # Utilizar strptime para obtener un objeto de datetime
        hora_entrada_designada_datetime = datetime.datetime.strptime(hora_entrada_designada_str,"%H:%M:%S")

        # Crear un objeto timedelta usando el valor de minutos directamente
        tolerancia_despues = datetime.timedelta(minutes=self.TOLERANCIA_DESPUES)

        # Obtener la hora actual
        hora_actual = datetime.datetime.now()

        # Calcular la hora máxima permitida (hora de entrada + tolerancia)
        hora_maxima_permitida = hora_entrada_designada_datetime + tolerancia_despues

        # Verificar si la hora actual está dentro del rango
        # print("Hora de entrada designada:", hora_entrada_designada_datetime)
        # print("Hora actual:", hora_actual)
        # print("Rango permitido:", hora_entrada_designada_datetime.time(), "<=", hora_actual.time(), "<=", hora_maxima_permitida.time())

        if hora_entrada_designada_datetime.time() <= hora_actual.time() <= hora_maxima_permitida.time():

            registro_asistencia = RegistroAsistencia(
                usuario=usuario,
                tipo=TipoRegistro.objects.get(tipo_registro='Automatico'),
                curso=inscripcion.curso.nombreCurso,
                fecha_asistencia=datetime.date.today(),
                hora_asistencia=datetime.datetime.now().time(),
                evento='Clase'
            )
            # Determinar el estado de la asistencia
            # elif hora_entrada_designada.curso.horaSalida < registro_asistencia.hora_asistencia:
            #     registro_asistencia.estado_asistencia = RegistroAsistencia.EstadoAsistencia.ASISTENCIA_COMPLETA
            fecha = hora_actual.date()
            if hora_entrada_designada_datetime.time() <= hora_actual.time() <= (hora_entrada_designada_datetime + datetime.timedelta(minutes=self.TOLERANCIA_ANTES)).time():
                # Está "A tiempo"
                fecha_entrada = hora_actual.strftime("%Y-%m-%d %H:%M:%S")
                self.registros[usuario] = {"fecha": fecha, "entrada": fecha_entrada}
                registro_asistencia.estado_asistencia = RegistroAsistencia.EstadoAsistencia.A_TIEMPO
                print(f"{usuario} ha registrado entrada a tiempo")
            elif (hora_entrada_designada_datetime + datetime.timedelta(minutes=self.TOLERANCIA_ANTES)).time() < hora_actual.time() <= hora_maxima_permitida.time():
                # Está "Atrasado"
                self.atrasos[usuario] = {"fecha": fecha}
                registro_asistencia.estado_asistencia = RegistroAsistencia.EstadoAsistencia.ATRASADO
                print(f"{usuario} ha registrado atraso")
            else:
                # Está fuera del rango permitido
                print(f"{usuario} no está dentro del rango permitido")

            registro_asistencia.save()

        else:
            print(
                f"El horario para el curso {inscripcion.curso.nombreCurso} se encuentra entre {inscripcion.curso.horaEntrada}-{inscripcion.curso.horaSalida}")

    def registrar_salida(self, nombre_persona):
        hora_actual = datetime.datetime.now()
        hora_salida_designada = hora_actual.replace(hour=self.HORA_SALIDA, minute=self.MINUTOS_SALIDA, second=0,
                                                    microsecond=0)
        limite_tolerancia = hora_salida_designada + datetime.timedelta(minutes=self.TOLERANCIA_SALIDA_DESPUES)
        print(hora_actual, " + ", hora_salida_designada, " * ", limite_tolerancia)

        if (nombre_persona in self.registros or nombre_persona in self.atrasos) and \
                ("salida" not in self.registros.get(nombre_persona, {}) and "salida" not in self.atrasos.get(
                    nombre_persona, {})):
            print("entro del if")

            # Verificar si ya existe una asistencia para este usuario y fecha
            usuario = Usuario.objects.get(usuario__username=nombre_persona)
            inscripcion = Inscripcion.objects.get(usuario=usuario, curso=self.idcurso)

            # Buscar el registro de entrada para el usuario y fecha actual
            registro_entrada = RegistroAsistencia.objects.filter(
                usuario=usuario,
                fecha_asistencia=datetime.date.today(),
                evento='Clase',
                curso=inscripcion.curso.nombreCurso
            ).first()

            print(self.registros)

            if registro_entrada and "salida" not in self.registros.get(nombre_persona, {}):
                print('hola')
                if hora_actual >= hora_salida_designada and hora_actual <= limite_tolerancia:
                    fecha_salida = hora_actual.strftime("%Y-%m-%d %H:%M:%S")

                    # Actualizar el registro existente
                    registro_entrada.hora_salida = datetime.datetime.now().time()
                    registro_entrada.save()
                    print(f"Registro de salida actualizado para {nombre_persona}")

                    # Marcar que la salida ya se ha registrado para evitar actualizaciones constantes
                    self.registros[nombre_persona]["salida"] = fecha_salida

    def verificar_asistencia_final(self, nombre_persona):
        if nombre_persona in self.registros and "salida" in self.registros[nombre_persona]:
            print(f"{nombre_persona} tiene asistencia completa")
        elif nombre_persona in self.atrasos and "salida" in self.atrasos[nombre_persona]:
            print(f"{nombre_persona} tiene media asistencia")
        else:
            print(f"{nombre_persona} no tiene registros de asistencia")


class ReconocimientoFacial:
    def __init__(self, dataPath, modelPath, idcurso):
        self.idcurso = idcurso
        self.dataPath = dataPath
        self.modelPath = modelPath
        self.imagePaths = os.listdir(dataPath)
        print('Rostros:', self.imagePaths)

        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        # self.face_recognizer = cv2.face.FisherFaceRecognizer_create()
        self.face_recognizer.read(modelPath)

        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.asistencia = Asistencia()

    def detectarRostro(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = self.faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = self.face_recognizer.predict(rostro)
            usuario = Usuario.objects.get(usuario__username=self.imagePaths[result[0]])

            if result[1] < 75:
                try:
                    hora_entrada_designada = Inscripcion.objects.get(usuario__usuario__username=usuario,
                                                                     curso=self.idcurso)
                    self.asistencia.HORA_ENTRADA_DESIGNADA = hora_entrada_designada.curso.horaEntrada.hour
                    self.asistencia.HORA_SALIDA = hora_entrada_designada.curso.horaSalida.hour
                    self.asistencia.MINUTOS_SALIDA = hora_entrada_designada.curso.horaSalida.minute
                    self.asistencia.idcurso = self.idcurso
                    inscripcion = Inscripcion.objects.get(usuario__usuario__username=usuario, curso=self.idcurso)
                    if Inscripcion.objects.filter(usuario__usuario__username=usuario, curso=self.idcurso).exists():
                        # Persona inscrita en el curso
                        cv2.putText(frame,
                                    '{} - {} - {}'.format(usuario, usuario.facultad, usuario.carrera.nombreCarrera),
                                    (x, y - 25), 2, 1.1,
                                    (0, 255, 0), 1,
                                    cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Verificar si ya existe una asistencia para este usuario y fecha
                        if not RegistroAsistencia.objects.filter(usuario=usuario,
                                                                 fecha_asistencia=datetime.date.today(),
                                                                 evento='Clase',
                                                                 curso=inscripcion.curso.nombreCurso).exists():

                            self.asistencia.registrar_asistencia(usuario, inscripcion)
                        else:
                            print(f"Asistencia ya registrada para {usuario} hoy.")

                    self.asistencia.registrar_salida(usuario)

                except Inscripcion.DoesNotExist:
                    # Persona no inscrita en el curso (en rojo)
                    cv2.putText(frame, '{} - {} - {}'.format(usuario, usuario.facultad, usuario.carrera.nombreCarrera),
                                (x, y - 25), 2, 1.1,
                                (0, 0, 255), 1,  # Rojo
                                cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # print(f"La Inscripcion para el usuario {usuario} y curso {self.idcurso} no existe.")
                    continue
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        return frame

    def reconocimiento(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while True:
            ret, frame = cap.read()

            if ret == True:
                frame = self.detectarRostro(frame)

            cv2.imshow('Reconocimiento Facial', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
