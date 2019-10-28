import pygame
from room import room
from tile import tile

class vacuum:
    def __init__(self, room):
        self.img = pygame.image.load("vacuum.png")
        self.room = room

    def set_position(self, row, col):
        old = self.room.vacuum_position()
        window = self.room.get_window()
        cell_size = self.room.get_cell_size()
        self.room.set_vacuum(row, col)
        pygame.draw.rect(window, (0,0,0),((col*cell_size)+1, (row*cell_size)+1, cell_size-2, cell_size-2)
        pygame.blit(self.img, (((col*cell_size)+2), ((row*cell_size)+2))
        pygame.display.update()

    def move_up(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(!grid[row][col].has_up_border() and row > 0):
            set_position(row-1, col)
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def move_down(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(!grid[row][col].has_down_border() and row < self.room.get_rows()-1):
            set_position(row+1, col)
        else:
            raise Exception("Invalid move! Cannot move down from current position.")

    def move_right(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(!grid[row][col].has_right_border() and col < self.room.get_cols()-1):
            set_position(row, col+1)
        else:
            raise Exception("Invalid move! Cannot move right from current position.")

    def move_left(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(!grid[row][col].has_left_border() and col > 0):
            set_position(row, col-1)
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def clean(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(grid[row][col].has_dirt()):
            self.room.clean_tile(row, col)
            set_position(row, col)
        else:
            pass
