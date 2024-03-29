# Created by Ajaya Ramachandran and Jacob Nuttall
# Project HappyStick 2024

###### IMPORT ######

import pygame
import Joystick_Test as jst
import random
import time
from math import *
import numpy as np

###### SETUP ######
pygame.init()

windowSize = (360, 360)

pygame.display.set_caption("Project HappyStick") # Sets title of window
screen = pygame.display.set_mode(windowSize) # Sets the dimensions of the window to the windowSize
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)

jsCoords = [0, 0]
initialTime = time.time()
keylog = [["-1", time.time()]]
deadZone = 5

###### INITIALIZE ######

fps = 60
clock = pygame.time.Clock()

###### OPERATOR FUNCTIONS ######
def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
    jX, jY = jsCoords[0], jsCoords[1]
    x, y = -jX + windowSize[0]/2, jY + windowSize[1]/2
    return (x, y)

def dist(point1, point2): # calculates the distance between two points
    return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def dir(point1, point2): # calculates the direction between one point and another
    return degrees(atan2((point2[1] - point1[1]), (point2[0] - point1[0])) + pi)

###### MAIN FUNCTIONS ######

def drawPoint(SScoords):
    pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

def testProgram():
    running = True # Runs the game loop
    while running:
        screen.fill((0,0,0))

        start = -112
        for line in range(15):
            x = start + line*16
            pygame.draw.aaline(screen, (50, 50, 50), jsToSS((x, sqrt(128**2 - x**2))), jsToSS((x, -sqrt(128**2 - x**2)))) # vertical gridlines
        
        for line in range(15):
            y = start + line*16
            pygame.draw.aaline(screen, (50, 50, 50), jsToSS((sqrt(128**2 - y**2), y)), jsToSS((-sqrt(128**2 - y**2), y))) # horizontal gridlines
        
        pygame.draw.circle(screen, (50, 50, 50), jsToSS((0,0)), 5) # center of graph point
        pygame.draw.circle(screen, (255, 255, 255), jsToSS((0, 0)), 128, 1) # large boundary circle

        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module

        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        drawPoint(ssCoords) # draws a red point on the location of the joystick

        if dist((0, 0), jsCoords) > deadZone: # runs the detection of the joystick's "moves" if it has left the deadzone
            if 45 <= dir((0, 0), jsCoords) < 135 and not keylog[-1][0] == "u": # pointing up
                keylog.append(["u", time.time()])
                print(["u", time.time()])

            elif 135 <= dir((0, 0), jsCoords) < 225 and not keylog[-1][0] == "l": # pointing left
                keylog.append(["l", time.time()])
                print(["l", time.time()])

            elif 225 <= dir((0, 0), jsCoords) < 315 and not keylog[-1][0] == "d": # pointing down
                keylog.append(["d", time.time()])
                print(["d", time.time()])
                
            elif 45 <= dir((0, 0), jsCoords) < 0 or 315 < dir((0, 0), jsCoords) <= 360 and not keylog[-1][0] == "r": # pointing right
                keylog.append(["r", time.time()])
                print(["r", time.time()])

        elif not keylog[-1][0] == "-1":
            keylog.append(["-1", time.time()])
            print(["-1", time.time()])

        for direction in ["u", "r", "d", "l"]: # detects "double-moves" and if so updates the keylog
            if [item[0] for item in keylog[-3:]] == [direction, "-1", direction] and keylog[-1][1] - keylog[-3][1] < 0.5:
                keylog[-1][0] = direction + direction

        for event in pygame.event.get(): # checks if program is quit, if so stops the code
            if event.type == pygame.QUIT:
                running = False
        # runs framerate wait time
        clock.tick(fps)
        # update the screen
        pygame.display.update()
        #time.sleep(1)

    # quit Pygame
    pygame.quit()

testProgram()

