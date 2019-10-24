import pygame
import random
from tile import tile
class room:
    def __init__(self, cell_size, rows, cols, window):
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.window = window
        self.vacuum = [rows//2, cols//2]
        self.grid = []
        for row in range(rows):
            self.grid.append([])
            for col in range(cols):
                self.grid[row].append(tile(row, col))
                if(row == 0):
                    self.grid[row][col].set_up_border()
                if(col == 0):
                    self.grid[row][col].set_left_border()
                if(row == rows-1):
                    self.grid[row][col].set_down_border()
                if(col == cols-1):
                    self.grid[row][col].set_right_border()
        self.grid[self.vacuum[0], self.vacuum[1]].set_vacuum()

    def draw_grid(self):
        x = 0
        y = 0
        for row in range(self.rows):
            if(row != 0):
                pygame.draw.line(self.window, (255,255,255), (0,y),(self.cols * self.cell_size,y))
            y = y + self.cell_size

        for col in range(self.cols):
            if(col != 0):
                pygame.draw.line(self.window, (255,255,255), (x,0),(x,self.rows *self.cell_size))
            x = x + self.cell_size
        pygame.draw.line(self.window, (255,0,0), (0,0), (self.cols*self.cell_size, 0))
        pygame.draw.line(self.window, (255,0,0), (0,0), (0, self.rows*self.cell_size))
        pygame.draw.line(self.window, (255,0,0), (self.cols*self.cell_size-1,0), (self.cols*self.cell_size-1, self.rows*self.cell_size))
        pygame.draw.line(self.window, (255,0,0), (0,self.rows*self.cell_size-1), (self.cols*self.cell_size, self.rows*self.cell_size-1))

    def draw_borders(self):
        number = random.randint(0, min(self.rows, self.cols)-1)
        for i in range(number):
            x = random.randint(0, self.cols-1)
            y = random.randint(0, self.rows-1)
            dir = random.randint(0,3)

            if(dir == 0):  # up border
                self.grid[y][x].set_up_border()
                pygame.draw.line(self.window, (255,0,0), (x*self.cell_size,y*self.cell_size),((x+1)*self.cell_size, y*self.cell_size))
            elif(dir == 1):  # down border
                self.grid[y][x].set_down_border()
                pygame.draw.line(self.window, (255,0,0),(x*self.cell_size,(y+1)*self.cell_size), ((x+1)*self.cell_size,(y+1)*self.cell_size))
            elif(dir == 2):  # left border
                self.grid[y][x].set_left_border()
                pygame.draw.line(self.window, (255,0,0),(x*self.cell_size, y*self.cell_size), (x*self.cell_size, (y+1)*self.cell_size))
            elif(dir == 3):  # right border
                self.grid[y][x].set_right_border()
                pygame.draw.line(self.window, (255,0,0),((x+1)*self.cell_size, y*self.cell_size), ((x+1)*self.cell_size, (y+1)*self.cell_size))
            else:
                pass

    def get_window(self):
        return self.window

    def get_cell_size(self):
        return self.cell_size

    def get_array(self):
        return self.grid

    def vacuum_position(self):
        return self.vacuum

    def set_vacuum(self, row, col):
        self.grid[self.vacuum[0], self.vacuum[1]].remove_vacuum()
        self.vacuum = [row, col]
        self.grid[self.vacuum[0], self.vacuum[1]].set_vacuum()
