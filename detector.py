import cv2


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
        

        cv2.imshow('Test', img)

        key = cv2.waitKey(1)
