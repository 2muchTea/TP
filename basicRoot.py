#################################################
#Jonathan Perez (jdperez)
#Section E
#################################################

import random
import numpy as np
import cv2 as cv
import pygame
from pygame import gfxdraw
import math

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

######
#plan
######

#create root at top middle of screen (initializes with down direction)
#root grows all the way to almost bottom of screen
#root stops (mode = stopped)
#lateral roots created along primary root (randomly growing right or left) (makeLateral function?)
#line thickness is decided by color of pixel at that node
#every "move", make move, find what threshold root is in, decide thickness range
#roots should have a preference towards downward direction
#initialized with a certain growth speed that is reduced (by percentage) until almost stopped
#line thickness should also be proportional to growth speed (that way it tapers as it moves)

#print done just for testing UI's sake

######
#Turtle Graphics
######

#turtle graphics based off of template found on 15-104 website

#makeTurtle(x, y) -- make a turtle at x, y, facing right, pen down
#left(d) -- turn left by d degrees
#right(d) -- turn right by d degrees
#forward(p) -- move forward by p pixels
#back(p) -- move back by p pixels
#penDown() -- pen down
#penUp() -- pen up
#goto(x, y) -- go straight to this location
#setColor(color) -- set the drawing color
#setWeight(w) -- set line width to w
#face(d) -- turn to this absolute direction in degrees
#angleTo(x, y) -- what is the angle from my heading to location x, y?
#turnToward(x, y, d) -- turn by d degrees toward location x, y
#distanceTo(x, y) -- how far is it to location x, y?

class Turtle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = [(x, y)]
        self.widths = [1]
        self.angle = 0 # radians(same as unit circle)
        self.penIsDown = True
        self.color = "black"
        self.width = 5
        
    def left(self, radians):
        self.angle -= radians
        
    def right(self, radians):
        self.angle += radians
        
    def forward(self, dist):
        #rad = math.radians(self.angle)
        newx = roundHalfUp(self.x + (math.cos(self.angle) * dist))
        newy = roundHalfUp(self.y + (math.sin(self.angle) * dist))
        self.goTo(newx, newy)
        pass
        
    def back(self, dist):
        self.forward(-1 * dist)
        
    def penDown(self):
        self.penIsDown = True
        
    def penUp(self):
        self.penIsDown = False
        
    def goTo(self, newX, newY):
        self.x, self.y = newX, newY
        self.points.append((self.x, self.y))
        self.widths.append(self.width)
        
    def distTo(self, x, y):
        a = self.x - x
        b = self.y - y
        return (a**2 + b**2)**0.5
        
    def angleTo(self, x, y):
        pass
        
    def turnToward(self, x, y):
        pass
        
    def setColor(self, color):
        self.color = color
        
    def face(self, angle):
        self.angle = angle
        
######
#Root Classes
######

class Root(Turtle):
    def __init__(self, x, y, angle, widthInit, growthInit, img):
        super().__init__(x, y) 
        self.widthInit = widthInit
        self.width = widthInit
        self.widths = [widthInit] #starts with specified width
        self.angle = angle #degrees
        self.growing = True
        self.growRate = growthInit # pixels per move
        self.img = img
        self.imgSize = self.img.shape
        self.branches = []
        
    def forward(self, dist):
        #rad = math.radians(self.angle)
        newx = roundHalfUp(self.x + (math.cos(math.radians(self.angle)) * dist))
        newy = roundHalfUp(self.y + (math.sin(math.radians(self.angle)) * dist))
        xSize = self.imgSize[1]
        ySize = self.imgSize[0]
        if(newy < ySize and newy > 0 and newx < xSize and newx > 0):
            self.slowDown(newx, newy)
            self.decideDir(newx, newy)
            self.goTo(newx, newy)
        else:
            self.growing = False
    
    #decides how much to reduce growth rate based off of position
    def slowDown(self, x, y):
        greyValue = self.img[y, x]
        if(greyValue > 100):
            slowRate = ((greyValue - 100) / 155) * .10
            self.growRate *= (1 - slowRate)
            
    def decideDir(self, x, y):
        if(self.angle > 90):
            self.angle -= random.randint(-1, 2)
        elif(self.angle < 90):
            self.angle += random.randint(-1, 2)
        
    def split(self):
        newBranches = []
        greyValue = self.img[self.y, self.x]
        if(greyValue <= 150 and self.width > 1):
            splitChance = (1 - (greyValue / 150) * 0.05)
            if(random.random() >= (1 - splitChance)):
                self.growing = False
                angle1 = self.angle + (random.randint(2, 30))
                angle2 = self.angle - (random.randint(2, 30))
                newWidth = self.width - 1
                newGrow = self.growRate
                newBranches.append(Root(self.x, self.y, angle1, newWidth, newGrow, self.img))
                newBranches.append(Root(self.x, self.y, angle2, newWidth, newGrow, self.img))
                self.growing = False
                return newBranches
            
