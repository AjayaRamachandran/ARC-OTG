###### IMPORT ######

import pygame
import Joystick_Test as jst
import random
import time
from math import *
import numpy as np
import JSmanager as jsm

from games import tetris

###### SETUP ######

pygame.init()
screenDimensions = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print(screenDimensions)

windowSize = (1024, 600)

pygame.display.set_caption("Project HappyStick") # Sets title of window
screen = pygame.display.set_mode(windowSize)#, pygame.FULLSCREEN) # Sets the dimensions of the window to the windowSize
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

font = pygame.font.Font("fonts/Retro Gaming.ttf", 32)

###### INITIALIZE ######

jsm.keylog

fps = 60
clock = pygame.time.Clock()

initialTime = time.time()
oldNews = True
clickStatus = False
oldClickStatus = False
rowOffsetX = 0
chaseOffsetX = 0
currentPage = "GAMES"
button1Clicked = False

menuButtons = [
    "GAMES",
    "STATS",
    "OPTIONS",
]

games = [
    "Tetris",
    "Galaga",
    "Turrican",
    "Dance Dance Revolution",
    "Terraria",
    "Mariokart",
    "Poly Bridge"
]

gamePics = [
    "images/Game1.png",
    "images/Game2.png",
    "images/Game3.png",
    "images/Game4.png",
    "images/Game5.png",
    "images/Game6.png",
    "images/Game7.png",
]

background = pygame.image.load("images/Background2.png")
background = pygame.transform.scale(background, windowSize)
backgroundRect = background.get_rect()

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
    return (int(x), int(y))

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
home = True
while running:
    if home:
        #screen.fill((50,110,60))
        screen.blit(background, backgroundRect)
        pygame.draw.rect(screen, (35, 75, 40), (0, 610, 1280, 720))
        #pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 100))  # Example rectangle

        ### ON-SCREEN BUTTON LOOPS ###
        buttonPositions = []

        centerX = 200
        centerY = windowSize[1] / 2
        chaseOffsetX += (rowOffsetX - chaseOffsetX) * 0.2
        for index, game in enumerate(games): # loops through all of the games to draw the boxes
            #pygame.draw.rect(screen, (255, 255, 255), (centerX - 152 + chaseOffsetX, centerY - 152, 304, 304), 2, border_radius=10)
            gameCover = pygame.image.load(gamePics[index])
            gameCoverRect = (centerX - 150 + chaseOffsetX, centerY - 150, 300, 300)
            screen.blit(gameCover, gameCoverRect)
            gameCover = None
            gameCoverRect = None
            buttonPositions.append((game, (centerX + chaseOffsetX, centerY)))
            centerX += 320
        centerX = 20
        centerY = windowSize[1] - 90
        for menuButton in menuButtons: # loops through all of the menu buttons to draw the boxes
            pygame.draw.rect(screen, (15, 30, 15), (centerX, centerY, (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons), 70))
            buttonPositions.append((menuButton, (centerX + (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) / 2, centerY + 35)))
            buttonText = font.render(menuButton, False, (255,255,255))
            buttonTextRect = buttonText.get_rect()
            screen.blit(buttonText, (centerX + (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) / 2 - buttonTextRect[2]/2, centerY + 35 - buttonTextRect[3]/2))
            centerX += (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) + 10
        pygame.draw.rect(screen, (255, 255, 255), (20, 20, 40, 40), 2)#, border_radius=10)
        buttonPositions.append((menuButton, (40, 40)))

        ### BUTTON MANAGEMENT ###
        for index, object in enumerate(buttonPositions):
            if index == selected:
                if index < len(buttonPositions) - 4:
                    pygame.draw.rect(screen, (255, 255, 255), (object[1][0] - 152, object[1][1] - 152, 304, 304), 2)
                elif index == len(buttonPositions) - 1:
                    pygame.draw.circle(screen, (255, 255, 0), (object[1][0], object[1][1]), 5) # center of graph point
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (object[1][0] - ((windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) / 2) - 2, object[1][1] - 70/2 - 2, (windowSize[0] - 40 - 10*(len(menuButtons) - 1)) / len(menuButtons) + 4, 74), 2)

                relativePolarCoords = []
                for index1, object1 in enumerate(buttonPositions):
                    if index1 != index: # ignores the selected button when checking
                        relativePolarCoords.append((dist(object[1], object1[1]), dir(object[1], object1[1]), index1)) # grabs the distance to and direction to all of the buttons from the hovered button
                        #pygame.draw.aaline(screen, (255, 255, 255), object[1], object1[1])
                        #pygame.draw.aaline(screen, (255, 255, 0), object[1], (object[1][0] + 128 * cos(relativePolarCoords[-1][1]), object[1][1] + 128 * sin(relativePolarCoords[-1][1])))
                        
                relativePolarCoords.sort(key = lambda x:x[0])

                acceptedRelations = []
                for relation in relativePolarCoords: # Looks through all the button relations to determine which are viable options
                    blocked = False
                    for comparator in acceptedRelations:
                        if dist((cos(relation[1]), sin(relation[1])), (cos(comparator[1]), sin(comparator[1]))) < 0.8: # Makes sure each new button option is sufficiently distanced (directionally) from the others
                            blocked = True
                    if blocked == False:
                        acceptedRelations.append(relation)
        
        # We have found the branches of all the closest buttons to the selected. Next we need to figure out which one the player is going to based on their js position

        #drawTestBG()
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module

        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        drawPoint(ssCoords) # draws a red point on the location of the joystick
        jsm.updateKeylog()
        
        if jst.giveBackButton() != oldClickStatus and oldClickStatus == False: # detects changes in the click status and makes updates accordingly
            pygame.draw.circle(screen, (0, 0, 255), (windowSize[0]/2, windowSize[1]/2), 500)
            button1Clicked = True
        else:
            button1Clicked = False
        
        if button1Clicked:
            if selected < len(games):
                if games[selected] == "Tetris":
                    home = False
                    tetris.run(screen)
                    home = True

        clickStatus = jst.giveBackButton()

        if jsm.keylog[-1][0] != "-1" and not oldNews:
            oldNews = True # makes sure the command is only run once per joystick movement
            unitMousePos = [-cos(dir((0,0), jsCoords)), sin(dir((0,0), jsCoords))]
            branchDistances = []
            for relation in acceptedRelations:
                branchDistances.append((dist(unitMousePos, (cos(relation[1]), sin(relation[1]))), relation[2]))
            branchDistances.sort(key = lambda x:x[0])

            if branchDistances[0][0] < 0.5: # makes sure that even if a specific button is the "closest", that it is within a certain threshold of the joystick direction
                selected = branchDistances[0][1]
            
            if buttonPositions[selected][1][0] > windowSize[0] - 200 and selected < len(buttonPositions) - 4:
                rowOffsetX -= 320
            if buttonPositions[selected][1][0] < 0:
                rowOffsetX += 320

        if jsm.keylog[-1][0] == "-1":
            oldNews = False

    for event in pygame.event.get(): # checks if program is quit, if so stops the code
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    if home:
        oldClickStatus = clickStatus
    # runs framerate wait time
    clock.tick(fps)
    # update the screen
    if home:
        pygame.display.update()
    #time.sleep(1)
# quit Pygame
pygame.quit()