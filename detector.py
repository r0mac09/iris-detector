import cv2
import numpy as np

FACE_CASCADE_PATH = './data/haarcascade_frontalcatface_extended.xml'
EYE_CASCADE_PATH = './data/haarcascade_eye.xml'

face_detector = cv2.CascadeClassifier(FACE_CASCADE_PATH)
eye_detector = cv2.CascadeClassifier(EYE_CASCADE_PATH)


def detect(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(
        img, scaleFactor=1.05, minNeighbors=5,
        minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)

    all_eyes = []

    for fx, fy, fw, fh in faces:
        face_crop = img[fy:fy+fh, fx:fx+fw]
        eyes = eye_detector.detectMultiScale(
            face_crop, scaleFactor=1.1, minNeighbors=10,
            minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        all_eyes += [(fx+x, fy+y,w, h) for x, y, w, h in eyes]
        
    return faces, all_eyes


def detect_pupil(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, thresh = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    # contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    c = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 2, img.shape[0]/2)
    
    print(c)
    pupils = []
    # for l in c:
    #     for circle in l:
    #         center = (circle[0], circle[1])
    #         radius = circle[2]
    #         pupils.append(center[0], center[1], radius)
    
    return pupils
    
def detect_iris(img, pupil):
    _, t = cv2.threshold(img, 195, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(t, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the iris using the radius of the pupil as input.
    c = cv2.HoughCircles(contours, cv2.HOUGH_GRADIENT, 2, pupil[2] * 2, param2 = 150)

    for l in c:
        for circle in l:
            center = (pupil[0], pupil[1])
            radius = circle[2]
            # This creates a black image and draws an iris-sized white circle in it.
            mask = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)
            cv2.circle(mask, center, radius, (255, 255, 255), thickness = -1)
            # Mask the iris and crop everything outside of its radius.
            img = cv2.bitwise_and(img, mask)



if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    key = -1

    while key != ord('q'):
        stat, img = cap.read()
        faces, eyes = detect(img)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

        for (x, y, w, h) in eyes:
            cv2.rectangle(img, (x, y), (x + w, y + h),
                          (0, 0, 255), 2)
             
            crop = img[y:y+h, x:x+w]
            pupils = detect_pupil(crop)
            
            for px, py, pr in pupils:
                cv2.circle(img, (x+px, y+py), pr, (255, 128, 128), 1, cv2.LINE_AA)

        cv2.imshow('Test', img)

        key = cv2.waitKey(1)
