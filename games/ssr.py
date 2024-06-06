###### IMPORT ######
import pygame
import random
import JSmanager as jsm
import Joystick_Test as jst
import copy

###### INITIALIZE ######
width, height = 1024, 600
windowSize = (width, height)
fps = 60
clock = pygame.time.Clock()

pygame.init()
font = pygame.font.Font("fonts/Retro Gaming.ttf", 32)

jsm.keylog
oldNews = False
buttonNews = False

arrowsOnScreen = []

up = pygame.image.load("images/SSRUp.png")
right = pygame.image.load("images/SSRRight.png")
left = pygame.image.load("images/SSRLeft.png")

###### FUNCTIONS ######
def cascade():
    for arrow in arrowsOnScreen:
        arrow[1] += 2

###### MAINLOOP ######      
def run(screen):
    def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
        jX, jY = jsCoords[0], jsCoords[1]
        x, y = jX + windowSize[0]/2, jY + windowSize[1]/2
        return (int(x), int(y))
    def drawPoint(SScoords):
        pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

    running = True
    waitIterator = 0

    centeredMouseX = jst.giveCoords()[0]
    trueUserSlot = (abs(centeredMouseX) > 50) * ((centeredMouseX > 0) - 0.5) * 2 * 100 + width/2
    chaseUserSlot = trueUserSlot

    while running:
        screen.fill((75, 30, 30))
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        jsm.updateKeylog()
        waitIterator += 1

        centeredMouseX = jst.giveCoords()[0]
        trueUserSlot = (abs(centeredMouseX) > 50) * ((centeredMouseX > 0) - 0.5) * 2 * 100 + width/2
        chaseUserSlot += (trueUserSlot - chaseUserSlot) * 0.3
        
        if waitIterator % 10 == 0:
            lane = random.choice([width/2 - 100, width/2, width/2 + 100])
            arrowsOnScreen.append([lane, 100])
        
        cascade()

        for arrow in arrowsOnScreen:
            if arrow[1] > height - 100:
                arrowsOnScreen.remove(arrow)
            ypos = -80000 / (arrow[1] - 650) - 80
            pygame.draw.circle(screen, [255,255,255], (width/2 + ((arrow[0] - width/2) * (-80000 / (arrow[1] - 650)) / (height - 100)), ypos), ypos / 10)

        pygame.draw.circle(screen, [255,255,0], (chaseUserSlot, height-100), 10)
        for event in pygame.event.get(): # checks if program is quit, if so stops the code
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        if jst.giveBackButton():
            running = False

        drawPoint(ssCoords) # draws a red point on the location of the joystick
        # runs framerate wait time
        clock.tick(fps)
        # update the screen
        pygame.display.update()
    
    return -1