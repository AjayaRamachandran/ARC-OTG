###### IMPORT ######
import pygame
import random
import JSmanager as jsm
import Joystick_Test as jst
import copy
from PIL import Image

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

edgeRule = [
    [0, 0], [2, 2],
    [0, 1], [2, 20],
    [1, 0], [20, 2],
    [1, 1], [20, 20]
]

kernel = [
    [-1, 1],
    [0, 1],
    [1, 1],
    [-1, 0],
    [1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
]

###### FUNCTIONS ######
def generateLevel(width, length, roomSize, iterations):
    level = []
    for x in range(2 * width + 1):
        row = []
        for y in range(2 * length + 1):
            row.append(".")
        level.append(row)
    
    agentX = 1
    agentY = 1
    level[agentX][agentY] = "0"
    pastPositions = []
    options = ["r", "d"]
    iter = 0
    while iter < iterations:
        iter += 1
        options = ["u","d","l","r"]
        if agentX == 1:
            options.remove("l")
        elif level[agentX - 2][agentY] == "0":
            options.remove("l")
        if agentX == width * 2 - 1:
            options.remove("r")
        elif level[agentX + 2][agentY] == "0":
            options.remove("r")
        if agentY == 1:
            options.remove("u")
        elif level[agentX][agentY - 2] == "0":
            options.remove("u")
        if agentY == length * 2 - 1:
            options.remove("d")
        elif level[agentX][agentY + 2] == "0":
            options.remove("d")

        if options != []:
            choice = random.choice(options)
            if choice == "r":
                for i in range(2):
                    agentX += 1
                    level[agentX][agentY] = "0"
                pastPositions.append([agentX, agentY])
            if choice == "l":
                for i in range(2):
                    agentX -= 1
                    level[agentX][agentY] = "0"
                pastPositions.append([agentX, agentY])
            if choice == "u":
                for i in range(2):
                    agentY -= 1
                    level[agentX][agentY] = "0"
                pastPositions.append([agentX, agentY])
            if choice == "d":
                for i in range(2):
                    agentY += 1
                    level[agentX][agentY] = "0"
                pastPositions.append([agentX, agentY])
        else:
            [agentX, agentY] = random.choice(pastPositions)

    generatedLevel = []
    smallLevel = []
    for index, col in enumerate(level):
        if index % 2 == 1:
            for i in range(roomSize - 1):
                generatedLevel.append(col)
        generatedLevel.append(col)
        smallLevel.append(col)

    newGeneratedLevel = copy.deepcopy(generatedLevel)

    for outerIndex, col in enumerate(generatedLevel):
        newGeneratedLevel[outerIndex] = []
        for index in range(len(col)):
            if index % 2 == 1:
                for i in range(roomSize - 1):
                    newGeneratedLevel[outerIndex].append(generatedLevel[outerIndex][index])
            newGeneratedLevel[outerIndex].append(generatedLevel[outerIndex][index])

    for row in range(len(smallLevel)):
        for cell in range(len(smallLevel[i])):
            border = 0
            for item in kernel:
                if item[0] + row >= 0 and item[0] + row <= len(smallLevel[i]) - 1 and item[1] + cell >= 0 and item[1] + cell <= len(smallLevel) - 1:
                    if smallLevel[item[0] + row][item[1] + cell] == "0" and smallLevel[row][cell] == ".":
                        border = 1
            if border == 1:
                smallLevel[row][cell] = "1"
        print(smallLevel[row])

    image = Image.new("RGBA", (len(newGeneratedLevel[0]), len(newGeneratedLevel)))
    for y, row in enumerate(newGeneratedLevel):
        for x, pixel in enumerate(row):
            if pixel == ".":
                image.putpixel((x, y), (0,0,0,255))
            if pixel == "0":
                image.putpixel((x, y), (255,255,255,255))
    image.save("finaloutput.png")
    return smallLevel

#generateLevel(5, 5, 3, 8)

###### MAINLOOP ######      
def run(screen):
    def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
        jX, jY = jsCoords[0], jsCoords[1]
        x, y = jX + windowSize[0]/2, jY + windowSize[1]/2
        return (int(x), int(y))
    def drawPoint(SScoords):
        pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

    level = generateLevel(5, 5, 3, random.randint(5,10))
        
    running = True

    while running:
        screen.fill((30, 75, 30))
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        jsm.updateKeylog()

        position = [0,0]
        for row in range(len(level)):
            position[0] = 0
            for cell in range(len(level[row])):
                dimensions = [edgeRule[edgeRule.index([cell%2, row%2]) + 1][a] * 5 for a in range(2)]
                if level[row][cell] == "0":
                    pygame.draw.rect(screen, [40, 90, 40], [position, dimensions])
                if level[row][cell] == "1":
                    pygame.draw.rect(screen, [255, 255, 255], [position, dimensions])
                if level[row][cell] == ".":
                    None
                position[0] += dimensions[0]
                #position[0] += 60
            position[1] += dimensions[1]
            #position[1] += 60

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