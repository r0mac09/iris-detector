import cv2
import imutils


FACE_CASCADE_PATH = './data/haarcascade_frontalcatface_extended.xml'
EYE_CASCADE_PATH = './data/haarcascade_eye.xml'


face_detector = cv2.CascadeClassifier(FACE_CASCADE_PATH)
eye_detector = cv2.CascadeClassifier(EYE_CASCADE_PATH)


if __name__ == '__main__':
	img = cv2.imread('./test.png')
	# img = imutils.resize(img, width=500)
	img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_g = cv2.equalizeHist(img_g)
	

	results = face_detector.detectMultiScale(
		img_g, scaleFactor=1.05, minNeighbors=5,
		minSize=(10, 10), flags=cv2.CASCADE_SCALE_IMAGE)

	print(results)

	for (fX, fY, fW, fH) in results:
		print('FACE')
		# extract the face ROI
		faceROI = img_g[fY:fY+ fH, fX:fX + fW]
		# apply eyes detection to the face ROI
		eyeRects = eye_detector.detectMultiScale(
			faceROI, scaleFactor=1.1, minNeighbors=10,
			minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

		# loop over the eye bounding boxes
		for (eX, eY, eW, eH) in eyeRects:
			print('EYEEE')
			# draw the eye bounding box
			ptA = (fX + eX, fY + eY)
			ptB = (fX + eX + eW, fY + eY + eH)
			cv2.rectangle(img, ptA, ptB, (0, 0, 255), 2)
		
		# draw the face bounding box on the frame
		cv2.rectangle(img, (fX, fY), (fX + fW, fY + fH),
			(0, 255, 0), 2)

	
	cv2.imshow('Test', img)

	cv2.waitKey(0)