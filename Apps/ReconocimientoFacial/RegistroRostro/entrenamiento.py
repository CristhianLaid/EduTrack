import cv2
import os
import numpy as np


class Entrenar:

    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.peopleList = os.listdir(dataPath)
        print('Lista de personas: ', self.peopleList)

        self.labels = []
        self.facesData = []
        self.label = 0

    def hacerEntrenamiento(self):
        for nameDir in self.peopleList:
            personPath = self.dataPath + '/' + nameDir
            print('Leyendo las imágenes')

            for fileName in os.listdir(personPath):
                print('Rostros: ', nameDir + '/' + fileName)
                self.labels.append(self.label)
                self.facesData.append(cv2.imread(personPath + '/' + fileName, 0))

            self.label = self.label + 1

        # Métodos para entrenar el reconocedor
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        # face_recognizer = cv2.face.FisherFaceRecognizer_create()

        # Entrenando el reconocedor de rostros
        print("Entrenando...")
        face_recognizer.train(self.facesData, np.array(self.labels))

        # Almacenando el modelo obtenido
        face_recognizer.write('modeloLBPHFace.xml')
        # face_recognizer.write('modeloFisherFace.xml')
        print("Modelo almacenado...")