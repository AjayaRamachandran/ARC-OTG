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
def rotate(matrix, direction):
    matrix1 = copy.deepcopy(matrix)
    if direction == "r":
        return list(zip(*matrix1[::-1]))
    if direction == "l":
        for i in range(3):
            matrix1 = list(zip(*matrix1[::-1]))
        return matrix1

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

    global board, boardWidth, boardHeight, tileSize, horizontalTiles, verticalTiles, oldNews, buttonNews, running, waitIterator, spawnNew, score, pastRowsCleared, frameTime, nextBlock, holdPiece

    def resetGame():
        global board, boardWidth, boardHeight, tileSize, horizontalTiles, verticalTiles, oldNews, buttonNews, running, waitIterator, spawnNew, score, pastRowsCleared, frameTime, nextBlock, holdPiece
        waitIterator = 0
        running = True
        horizontalTiles = 10
        verticalTiles = 20
        board = []
        [board.append("..........") for row in range(verticalTiles)]
        tileSize = 25
        spawnNew = True
        score = 0
        pastRowsCleared = [0]
        frameTime = 3000
        nextBlock = random.choice(shapes)
        holdPiece = []
        buttonNews = True

    def endGame():
        resetGame()

    resetGame()
    while running:
        screen.fill((30, 30, 75))
        jsCoords = jst.giveCoords() # retrieves the input coordinates from the relevant module
        ssCoords = jsToSS(jsCoords) # converts the joystick coordinates into screen space coordinates
        jsm.updateKeylog()
        waitIterator += 1

        boardWidth = horizontalTiles * tileSize
        boardHeight = verticalTiles * tileSize
        pygame.draw.rect(screen, (20, 20, 50), ((width - boardWidth)/2, (height - boardHeight)/2, boardWidth, boardHeight))

        text = font.render("TETRIS", False, (255,255,255))
        textR = ((20, 20), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)

        text = font.render("SCORE", False, (255,255,255))
        textR = ((width - 200 - text.get_rect()[2]/2, height/2 - 125 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)
    
        text = font.render(str(score), False, (255,255,255))
        textR = ((width - 200 - text.get_rect()[2]/2, height/2 - 75 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)

        text = font.render("MAX", False, (255,255,255))
        textR = ((width - 200 - text.get_rect()[2]/2, height/2 + 75 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)
    
        text = font.render(str(score), False, (255,255,255))
        textR = ((width - 200 - text.get_rect()[2]/2, height/2 + 125 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)

        text = font.render("NEXT", False, (255,255,255))
        textR = ((200 - text.get_rect()[2]/2, height/2 - 140 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)

        text = font.render("HOLD", False, (255,255,255))
        textR = ((200 - text.get_rect()[2]/2, height/2 + 60 - text.get_rect()[3]/2), (text.get_rect()[2], text.get_rect()[3]))
        screen.blit(text, textR)
        
        if spawnNew:
            currentBlock = nextBlock
            nextBlock = random.choice(shapes)
            
            blockColumn = random.randint(0, horizontalTiles-3)
            blockRow = 0
            spawnNew = False
            numRowsCleared = 0
            for rows in range(len(board)):
                if board[rows] == "0000000000":
                    cascade(rows)
                    numRowsCleared += 1
            if numRowsCleared > 0:
                pastRowsCleared.append(numRowsCleared)
                score += int(numRowsCleared**2 * 100 + (pastRowsCleared[-1] == pastRowsCleared[-2] == 4) * 400)

        stamp(currentBlock, blockRow, blockColumn, True)
        #cascade(verticalTiles - 1)
        #print(jsm.keylog)
        if jsm.keylog[-1][0] == "u" and not oldNews:
            oldNews = True
            currentBlock = rotate(currentBlock, "r")
            for row in range(len(currentBlock)):
                for index, cell in enumerate(currentBlock[row]):
                    if cell == "0":
                        failed = False
                        if blockColumn + index >= horizontalTiles:
                            blockColumn -= 1
                        elif blockColumn + index < 0:
                            blockColumn += 1
                        elif board[blockRow + row][blockColumn + index] == "0":
                            failed = True
                            currentBlock = rotate(currentBlock, "l")
        if jsm.keylog[-1][0] == "r" and not oldNews:
            oldNews = True
            blockColumn = blockColumn + 1
            for row in range(len(currentBlock)):
                for index, cell in enumerate(currentBlock[row]):
                    if cell == "0":
                        failed = True
                        while failed == True:
                            if blockColumn + index >= horizontalTiles:
                                failed = True
                                blockColumn -= 1
                            elif board[blockRow + row][blockColumn + index] == "0":
                                failed = True
                                blockColumn -= 1
                            else:
                                failed = False
        if jsm.keylog[-1][0] == "l" and not oldNews:
            oldNews = True
            blockColumn = blockColumn - 1
            for row in range(len(currentBlock)):
                for index, cell in enumerate(currentBlock[row]):
                    if cell == "0":
                        failed = True
                        while failed == True:
                            if blockColumn + index < 0:
                                failed = True
                                blockColumn += 1
                            elif board[blockRow + row][blockColumn + index] == "0":
                                failed = True
                                blockColumn += 1
                            else:
                                failed = False
        if jsm.keylog[-1][0] == "d" and not oldNews:
            oldNews = True
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
        if jst.giveButton() and not buttonNews:
            buttonNews = True
            if holdPiece == []:
                holdPiece = currentBlock
                currentBlock = nextBlock
            else:
                currentBlock, holdPiece = holdPiece, currentBlock
        elif not jst.giveButton():
            buttonNews = False

        if jsm.keylog[-1][0] == "-1":
            oldNews = False
        if waitIterator % (round(frameTime/100)) == 0:
            blockRow += 1
            failed = False
            frameTime = max(1000, frameTime - 1)
        for row in range(len(currentBlock)):
            for index, cell in enumerate(currentBlock[row]):
                if cell == "0":
                    failed = False
                    if blockColumn + index >= horizontalTiles:
                        failed = True
                        blockColumn -= 1
                    if blockColumn + index < 0:
                        failed = True
                        blockColumn += 1
                    if blockRow + row >= verticalTiles:
                        failed = True
                        blockRow -= 1
                        spawnNew = True
                    if board[blockRow + row][blockColumn + index] == "0":
                        failed = True
                        blockRow -= 1
                        spawnNew = True

        stamp(currentBlock, blockRow, blockColumn, False)
        if spawnNew:
            if board[2] != "..........":
                endGame()       
        #if waitIterator%100 == 0:
            #stamp(random.choice(range(len(shapes))), 1, random.randint(0, horizontalTiles-3), False)

        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell == "0":
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [x * tileSize + (width - boardWidth)/2, y * tileSize + (height - boardHeight)/2, tileSize, tileSize])
                else:
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [x * tileSize + (width - boardWidth)/2, y * tileSize + (height - boardHeight)/2, tileSize, tileSize], 2)
        
        for y, row in enumerate(nextBlock):
            for x, cell in enumerate(row):
                if cell == "0":
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [(x - ((len(nextBlock))/2)) * tileSize + 200, (y - ((len(row))/2)) * tileSize + (height)/2 - 60, tileSize, tileSize])
                else:
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [(x - ((len(nextBlock))/2)) * tileSize + 200, (y - ((len(row))/2)) * tileSize + (height)/2 - 60, tileSize, tileSize], 2)

        for y, row in enumerate(holdPiece):
            for x, cell in enumerate(row):
                if cell == "0":
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [(x - ((len(holdPiece))/2)) * tileSize + 200, (y - ((len(row))/2)) * tileSize + (height)/2 + 140, tileSize, tileSize])
                else:
                    color = [min(255, 35 + 255*(cell == "0")), min(255, 35 + 255*(cell == "0")), min(255, 85 + 255*(cell == "0"))]
                    pygame.draw.rect(screen, color, [(x - ((len(holdPiece))/2)) * tileSize + 200, (y - ((len(row))/2)) * tileSize + (height)/2 + 140, tileSize, tileSize], 2)
        
        pygame.draw.line(screen, (255,0,0), ((width-boardWidth)/2, 3 * tileSize + (height - boardHeight)/2), ((width+boardWidth)/2, 3 * tileSize + (height - boardHeight)/2), 4)

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