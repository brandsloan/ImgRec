import cv2, time
import numpy as np
import matplotlib.pyplot as plt
import os
import sys


class VidCap:
        def __init__(self, waitTime = 0.0, errorTolerance = .95, targetDir = None):
                self.execDir = os.getcwd()
                self.address = "http://BR20039543:GaiusCenturion1#@127.0.0.1:8090/0"
                self.waitTime = float(waitTime)
                self.errorTolerance = float(errorTolerance)
                if targetDir == None:
                        baseDir = os.path.dirname(os.path.abspath(__file__))
                        self.targetDir = os.path.join(baseDir, "images")
                else:
                        self.targetDir = targetDir
                if not os.path.isdir(self.targetDir):
                        os.mkdir(self.targetDir, 0O755)
                
        def write_image(self, imgName, img):
                try:
                        os.chdir(self.targetDir)
                        cv2.imwrite(imgName, img)
                except: 
                        print("Error opening target directory")
                finally:
                        os.chdir(self.execDir)
        
        def read_image(self, imgName, channels=-1, readDir = None):
                if readDir == None:
                        readDir = self.targetDir
                retImg = None
                if os.getcwd() == readDir:
                        if channels == 0:
                                retImg = cv2.imread(imgName, channels)
                        else:
                                retImg = cv2.imread(imgName)
                else:
                        try:
                                os.chdir(readDir)
                                if channels == 0:
                                        retImg = cv2.imread(imgName, channels)
                                else:
                                        retImg = cv2.imread(imgName)
                        except:
                                print("Error opening target directory")
                        finally:
                                os.chdir(self.execDir)
                return retImg

        def image_capture(self):
                print("EMERGENCY EXIT KEY: q")
                if self.waitTime <= 0.0:
                        try:
                                self.waitTime = raw_input("Enter time interval in number of seconds: ")
                                self.waitTime = float(self.waitTime)
                                if self.waitTime <= 0:
                                        raise Exception
                        except ValueError:
                                self.waitTime = 3
                                print("Input non numeric, using base wait time of %d seconds" % self.waitTime)
                        except Exception as e:
                                self.waitTime = 3
                                print("Input must be positive, using base wait time of %d seconds" % self.waitTime)
                                
                quit = False
                i = 0
                video = cv2.VideoCapture(0)
                
                if video.isOpened() == True:
                        while(quit != True):
                                check, frame = video.read()
                                print(i)
                                self.write_image("Image"+str(i)+".png", frame)
                                time.sleep(self.waitTime)
                                if cv2.waitKey(1) == ord('q'):
                                    quit = True
                                i += 1
                else:
                        print("Failed to initiate designated camera")
                video.release()
                print(str(i) + " images")
        
        def crop_image(self, image,tol=0):
                img = self.read_image(image, 0)
                mask = img>tol
                afterImg = img[np.ix_(mask.any(1),mask.any(0))]
                return afterImg
        
        def crop_open_image(self, image,tol=0):
                imgC = image
                img = cv2.cvtColor(imgC, cv2.COLOR_BGR2GRAY)
                mask = img>tol
                afterImg = imgC[np.ix_(mask.any(1),mask.any(0))]
                return afterImg
        
        def extract(self, image):
                img = self.read_image(image)
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
                
                #cv2.imwrite("bgextract.png", img)
                self.write_image("bgextract.png", img)
                #plt.imshow(img)
                #plt.colorbar()
                #plt.show()
                retImg = self.crop_open_image(img)
                return retImg
                
        def compare(self, image, tempDir, *templates):
                found = 0
                img = image
                #print(tempDir)
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                
                img_gray = cv2.equalizeHist(img_gray)
                for t in (templates):
                        #print(tempDir)
                        #print(t)
                        temp = self.read_image(t, 0, tempDir)
                        w, h = temp.shape[::-1]
                        res = cv2.matchTemplate(img_gray, temp, cv2.TM_CCOEFF_NORMED)
                        res3 = cv2.matchTemplate(img_gray, temp, cv2.TM_CCORR_NORMED)
                        loc = np.where(res >= self.errorTolerance)
                        loc3 = np.where(res3 >= self.errorTolerance)
                                
                        for pt in zip(*loc[::-1]):
                                cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (255, 0, 0), 2)
                                cv2.putText(img, t, (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                                found = 1
                                #pass
                        for pt in zip(*loc3[::-1]):
                                #cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 1)
                                pass
                        if found == 1:
                                print(t + " was found")
                        else:
                                print(t + " was not found")
                        found = 0
                        #cv2.imshow(t, temp)
                #cv2.imshow("boxed", img)
                self.write_image("Final.png", img)
                #cv2.imshow("ig", img_gray)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                return
                
        def templateCompare(self, image, tempDir):
                img = image
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                
                img_gray = cv2.equalizeHist(img_gray)
                for root, dirs, files in os.walk(tempDir):
                        for t in files:
                                if t.endswith("png") or t.endswith("jpg") or t.endswith("jpeg"):
                                        path = os.path.join(root, t)
                                        temp = self.read_image(t, 0)
                                        w, h = temp.shape[::-1]
                                        res = cv2.matchTemplate(img_gray, temp, cv2.TM_CCOEFF_NORMED)
                                        res3 = cv2.matchTemplate(img_gray, temp, cv2.TM_CCORR_NORMED)
                                        loc = np.where(res >= self.errorTolerance)
                                        loc3 = np.where(res3 >= self.errorTolerance)
                                                
                                        for pt in zip(*loc[::-1]):
                                                cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (255, 0, 0), 2)
                                                cv2.putText(img, t, (pt[0], pt[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                                                #pass
                                        for pt in zip(*loc3[::-1]):
                                                #cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 0, 255), 1)
                                                pass
                                        #cv2.imshow(t, temp)
                #cv2.imshow("boxed", img)
                #cv2.imshow("ig", img_gray)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                self.write_image("Final.png", img)
                return
                
if __name__ == "__main__":
        if(len(sys.argv) < 4):
                V = VidCap()
        else:
                V = VidCap(sys.argv[1] ,sys.argv[2], sys.argv[3])
        #V.image_capture()

        img = V.extract("Image0.png")
        V.compare(img,"/home/bsloan/basedir/ImgRec/HELLO" ,"T0.png", "T1.png", "T2.png")
