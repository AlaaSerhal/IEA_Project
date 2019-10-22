import pygame
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 70
HEIGHT = 70
MARGIN = 1.5
grid = []
for row in range(7):
    grid.append([])
    for column in range(7):
        grid[row].append(0)
pygame.init()
WINDOW_SIZE = [500, 500]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Vaccum Cleaner Agent")
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
    screen.fill(BLACK)
    for row in range(7):
        for column in range(7):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    clock.tick(60)
    pygame.display.flip()
pygame.quit()