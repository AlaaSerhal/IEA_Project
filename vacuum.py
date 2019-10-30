import pygame

class vacuum:
    def __init__(self, room, window):
        self.img = pygame.image.load("vacuum.png")
        self.room = room
        self.window = window

    def set_position(self, row, col):
        old = self.room.vacuum_position()
        old_col = old[1]
        old_row = old[0]
        cell_size = self.room.get_cell_size()
        self.room.set_vacuum(row, col)
        left = int((col*cell_size)+2)
        top = int((row*cell_size)+2)
        pygame.draw.rect(self.window, (0,0,0),((old_col*cell_size)+1, (old_row*cell_size)+1, cell_size-2, cell_size-2), False)
        self.window.blit(self.img, (left, top))
        print(self.room.vacuum_position())
        pygame.display.update()

    def move_up(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_up_border() and row > 0):
            self.set_position(row-1, col)
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def move_down(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_down_border() and row < self.room.get_rows()-1):
            self.set_position(row+1, col)
        else:
            raise Exception("Invalid move! Cannot move down from current position.")

    def move_right(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_right_border() and col < self.room.get_cols()-1):
            self.set_position(row, col+1)
        else:
            raise Exception("Invalid move! Cannot move right from current position.")

    def move_left(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_left_border() and col > 0):
            self.set_position(row, col-1)
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def clean(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(grid[row][col].has_dirt()):
            self.room.clean_tile(row, col)
            self.set_position(row, col)
        else:
            pass
