#################################################
#Jonathan Perez (jdperez)
#Section E
#################################################

'''
This file serves as a test for the capabilities of openCV face detection,
eye detection, edge detection, and thresholding, considering these will be 
key components to my project
'''


import random
import numpy as np
import cv2 as cv
import pygame
from pygame import gfxdraw
import math

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
        
        
        self.cvImg = []
        for i in range(len(self.testFiles)):
            img = cv.imread(self.testFiles[i])
            self.cvImg.append(img)
        
        self.grayImg = []
        for img in self.cvImg:
            self.grayImg.append(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
            
        self.numImages = len(self.testFiles)
            
        #cv cascades
        self.face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.lefteye_cascade = cv.CascadeClassifier("haarcascade_lefteye_2splits.xml")
        
        self.faces = self.face_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 5)
        self.leftEyes = self.lefteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
        
        #contour detection
        img = self.cvImg[self.imageIndex]
        imGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(self.grayImg[self.imageIndex], 127, 255, 0)
        im2, self.contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        
        #canny edge detection
        blurred = cv.GaussianBlur(imGray, (5, 5), 0)
        self.edges = cv.Canny(blurred, 100, 255)
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if(keyCode == 275 and self.imageIndex < self.numImages - 1):
            self.imageIndex += 1
        elif(keyCode == 276 and self.imageIndex > 0):
            self.imageIndex -= 1
            
        #face detection
        self.faces = self.face_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 5)
        self.leftEyes = self.lefteye_cascade.detectMultiScale(self.grayImg[self.imageIndex], 1.1, 3)
        
        #contour detection
        img = self.cvImg[self.imageIndex]
        imGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(self.grayImg[self.imageIndex], 127, 255, 0)
        im2, self.contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        
        #canny edge detection
        blurred = cv.GaussianBlur(imGray, (5, 5), 0)
        self.edges = cv.Canny(blurred, 100, 255)
        

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        screen.blit(self.testImages[self.imageIndex], (0,0))
        
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
            
        #draw contours and edges
        cv.drawContours(self.cvImg[self.imageIndex], self.contours, -1, (255,0,0), 1)
        cv.imshow("contours", self.cvImg[self.imageIndex])
        cv.imshow("edges", self.edges)
        
        

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