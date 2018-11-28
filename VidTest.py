import numpy as np 
import cv2
import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")
cc = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')

labels = {}
with open("labels.pickle", 'rb') as f:
	base_labels = pickle.load(f)
	labels = {v:k for k,v in base_labels.items()}


cap = cv2.VideoCapture(0)
color = (255, 0, 0)

while(True):
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = cc.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for(x,y,w,h) in faces:
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = frame[y:y+h, x:x+w]
		
		id_, conf = recognizer.predict(roi_gray)
		if conf >= 45:
			print id_
			print labels[id_]
			cv2.putText(frame, labels[id_], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
		cv2.imwrite('roi.png', roi_gray)
		cv2.rectangle(frame, (x,y), (x+w, y+h), color, 2)
		
	cv2.imshow('frame', frame)
	if cv2.waitKey(20) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()