import pygame
import time
from math import *

initialTime = time.time()
windowSize = (1024, 600)

def giveCoords():
    if sqrt((pygame.mouse.get_pos()[0] - windowSize[0]/2) ** 2 + (pygame.mouse.get_pos()[1] - windowSize[1]/2) ** 2) < 200:
        value = (0, 0)
    else:
        #dir = atan2(pygame.mouse.get_pos()[1] - 360, pygame.mouse.get_pos()[0] - 640)
        #return (-129 * cos(dir), 129 * sin(dir))
        value = (-pygame.mouse.get_pos()[0] * 256 / windowSize[0] + 128, pygame.mouse.get_pos()[1] * 256 / windowSize[1] - 128)
    #return [cos(time.time() - initialTime) * 128, sin(time.time() - initialTime) * 128] # replace the x and y components to the input from the joystick]
    if pygame.key.get_pressed()[pygame.K_UP]:
        value = (0, -128)
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        value = (-128, 0)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        value = (0, 128)
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        value = (128, 0)
    return value

def giveButton():
    return pygame.mouse.get_pressed()[0]