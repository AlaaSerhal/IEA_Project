import pygame
from room import room
def main():
    rows, cols = 15, 15
    while(rows >= 15 or cols >= 15 or rows == 0 or cols == 0):
        rows = int(input("please enter number of rows as an integer: "))
        cols = int(input("please enter number of columns as an integer: "))
    print("borders will be randomly placed")
    CELL_SIZE = 40
    window_size = [cols * CELL_SIZE, rows * CELL_SIZE]

    pygame.init()

    dirt_img = pygame.image.load("dirt.png")

    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Vacuum Cleaner Agent")
    run = True
    clock = pygame.time.Clock()
    r = room(CELL_SIZE, rows, cols, window)
    r.draw_grid()
    r.draw_borders()
    # window.blit(vacuum_img, (50,50))
    window.blit(dirt_img, (200,200))
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()

main()