class PrimaryRoot(Root):
    
    def __init__(self, x, widthInit, growthInit, img):
        super().__init__(x, 0, 90, widthInit, growthInit, img) 
        self.branched = False
        self.stopHeight = 550
        
    def forward(self, dist):
        #rad = math.radians(self.angle)
        newx = roundHalfUp(self.x + (math.cos(math.radians(self.angle)) * dist))
        newy = roundHalfUp(self.y + (math.sin(math.radians(self.angle)) * dist))
        xSize = self.img.shape[1]
        ySize = self.img.shape[0]
        #print(newy, newx)
        if(newy < self.stopHeight and newy < ySize and newy > 0 and newx < xSize and newx > 0):
            greyValue = self.img[newy, newx]
            #only applies to lateral roots?
            
            if(greyValue > 100):
                slowRate = ((greyValue - 100) / 155) * .005 #max slowRate is 5 percent per move
                self.growRate *= (1 - slowRate)
        
        #root should taper
        #self.width = int((self.growRate / 3) * self.widthInit)
            
            self.goTo(newx, newy)
            
        else:
            self.growing = False
    
    #randomly choose a number of points to be "nodes" for lateral roots to grow
    def growLaterals(self):
        nodes = []
        for point in self.points:
            if(random.random() > .85):
                nodes.append(point)
        lats = []
        for node in nodes:
            #decide widthInit, growthInit, angle
            #each node creates two laterals
            angle1 = random.randint(90, 190)
            angle2 = random.randint(-10, 90)
            greyValue = self.img[node[1], node[0]]
            
            widthInit = roundHalfUp((1 - (greyValue / 255)) * 5)
            if(widthInit <= 3):
                widthInit = 1
            #growthInit = roundHalfUp((1 - (greyValue / 255)) * 3)
            #if(growthInit <= 1):
                #growthInit = 1.5
            growthInit = 3
            
            lats.append(Root(node[0], node[1], angle1, widthInit, growthInit, self.img))
            lats.append(Root(node[0], node[1], angle2, widthInit, growthInit, self.img))
            
        self.branched = True
        #print(lats)
        return lats
        
        
####################
#Animation/Graphics
####################

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
        self.testFile = "rootTestPhoto1.jpg"
        self.testImg = pygame.image.load(self.testFile)
        self.cvImg = cv.imread(self.testFile)
        self.cvGrey = cv.cvtColor(self.cvImg, cv.COLOR_BGR2GRAY)
        self.roots = []
        #self.roots.append(PrimaryRoot(self.width // 2, 5, 3, self.cvGrey))
        self.roots.append(PrimaryRoot(self.width // 4, 5, 3, self.cvGrey))
        self.roots.append(PrimaryRoot((3*self.width//4), 5, 3, self.cvGrey))

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        for root in self.roots:
            if(root.growing == True):
                #print("i should be growing")
                root.forward(root.growRate)
                #if not(isinstance(root, PrimaryRoot)):
                    #self.roots.extend(root.split())
                if(root.growRate < 1):
                    root.growing = False
            elif(root.growing == False):
                if(isinstance(root, PrimaryRoot) and root.branched == False):
                    print("make laterals!")
                    self.roots.extend(root.growLaterals())
                    #print(self.roots)
                #else:
                    #self.roots.remove(root)
        

    def redrawAll(self, screen):
        screen.blit(self.testImg, (0,0))
        
        for root in self.roots:
            for i in range(len(root.points)):
                x, y = root.points[i][0], root.points[i][1]
                pygame.gfxdraw.aacircle(screen, x, y, root.widths[i] // 2, (255,0,0))
                pygame.gfxdraw.filled_circle(screen, x, y, root.widths[i] // 2, (255,0,0))
        

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=600, fps=50, title="112 Pygame Game"):
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
        