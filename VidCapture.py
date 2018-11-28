import cv2, time
import msvcrt
import numpy as np
import matplotlib.pyplot as plt
import os

class VidCap:
	def VC(self, waitTime = 0.0, errorTolerance = .95 ,BasePic = "", targetDir = ""):
		self.execDir = os.getcwd()
		
		self.waitTime = waitTime
		self.errorTolerance = errorTolerance
		self.BasePic = BasePic
		self.targetDir = targetDir
	
	def write_image(self, imgName, img):
		try:
			os.chdir(self.targetDir)
			cv2.imwrite(imgName, img)
		except: 
			print("Error opening target directory")
		finally:
			os.chdir(self.execDir)
		
	def image_capture(self):
		if self.waitTime <= 1.0:
			try:
				self.waitTime = raw_input("Enter time interval in number of seconds: ")
				self.waitTime = float(self.waitTime)
				if self.waitTime <= 0:
					raise Excep
			except ValueError, Excep:
				self.waitTime = 3
				print "Invalid input, using base wait time of %d seconds" % self.waitTime

		quit = False
		i = 0
		if self.BasePic == "":
			video = cv2.VideoCapture(0)
			check, frame = video.read()
			cv2.imwrite("BaseImage.png", frame)
			video.release()

		while(quit != True):
			video = cv2.VideoCapture(0)
			check, frame = video.read()

			cv2.imwrite("Image"+str(i)+".png", frame)
			time.sleep(self.waitTime)
			if msvcrt.kbhit():
				if msvcrt.getch() == "q":
					quit = True
			i += 1
				
		video.release()
		print str(i) + " images"
	
	def __init__(self):
		self.VC(-1, .775, "a", "b")
		
	def extract(self, template, image):
		img = cv2.imread(image)
		tmp = cv2.imread(template,0)
		#img = cv2.GaussianBlur(img, (5, 5), 0)
		#tmp = cv2.GaussianBlur(tmp, (5, 5), 0)
		#img = cv2.bilateralFilter(img,9,75,75)
		#tmp = cv2.bilateralFilter(tmp,9,75,75)
		
		w, h = img.shape[:-1]
		mask = np.zeros(img.shape[:2], np.uint8)
		bgdModel = np.zeros((1,65), np.float64)
		fgdModel = np.zeros((1,65), np.float64)
		
		rect = (int(.2*w), int(.2*h), int(.8*w), int(.8*w))
		cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
		mask2 = np.where((mask==2)|(mask==0), 0, 1).astype('uint8')
		img = img*mask2[:,:,np.newaxis]
		
		cv2.imwrite("bgextract.png", img)
		#self.write_image("bgextract.png", img)
		plt.imshow(img)
		plt.colorbar()
		plt.show()
		#cv2.imshow("TEMP", tmp)
		return tmp, img
		
	def compare(self, image, *templates):
		#img = cv2.imread(image)
		img = image
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		#img_gray3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img_gray = cv2.equalizeHist(img_gray)
		for temp in (templates):
			#temp = templates[i]
			#temp_gray = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)	
			#temp_gray = cv2.equalizeHist(temp_gray)
			#temp = cv2.imread(template)
			w, h = temp.shape[::-1]
			res = cv2.matchTemplate(img_gray, temp, cv2.TM_CCOEFF_NORMED)
			res3 = cv2.matchTemplate(img_gray, temp, cv2.TM_CCORR_NORMED)
			loc = np.where(res >= self.errorTolerance)
			loc3 = np.where(res3 >= self.errorTolerance)
				
			for pt in zip(*loc[::-1]):
				cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (255, 0, 0), 2)
			for pt in zip(*loc3[::-1]):
				cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 1)
			cv2.imshow("img", temp)
		cv2.imshow("boxed", img)
		cv2.imshow("ig", img_gray)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return
	
	def crop_image(self, image,tol=0):
		img = cv2.imread(image, 0)
		cv2.imshow("before", img)
		mask = img>tol
		cv2.imshow("after", img[np.ix_(mask.any(1),mask.any(0))])
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return img[np.ix_(mask.any(1),mask.any(0))]
	
	def crop_open_image(self, image,tol=0):
		imgC = image
		img = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)
		cv2.imshow("before", imgC)
		mask = img>tol
		cv2.imshow("after", img[np.ix_(mask.any(1),mask.any(0))])
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return imgC[np.ix_(mask.any(1),mask.any(0))]

V = VidCap()
#V.image_capture()
b, i = V.extract("BaseImage.png", "TestImage.png")
nb = V.crop_image("bi.png", 0)
nb1 = V.crop_image("bi1.png", 0)
nb2 = V.crop_image("bi2.png", 0)
i = V.crop_open_image(i, 0)
V.compare(i, nb, nb1, nb2)#"BaseImage.png")