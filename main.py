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

windowSize = (1280, 720)

pygame.display.set_caption("Project HappyStick") # Sets title of window
screen = pygame.display.set_mode(windowSize)#, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font(None, 36)

###### INITIALIZE ######

jsm.keylog

fps = 60
clock = pygame.time.Clock()
initialTime = time.time()
oldNews = True

menuButtons = [
    "Games",
    "Stats",
    "Options"
]

games = [
    "Galaga",
    "Turrican",
    "Dance Dance Revolution",
    "Tetris",
    "Poly Bridge"
]

selected = 0

###### OPERATOR FUNCTIONS ######

def dist(point1, point2): # calculates the distance between two points
    return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def dir(point1, point2): # calculates the direction between one point and another
    return atan2((point2[1] - point1[1]), (point2[0] - point1[0]))

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
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 100))  # Example rectangle

    #drawTestBG()
    jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
    #print(jsCoords)

    ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
    drawPoint(ssCoords) # draws a red point on the location of the joystick


    ### BUTTON LOOPS ###
    buttonPositions = []

    centerX = 200
    centerY = windowSize[1] / 2
    for game in games: # loops through all of the games to draw the boxes
        pygame.draw.rect(screen, (255, 255, 255), (centerX - 150, centerY - 150, 300, 300), 2, border_radius=10)
        buttonPositions.append((game, (centerX, centerY)))
        centerX += 320
    
    centerX = 20
    centerY = windowSize[1] - 90
    for menuButton in menuButtons: # loops through all of the menu buttons to draw the boxes
        pygame.draw.rect(screen, (255, 255, 255), (centerX, centerY, (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons), 70), 2, border_radius=10)
        buttonPositions.append((menuButton, (centerX + (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) / 2, centerY + 35)))
        centerX += (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) + 10

    ### BUTTON MANAGEMENT ###
    for index, object in enumerate(buttonPositions):
        if index == selected:
            pygame.draw.circle(screen, (255, 255, 0), object[1], 5) # center of graph point

            relativePolarCoords = []
            for index1, object1 in enumerate(buttonPositions):
                if index1 != index: # ignores the selected button when checking
                    relativePolarCoords.append((dist(object[1], object1[1]), dir(object[1], object1[1]))) # grabs the distance to and direction to all of the buttons from the hovered button
                    pygame.draw.aaline(screen, (255, 255, 255), object[1], object1[1])
                    #pygame.draw.aaline(screen, (255, 255, 0), object[1], (object[1][0] + 128 * cos(relativePolarCoords[-1][1]), object[1][1] + 128 * sin(relativePolarCoords[-1][1])))
                    
            relativePolarCoords.sort(key = lambda x:x[0])

            acceptedRelations = []
            for relation in relativePolarCoords:
                blocked = False
                for comparator in acceptedRelations:
                    if dist((cos(relation[1]), sin(relation[1])), (cos(comparator[1]), sin(comparator[1]))) < 0.8:
                        blocked = True
                if blocked == False:
                    acceptedRelations.append(relation)
            
            for relation in acceptedRelations:
                pygame.draw.aaline(screen, (255, 255, 0), object[1], (object[1][0] + 128 * cos(relation[1]), object[1][1] + 128 * sin(relation[1])))
                None
    
    # We have found the branches of all the closest buttons to the selected. Next we need to figure out which one the player is going to based on their js position

    jsm.updateKeylog()

    if jsm.keylog[-1][0] != "-1" and not oldNews:
        selected = (selected + 1)*(selected != len(buttonPositions) - 1)
        oldNews = True

    if jsm.keylog[-1][0] == "-1":
        oldNews = False

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