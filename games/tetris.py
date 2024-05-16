import pygame

width, height = 1024, 600
fps = 60
clock = pygame.time.Clock()

def run(screen):

    running = True
    while running:
        screen.fill((30, 30, 75))

        horizontalTiles = 10
        verticalTiles = 20
        tileSize = 40

        boardWidth = (horizontalTiles + 1) / 2 * tileSize
        boardHeight = (verticalTiles + 1) / 2 * tileSize
        pygame.draw.rect(screen, (20, 20, 50), ((width - boardWidth)/2, (height - boardHeight)/2, boardWidth, boardHeight))

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