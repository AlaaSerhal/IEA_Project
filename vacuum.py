import pygame
from room import room

class vacuum:
    def __init__(self, room):
        self.img = pygame.image.load("vacuum.png")
        self.room = room

    def get_position(self):
        return self.room.vacuum_position()

    def set_position(self, row, col):
        old = get_position()
        window = self.room.get_window()
        cell_size = self.room.get_cell_size()
        self.room.set_vacuum(row, col)
        pygame.draw.rect(window, (0,0,0),((col*cell_size)+1, (row*cell_size)+1, cell_size-2, cell_size-2)
        pygame.blit(self.img, (((col*cell_size)+2), ((row*cell_size)+2))
        pygame.display.update()

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass

    def clean(self):
        pass
