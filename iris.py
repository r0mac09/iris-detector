import cv2
import dlib
import numpy as np

# Pentru dlib e nevoie de C++ Make din https://visualstudio.microsoft.com/visual-cpp-build-tools/

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')


def get_landmarks(image):
    # Convertim imaginea in alb-negru
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detectam fetele din imagine
    faces = detector(gray, 1)
    
    # Creem o lista in care sa adaugam seturile de puncte pentru fiecare fata
    landmarks_list = []
    
    # Iteram prin fiecare fata
    for face in faces:
        
        # Calculam cele 68 de puncte ce dau forma fetei
        landmarks = predictor(gray, face)
        
        # Convertim punctele intr-o matrice de numere intregi cu doua coloane si 68 randuri
        landmarks_np = np.int32([(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)])

        # Adaugam matricea de puncte in lista
        landmarks_list.append(landmarks_np)

    return landmarks_list


def extract_eye_crops(image, landmarks_list):
    # Creem o lista in care sa adaugam centrele punctelor corespunzatoare ochilor
    eye_centers = []
    
    for landmarks in landmarks_list:
        left = np.mean(landmarks[36:42], axis=0)
        right = np.mean(landmarks[42:48], axis=0)
        
        left, right = np.int32(np.round(left)), np.int32(np.round(right))
        
        
        
    
    
if __name__ == '__main__':
    image = cv2.imread('./john-cena.png')
    get_landmarks(image)