###### IMPORT ######

import pygame
import Joystick_Test as jst
import random
import time
from math import *
import numpy as np
import JSmanager as jsm

###### SETUP ######

pygame.init()
screenDimensions = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print(screenDimensions)

windowSize = (480, 270)

pygame.display.set_caption("Project HappyStick") # Sets title of window
screen = pygame.display.set_mode(windowSize, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)

###### INITIALIZE ######

jsm.keylog

fps = 60
clock = pygame.time.Clock()

###### FUNCTIONS ######

def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
    jX, jY = jsCoords[0], jsCoords[1]
    x, y = -jX + windowSize[0]/2, jY + windowSize[1]/2
    return (x, y)

def drawPoint(SScoords):
    pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

def drawTestBG():
    start = -112
    for line in range(15):
        x = start + line*16
        pygame.draw.aaline(screen, (50, 50, 50), jsToSS((x, sqrt(128**2 - x**2))), jsToSS((x, -sqrt(128**2 - x**2)))) # vertical gridlines
    
    for line in range(15):
        y = start + line*16
        pygame.draw.aaline(screen, (50, 50, 50), jsToSS((sqrt(128**2 - y**2), y)), jsToSS((-sqrt(128**2 - y**2), y))) # horizontal gridlines
    pygame.draw.circle(screen, (50, 50, 50), jsToSS((0,0)), 5) # center of graph point
    pygame.draw.circle(screen, (255, 255, 255), jsToSS((0, 0)), 128, 1) # large boundary circle


###### MAINLOOP ######

running = True # Runs the game loop
while running:
    screen.fill((10,10,10))
    pygame.draw.rect(screen, (0, 0, 0), (100, 100, 50, 50))  # Example rectangle

    jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module

    ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
    drawPoint(ssCoords) # draws a red point on the location of the joystick

    jsm.updateKeylog()

    for event in pygame.event.get(): # checks if program is quit, if so stops the code
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # runs framerate wait time
    clock.tick(fps)
    # update the screen
    pygame.display.update()
    #time.sleep(1)

# quit Pygame
pygame.quit()