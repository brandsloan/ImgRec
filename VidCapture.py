import cv2, time
import msvcrt
import numpy as np
import matplotlib.pyplot as plt
import os



class VidCap:
	def __init__(self, waitTime = 0.0, errorTolerance = .95, basePic = None, targetDir = None):
		self.execDir = os.getcwd()
		self.address = "http://BR20039543:GaiusCenturion1#@127.0.0.1:8090/0"
		self.waitTime = waitTime
		self.errorTolerance = errorTolerance
		self.basePic = basePic
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
		print("EMERGENCY EXIT KEY: q")
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
		video = cv2.VideoCapture(0)
		if not self.basePic:
			print("Updating Base Picture")		
			if video.isOpened() == True:
				check, frame = video.read()
				cv2.imwrite("BaseImage.png", frame)
			else:
				print("Failed to initiate designated camera")
			#video.release()
		#video = cv2.VideoCapture(0)
		if video.isOpened() == True:
			while(quit != True):
				check, frame = video.read()
				print(i)
				cv2.imwrite("Image"+str(i)+".png", frame)
				time.sleep(self.waitTime)
				if msvcrt.kbhit():
					if msvcrt.getch() == "q":
						quit = True
				i += 1
		else:
			print("Failed to initiate designated camera")
		video.release()
		print str(i) + " images"
		
	def extract(self, image):
		img = cv2.imread(image)
		#img = cv2.GaussianBlur(img, (5, 5), 0)
		#img = cv2.bilateralFilter(img,9,75,75)
		
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
		return img
		
	def compare(self, image, *templates):
		#img = cv2.imread(image)
		img = image
		#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		
		img_gray = cv2.equalizeHist(img)
		for temp in (templates):
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
		afterImg = img[np.ix_(mask.any(1),mask.any(0))]
		cv2.imshow("after", afterImg)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return afterImg

V = VidCap(-1, .95, "", "")
V.image_capture()
b = V.extract("BaseImage.png")
nb = V.crop_image("Image0.png", 0)
nb1 = V.crop_image("Image1.png", 0)
nb2 = V.crop_image("Image2.png", 0)
b = V.crop_open_image(b, 0)
V.compare(b, nb, nb1, nb2)