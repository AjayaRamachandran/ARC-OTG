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

jsm.keylog
oldNews = False

board = []

shapes = [
    [
        "..0.",
        "..0.",
        "..0.",
        "..0.",
    ],
    [
        "00",
        "00"
    ],
    [
        ".0.",
        ".0.",
        "00."
    ],
    [
        ".0.",
        ".0.",
        ".00"
    ],
    [
        ".0.",
        ".00",
        "..0"
    ],
    [
        "..0",
        ".00",
        ".0."
    ],
    [
        ".0.",
        ".00",
        ".0."
    ]
]

###### OPERATOR FUNCTIONS ######
def rotate(matrix):
    return list(zip(*matrix[::-1]))

def cascade(highestStaticRow):
    global board
    board.pop(highestStaticRow)
    board.insert(0, "..........")

def stamp(shape, row, column, erase):
    global board
    for srIndex, shaperow in enumerate(shape):
        for scIndex, shapecell in enumerate(shaperow):
            if shapecell == "0":
                if erase and (column + scIndex < horizontalTiles and column + scIndex > -1):
                    board[row + srIndex] = board[row + srIndex][:column + scIndex] + "." + board[row + srIndex][column + scIndex + 1:]
                    #board[row + srIndex][column + scIndex] = "0"
                elif column + scIndex < horizontalTiles and column + scIndex > -1:
                    #print(row+srIndex)
                    #board[row + srIndex][column + scIndex] = "."
                    board[row + srIndex] = board[row + srIndex][:column + scIndex] + "0" + board[row + srIndex][column + scIndex + 1:]

###### MAINLOOP ######      
def run(screen):
    def jsToSS(jsCoords): # function to converts joystick coordinates (-128, 128) to screen space coordinates
        jX, jY = jsCoords[0], jsCoords[1]
        x, y = -jX + windowSize[0]/2, jY + windowSize[1]/2
        return (int(x), int(y))
    def drawPoint(SScoords):
        pygame.draw.circle(screen, (255, 0, 0), SScoords, 4)

    global board, boardWidth, boardHeight, tileSize, horizontalTiles, verticalTiles

    waitIterator = 0
    running = True
    horizontalTiles = 10
    verticalTiles = 20
    board = []
    [board.append("..........") for row in range(verticalTiles)]
    tileSize = 25
    spawnNew = True

    while running:
        screen.fill((30, 30, 75))
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        jsm.updateKeylog()
        waitIterator += 1

        boardWidth = horizontalTiles * tileSize
        boardHeight = verticalTiles * tileSize
        pygame.draw.rect(screen, (20, 20, 50), ((width - boardWidth)/2, (height - boardHeight)/2, boardWidth, boardHeight))

        if waitIterator%20 == 0:
            if spawnNew:
                currentBlock = random.choice(shapes)
                blockColumn = random.randint(0, horizontalTiles-3)
                blockRow = 0
                spawnNew = False
            stamp(currentBlock, blockRow, blockColumn, True)
            #cascade(verticalTiles - 1)
            #print(jsm.keylog)
            if jsm.keylog[-1][0] == "u" and not oldNews:
                oldNews = True
                currentBlock = rotate(currentBlock)
            if jsm.keylog[-1][0] == "r" and not oldNews:
                blockColumn = min(horizontalTiles-1, blockColumn + 1)
                for row in range(len(currentBlock)):
                    for index, cell in enumerate(currentBlock[row]):
                        if cell == "0":
                            if blockColumn + index >= horizontalTiles:
                                failed = True
                            elif board[blockRow + row][blockColumn + index] == "0":
                                failed = True
                if failed:
                    blockColumn -= 1
            if jsm.keylog[-1][0] == "l" and not oldNews:
                blockColumn = max(0, blockColumn - 1)
                for row in range(len(currentBlock)):
                    for index, cell in enumerate(currentBlock[row]):
                        if cell == "0":
                            if blockColumn + index < 0:
                                failed = True
                            elif board[blockRow + row][blockColumn + index] == "0":
                                failed = True
                if failed:
                    blockColumn += 1
            if jsm.keylog[-1][0] == "d" and not oldNews:
                blockRow += 1
                failed = False
                for row in range(len(currentBlock)):
                    for index, cell in enumerate(currentBlock[row]):
                        if cell == "0":
                            if blockRow + row >= verticalTiles:
                                failed = True
                            elif board[blockRow + row][blockColumn + index] == "0":
                                failed = True
            if jsm.keylog[-1][0] == "-1":
                oldNews = False
            blockRow += 1
            failed = False
            for row in range(len(currentBlock)):
                for index, cell in enumerate(currentBlock[row]):
                    if cell == "0":
                        if blockRow + row >= verticalTiles:
                            failed = True
                        elif board[blockRow + row][blockColumn + index] == "0":
                            failed = True
                        
            if failed:
                blockRow -= 1
                spawnNew = True
            stamp(currentBlock, blockRow, blockColumn, False)
            

        
        #if waitIterator%100 == 0:
            #stamp(random.choice(range(len(shapes))), 1, random.randint(0, horizontalTiles-3), False)

        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                pygame.draw.rect(screen, color, [x * tileSize + (width - boardWidth)/2, y * tileSize + (height - boardHeight)/2, tileSize, tileSize], 2)

        for event in pygame.event.get(): # checks if program is quit, if so stops the code
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        drawPoint(ssCoords) # draws a red point on the location of the joystick
        # runs framerate wait time
        clock.tick(fps)
        # update the screen
        pygame.display.update()
    
    return -1