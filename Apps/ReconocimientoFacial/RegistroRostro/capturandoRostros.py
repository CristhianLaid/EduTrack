# capturandoRostro.py
import cv2
import os
import imutils

class CapturaRostro:
    def __init__(self, person_name):
        self.person_name = person_name
        self.data_path = 'C:/EduTrack/Apps/ReconocimientoFacial/RegistroRostro/data'
        self.person_path = os.path.join(self.data_path, self.person_name)

        if not os.path.exists(self.person_path):
            print('Carpeta creada:', self.person_path)
            os.makedirs(self.person_path)

        self.face_classif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def capturar(self):
        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            aux_frame = frame.copy()

            faces = self.face_classif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rostro = aux_frame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(os.path.join(self.person_path, f'rostro_{count}.jpg'), rostro)
                count += 1

            cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == 27 or count >= 200:
                break

        cap.release()
        cv2.destroyAllWindows()

        return count > 0
