###### IMPORT ######
import pygame
import random
import JSmanager as jsm
import Joystick_Test as jst

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

###### FUNCTIONS ######

###### MAINLOOP ######      
def run(screen):
    def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
        jX, jY = jsCoords[0], jsCoords[1]
        x, y = jX + windowSize[0]/2, jY + windowSize[1]/2
        return (int(x), int(y))
    def drawPoint(SScoords):
        pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

    running = True

    while running:
        screen.fill((75, 30, 30))
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        jsm.updateKeylog()

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