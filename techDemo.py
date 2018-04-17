
'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import random
import numpy as np
import cv2 as cv
import pygame
from pygame import gfxdraw
import math


def faceTracker():
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv.CascadeClassifier('haarcascade_eye.xml')

    img = cv.imread('testPhoto1.jpg')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #for (x,y,w,h) in faces:
        #print(x,y,w,h, "face")
        #cv.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
        #for (ex,ey,ew,eh) in eyes:
            #cv.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv.imshow('img',img)
    cv.waitKey(0)
    cv.destroyAllWindows()

class PygameGame(object):

    def init(self):
        self.imageIndex = 0
        self.testFiles = []
        self.testFiles.append("testPhoto1.jpg")
        self.testFiles.append('testPhoto2.jpg')
        self.testFiles.append('testPhoto3.jpg')
        self.testFiles.append('testPhoto4.jpg')
        self.testFiles.append('testPhoto5.jpg')
        self.testFiles.append('testPhoto6.jpg')
        self.testFiles.append('testPhoto7.jpg')
        
        
        self.testImages = []
        for i in range(len(self.testFiles)):
            self.testImages.append(pygame.image.load(self.testFiles[i]))
            #self.testImages[i] = pygame.transform.rotate(self.testImages[i], 270)
        
        
        '''
        self.testImages.append(pygame.image.load("testPhoto1.jpg"))
        self.testImages.append(pygame.image.load('testPhoto2.jpg'))
        self.testImages.append(pygame.image.load('testPhoto3.jpg'))
        self.testImages.append(pygame.image.load('testPhoto4.jpg'))
        self.testImages.append(pygame.image.load('testPhoto5.jpg'))
        self.testImages.append(pygame.image.load('testPhoto6.jpg'))
        self.testImages.append(pygame.image.load('testPhoto7.jpg'))
        '''
        
        #rotating images?
        
        self.cvImg = []
        for i in range(len(self.testFiles)):
            img = cv.imread(self.testFiles[i])
            #rows,cols = img.shape
            #(h,w) = img.shape[:2]
            #M = cv.getRotationMatrix2D((w // 2, h // 2), 270,1)
            #rotated = cv.warpAffine(img, M, (h, w))
            #dst = cv.warpAffine(img,M,(cols,rows))
            self.cvImg.append(img)
        
        self.grayImg = []
        for img in self.cvImg:
            self.grayImg.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
            
        self.numImages = len(self.testFiles)
            
            
            
        #cv stuff?
        self.face_cascade = cv.CascadeClassifier("/Users/jonathanperez/Desktop/15-112/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml")
        self.lefteye_cascade = cv.CascadeClassifier("/Users/jonathanperez/Desktop/15-112/opencv-master/data/haarcascades/haarcascade_lefteye_2splits.xml")
        self.righteye_cascade = cv.CascadeClassifier("/Users/jonathanperez/Desktop/15-112/opencv-master/data/haarcascades/haarcascade_righteye_2splits.xml")
        
        
        self.faces = self.face_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 5)
        self.leftEyes = self.lefteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
        self.rightEyes = self.righteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
            
        cv.waitKey(0)
        
            
        

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        print(len(self.faces), "faces")
        #print(len(self.eyes), "eyes")
        if(keyCode == 275 and self.imageIndex < self.numImages - 1):
            self.imageIndex += 1
        elif(keyCode == 276 and self.imageIndex > 0):
            self.imageIndex -= 1
            
        self.faces = self.face_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 5)
        self.leftEyes = self.lefteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
        self.rightEyes = self.righteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        screen.blit(self.testImages[self.imageIndex], (0,0))
        #cv.imshow("test", self.grayImg[0]) # syntax ...(title, img)
        
        #RECT = (left, top, width, height) OR ((left, top), (width, height))
        
        #pygame.draw.rect(surface, (color), (rect), width=0)
        #pygame.draw.rect(screen, (0,0,0), (0,0,100,50))
        #pygame.draw.circle(surface, (color), (center position), radius, width=0)
        #pygame.draw.circle(screen, (0,0,0), (50, 75), 25)
        #pygame.draw.ellipse(surface, (color), (rect), width=0)
        #pygame.draw.ellipse(screen, (0,0,0), (100, 0, 50, 50))
        #pygame.draw.arc(surface, (color), (rect), startRadian, endRadian, width=1)
        #myStart = 0
        #myEnd = math.pi / 2
        #pygame.draw.arc(screen, (0,0,0), (150, 0, 50, 50), myStart, myEnd, 2) #goes clockwise from start to end by default
        #pygame.draw.line(surface, (color), (startPos), (endPos), width=1)
        #pygame.draw.line(screen, (0,0,0), (0,0), (self.width, self.height), 2) #remember, it's self.heigth/width now
        
        
        #gfx draw testing
        #pygame.gfxdraw.line(screen, 0, 50, self.width, self.height + 50, (0,0,0))
        
        #openCV face rectangles
        for (x,y,w,h) in self.faces:
            #make rectangle with pygame
            #pygame.draw.rect(screen, (0,0,0), (x,y,w,h))
            pygame.draw.line(screen, (0,0,255), (x,y), (x+w, y), 2)
            pygame.draw.line(screen, (0,0,255), (x,y), (x,y+h), 2)
            pygame.draw.line(screen, (0,0,255), (x,y+h), (x+w, y+h), 2)
            pygame.draw.line(screen, (0,0,255), (x+w, y), (x+w, y+h), 2)
            
            
        for (ex,ey,ew,eh) in self.leftEyes:
            #make rectangle with pygame
            pygame.draw.line(screen, (255,0,0), (ex,ey), (ex+ew, ey), 2)
            pygame.draw.line(screen, (255,0,0), (ex,ey), (ex,ey+eh), 2)
            pygame.draw.line(screen, (255,0,0), (ex,ey+eh), (ex+ew, ey+eh), 2)
            pygame.draw.line(screen, (255,0,0), (ex+ew, ey), (ex+ew, ey+eh), 2)
            
        # for (ex,ey,ew,eh) in self.rightEyes:
        #     #make rectangle with pygame
        #     pygame.draw.line(screen, (255,0,0), (ex,ey), (ex+ew, ey), 2)
        #     pygame.draw.line(screen, (255,0,0), (ex,ey), (ex,ey+eh), 2)
        #     pygame.draw.line(screen, (255,0,0), (ex,ey+eh), (ex+ew, ey+eh), 2)
        #     pygame.draw.line(screen, (255,0,0), (ex+ew, ey), (ex+ew, ey+eh), 2)
        
        

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=600, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()