import pygame
import time
from math import *

initialTime = time.time()

def giveCoords():
    return [cos(time.time() - initialTime) * 128, sin(time.time() - initialTime) * 128] # replace the x and y components to the input from the joystick]