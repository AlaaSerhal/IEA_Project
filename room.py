import pygame as pygame
import random
from tile import tile
import globals

class room:
    def __init__(self, cell_size, rows, cols, window):
        self.dirt_list = []
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.window = window
        self.dirt_machine = []
        self.vacuum = []
        self.grid = []
        self.dirt_img = pygame.image.load("dirt.png")
        for row in range(rows):  # create array
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
        for x in range(globals.globals.cleaning_agents):
            set = False
            self.vacuum.append([])
            while(not set):
                row = random.randint(0, rows -1)
                col = random.randint(0, cols -1)
                if(not self.grid[row][col].is_occupied()):
                    self.grid[row][col].set_vacuum()
                    self.vacuum[x].extend([row, col])
                    set = True
                else:
                    pass
        for x in range(globals.globals.dirt_agents):
            set = False
            self.dirt_machine.append([])
            while(not set):
                row = random.randint(0, rows -1)
                col = random.randint(0, cols -1)
                if(not self.grid[row][col].is_occupied()):
                    self.grid[row][col].set_dirt_machine()
                    self.dirt_machine[x].extend([row, col])
                    set = True
                else:
                    pass
        print(self.vacuum)
        print(self.dirt_machine)

    def draw_grid(self):  # draw grid and outside borders
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

    def draw_borders(self, number=None):  # generate and draw borders randomly (in red)
            if(number == None):  # if user does not specify number of borders
                number = random.randint(0, min(self.rows, self.cols)+5)
            else:
                pass
            print("number of borders: ", number)
            i = 0
            while(i < number):
                # coordinates
                x = random.randint(0, self.cols-1)
                y = random.randint(0, self.rows-1)
                # border on cell, up, down, left, right
                dir = random.randint(0,3)

                if(dir == 0 and not self.grid[y][x].has_up_border()):  # up border
                    self.grid[y][x].set_up_border()

                    if(y-1 >= 0):
                        self.grid[y-1][x].set_down_border()

                    pygame.draw.line(self.window, (255,0,0), (x*self.cell_size,y*self.cell_size),((x+1)*self.cell_size, y*self.cell_size))
                    i += 1
                elif(dir == 1 and not self.grid[y][x].has_down_border()):  # down border
                    self.grid[y][x].set_down_border()

                    if(y+1 < self.rows):
                        self.grid[y+1][x].set_up_border()

                    pygame.draw.line(self.window, (255,0,0),(x*self.cell_size,(y+1)*self.cell_size), ((x+1)*self.cell_size,(y+1)*self.cell_size))
                    i += 1
                elif(dir == 2 and not self.grid[y][x].has_left_border()):  # left border
                    self.grid[y][x].set_left_border()

                    if(x-1 >= 0):
                        self.grid[y][x-1].set_right_border()

                    pygame.draw.line(self.window, (255,0,0),(x*self.cell_size, y*self.cell_size), (x*self.cell_size, (y+1)*self.cell_size))
                    i += 1
                elif(dir == 3 and not self.grid[y][x].has_right_border()):  # right border
                    self.grid[y][x].set_right_border()

                    if(x+1 < self.cols):
                        self.grid[y][x+1].set_left_border()

                    pygame.draw.line(self.window, (255,0,0),((x+1)*self.cell_size, y*self.cell_size), ((x+1)*self.cell_size, (y+1)*self.cell_size))
                    i += 1
                else:
                    pass

    def set_dirt(self, row, col):  # set dirt at position
        self.grid[row][col].dirty()
        cell_size = self.cell_size
        left = int((col*cell_size)+2)
        top = int((row*cell_size)+2)
        self.window.blit(self.dirt_img, (left, top))
        element = [row, col]
        if(element not in self.dirt_list):
            self.dirt_list.append(element)
        pygame.display.update()

    def get_window(self):
        return self.window

    def get_cell_size(self):
        return self.cell_size

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def get_array(self):
        return self.grid

    def dirt_machine_position(self, id):
        return self.dirt_machine[id]

    def vacuum_position(self, id):
        return self.vacuum[id]

    def get_dirt_machine_tile(self,id):
        return self.grid[self.dirt_machine[id][0]][self.dirt_machine[id][1]]

    def get_vacuum_tile(self, id):
        return self.grid[self.vacuum[id][0]][self.vacuum[id][1]]

    def get_dirt_list(self):
        return self.dirt_list

    def clean_tile(self, row, col):
        element = [row, col]
        if(element in self.dirt_list):
            self.dirt_list.remove(element)
        self.grid[row][col].clean()

    def set_dirt_machine(self, id, row, col):
        self.grid[self.dirt_machine[id][0]][self.dirt_machine[id][1]].remove_dirt_machine()
        self.dirt_machine[id] = [row, col]
        self.grid[self.dirt_machine[id][0]][self.dirt_machine[id][1]].set_dirt_machine()

    def set_vacuum(self, id, row, col):  # sets vacuum in room
        self.grid[self.vacuum[id][0]][self.vacuum[id][1]].remove_vacuum()
        self.vacuum[id] = [row, col]
        self.grid[self.vacuum[id][0]][self.vacuum[id][1]].set_vacuum()

    def clear_room(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                self.grid[row][col].set_borders(False,False,False,False)
                self.grid[row][col].set_vacuum()
                self.grid[row][col].clean()
