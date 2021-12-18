import cv2
from iris import detect


img = cv2.imread('./test.png')
detection = detect(img)

for i, det in enumerate(detection):
    if det['left_eye'] != []:
        cv2.imshow(f'left {i}', det['left_eye_img'])
    if det['right_eye'] != []:
        cv2.imshow(f'right {i}', det['right_eye_img'])

cv2.waitKey(0)