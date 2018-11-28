import os
from PIL import Image
import numpy as np
import cv2
import pickle

cc = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_default.xml')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "test_images")
recognizer = cv2.face.LBPHFaceRecognizer_create()

size = (550, 550)

cur_id = 0
label_id = {}
x_train = []
y_labels = []

for root, dirs, files in os.walk(IMG_DIR):
	for file in files:
		if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
			path = os.path.join(root, file)
			label = os.path.basename(root).replace(" ", "-").lower()
			
			if not label in label_id:
				label_id[label] = cur_id
				cur_id += 1
			id_ = label_id[label]

			pil_image = Image.open(path).convert("L")
			final_image = pil_image.resize(size, Image.ANTIALIAS)
			image_array = np.array(pil_image, "uint8")
			
			faces = cc.detectMultiScale(image_array, scaleFactor = 1.5, minNeighbors=5)
			
			for(x,y,w,h) in faces:
				roi = image_array[y:y+h, x:x+w]
				x_train.append(roi)
				y_labels.append(id_)
				
with open("labels.pickle", 'wb') as f:
	pickle.dump(label_id, f)
	
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainer.yml")