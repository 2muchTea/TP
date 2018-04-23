#################################################
#Jonathan Perez (jdperez)
#Section E
#################################################

'''
This file is meant to implement turtle graphics into pygame using anti-aliased
circles instead of lines for superior graphics. This program simply allows
the user to control the movement of the turtle by pressing "f" to move forward,
right arrow to turn right, left arrow to turn left, up arrow to grow bigger, 
and down arrow to get smaller.
'''

import pygame
from pygame import gfxdraw
import random
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


#################
#TURTLE GRAPHICS
#################

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
        self.turtle = Turtle(self.width // 2, self.height // 2)

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
        if(self.isKeyPressed(102)): #102 is f
            self.turtle.forward(2)
        if(self.isKeyPressed(273)): #273 is up arrow
            self.turtle.width += 1
        if(self.isKeyPressed(274)): #115 is down arrow
            if(self.turtle.width > 1):
                self.turtle.width -= 1
        if(self.isKeyPressed(276)): #276 is left arrow
            self.turtle.left(math.pi / 24)
        if(self.isKeyPressed(275)): #275 is right arrow
            self.turtle.right(math.pi / 24)
        pass

    def redrawAll(self, screen):
        for i in range(len(self.turtle.points)):
            x, y = self.turtle.points[i][0], self.turtle.points[i][1]
            pygame.gfxdraw.aacircle(screen, x, y, self.turtle.widths[i] // 2, (0,0,0))
            pygame.gfxdraw.filled_circle(screen, x, y, self.turtle.widths[i] // 2, (0,0,0))

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
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