###### IMPORT ######
import pygame

###### INITIALIZE ######
width, height = 1024, 600
fps = 60
clock = pygame.time.Clock()

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


###### MAINLOOP ######      
def run(screen):

    running = True
    while running:
        screen.fill((30, 30, 75))

        horizontalTiles = 10
        verticalTiles = 20
        board = []
        [board.append("..........") for row in range(verticalTiles)]
        tileSize = 20

        boardWidth = horizontalTiles * tileSize
        boardHeight = verticalTiles * tileSize
        pygame.draw.rect(screen, (20, 20, 50), ((width - boardWidth)/2, (height - boardHeight)/2, boardWidth, boardHeight))

        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                color = [min(255, 130 + 255*(cell == "0")), min(255, 130 + 255*(cell == "0")), min(255, 175 + 255*(cell == "0"))]
                pygame.draw.rect(screen, color, [x * tileSize + (width - boardWidth)/2, y * tileSize + (height - boardHeight)/2, 2, 2])



        for event in pygame.event.get(): # checks if program is quit, if so stops the code
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # runs framerate wait time
        clock.tick(fps)
        # update the screen
        pygame.display.update()
    
    return -1