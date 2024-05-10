import pygame
import time
from math import *

initialTime = time.time()

def giveCoords():
    if sqrt((pygame.mouse.get_pos()[0] - 640) ** 2 + (pygame.mouse.get_pos()[1] - 360) ** 2) < 200:
        return (0, 0)
    else:
        #dir = atan2(pygame.mouse.get_pos()[1] - 360, pygame.mouse.get_pos()[0] - 640)
        #return (-129 * cos(dir), 129 * sin(dir))
        return (-pygame.mouse.get_pos()[0] / 5 + 128, pygame.mouse.get_pos()[1] * 256 / 720 - 128)
    #return [cos(time.time() - initialTime) * 128, sin(time.time() - initialTime) * 128] # replace the x and y components to the input from the joystick]