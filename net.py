import cv2

quit = False

for i in range (0, 10):
	video = cv2.VideoCapture(i)
	if video.isOpened() == True:
		print(i)
		while quit != True:
			ret, frame = video.read()
			cv2.imshow("frame", frame)
			if cv2.waitKey(20) == ord('q'):
				quit = True
		video.release()
	cv2.destroyAllWindows()
	quit = False
print("Hello world")