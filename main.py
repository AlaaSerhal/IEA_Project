import pygame
from room import room
def main():
    rows = int(input("please enter number of rows as an integer: "))
    cols = int(input("please enter number of columns as an integer: "))
    print("borders will be randomly placed")
    CELL_SIZE = 60
    window_size = [cols * CELL_SIZE, rows * CELL_SIZE]

    pygame.init()

    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Vacuum Cleaner Agent")
    run = True
    clock = pygame.time.Clock()
    r = room(CELL_SIZE, rows, cols, window)
    r.draw_grid()
    r.draw_borders()
    while run:
        pygame.time.delay(50)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # r.draw_grid()
        # r.draw_borders()
        pygame.display.update()
        # pygame.display.flip()

    pygame.quit()

main()
