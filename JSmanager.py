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

jsCoords = [0, 0]
initialTime = time.time()
keylog = [["-1", time.time()]]
deadZone = 5

###### OPERATOR FUNCTIONS ######

def dist(point1, point2): # calculates the distance between two points
    return sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def dir(point1, point2): # calculates the direction between one point and another
    return degrees(atan2((point2[1] - point1[1]), (point2[0] - point1[0])) + pi)

###### MAIN FUNCTIONS ######
def updateKeylog():
    jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module

    if dist((0, 0), jsCoords) > deadZone: # runs the detection of the joystick's "moves" if it has left the deadzone
        if 45 <= dir((0, 0), jsCoords) < 135 and not keylog[-1][0] == "u": # pointing up
            keylog.append(["u", time.time()])

        elif 135 <= dir((0, 0), jsCoords) < 225 and not keylog[-1][0] == "l": # pointing left
            keylog.append(["l", time.time()])

        elif 225 <= dir((0, 0), jsCoords) < 315 and not keylog[-1][0] == "d": # pointing down
            keylog.append(["d", time.time()])
            
        elif 0 <= dir((0, 0), jsCoords) < 45 or 315 < dir((0, 0), jsCoords) <= 360 and not keylog[-1][0] == "r": # pointing right
            keylog.append(["r", time.time()])

    elif not keylog[-1][0] == "-1":
        keylog.append(["-1", time.time()])

    for direction in ["u", "r", "d", "l"]: # detects "double-moves" and if so updates the keylog
        if [item[0] for item in keylog[-3:]] == [direction, "-1", direction] and keylog[-1][1] - keylog[-3][1] < 0.5:
            keylog[-1][0] = direction + direction


