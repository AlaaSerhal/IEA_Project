import pygame
import random
from tile import tile

from dij import Graph
from dij import dijkstra
from dij import shortest



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
        self.grid[self.vacuum[0]][self.vacuum[1]].set_vacuum()

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
                
                if(y-1 >= 0):
                    self.grid[y-1][x].set_down_border()
                
                pygame.draw.line(self.window, (255,0,0), (x*self.cell_size,y*self.cell_size),((x+1)*self.cell_size, y*self.cell_size))
            elif(dir == 1):  # down border
                self.grid[y][x].set_down_border()
                
                if(y+1 < self.rows):
                    self.grid[y+1][x].set_up_border()                
                
                pygame.draw.line(self.window, (255,0,0),(x*self.cell_size,(y+1)*self.cell_size), ((x+1)*self.cell_size,(y+1)*self.cell_size))
            elif(dir == 2):  # left border
                self.grid[y][x].set_left_border()
                
                if(x-1 >= 0):
                    self.grid[y][x-1].set_right_border()                
                
                pygame.draw.line(self.window, (255,0,0),(x*self.cell_size, y*self.cell_size), (x*self.cell_size, (y+1)*self.cell_size))
            elif(dir == 3):  # right border
                self.grid[y][x].set_right_border()
                
                if(x+1 < self.cols):
                    self.grid[y][x+1].set_left_border()                
                
                pygame.draw.line(self.window, (255,0,0),((x+1)*self.cell_size, y*self.cell_size), ((x+1)*self.cell_size, (y+1)*self.cell_size))
            else:
                pass

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

    def vacuum_position(self):
        return self.vacuum

    def clean_tile(self, row, col):
        self.grid[row][col].clean()

    def set_vacuum(self, row, col):
        self.grid[self.vacuum[0]][self.vacuum[1]].remove_vacuum()
        self.vacuum = [row, col]
        self.grid[self.vacuum[0]][self.vacuum[1]].set_vacuum()
        
        
        #UNDER CONSTRUCTION
    def add_nodes(self):
        
        grid2 = []
        
        for y in range(0,self.rows):
            
            grid2.append([])
            
            for x in range(0,self.cols):
                
                grid2[y].append(None)
                   
                
                #if(x == 0 and y == 0):
                #    grid2[y][x] = self.grid[x][y]
                #    continue
                
                #path path path
                if( not self.grid[x][y].has_left_border() and not self.grid[x][y].has_right_border() ):
                    #if has bottom or top path add node
                    if(self.grid[x][y].has_down_border() or self.grid[x][y].has_up_border() ):
                        grid2[y][x] = self.grid[x][y]
                        
                #path path wall
                if( not self.grid[x][y].has_left_border() and self.grid[x][y].has_right_border() ):
                    grid2[y][x] = self.grid[x][y]
                    
                #wall path wall
                if(  self.grid[x][y].has_left_border() and self.grid[x][y].has_right_border() ):
                    grid2[y][x] = self.grid[x][y]
                    
                #wall path path
                if(  self.grid[x][y].has_left_border() and not self.grid[x][y].has_right_border() ):
                    grid2[y][x] = self.grid[x][y]
                    
                    
                    
         

        for x in range(0,self.cols):
            for y in range(0,self.rows): 
                print( str(x) + ' ' + str(y))
                print(grid2[y][x] is None)
    
    
    def transformGridToGraph(self):

        g = Graph()
        
        print(self.rows)
            
        for row in range(0,self.rows):
            for col in range(0,self.cols):  
                g.add_vertex(self.grid[row][col].get_string_id())
                
        for y in range(0,self.rows):
            for x in range(0,self.cols):  
                
                if(not self.grid[y][x].has_up_border() ):
                    g.add_edge(self.grid[y][x].get_string_id(), self.grid[y-1][x].get_string_id(), 1)     
        
                if(not self.grid[y][x].has_down_border()):
                    g.add_edge(self.grid[y][x].get_string_id(), self.grid[y+1][x].get_string_id(), 1)     
                    
                if(not self.grid[y][x].has_left_border() ):
                    g.add_edge(self.grid[y][x].get_string_id(), self.grid[y][x-1].get_string_id(), 1)     
                
                if(not self.grid[y][x].has_right_border()  ):
                    g.add_edge(self.grid[y][x].get_string_id(), self.grid[y][x+1].get_string_id(), 1)     
 
    
        #print ('Graph data:')
        #for v in g:
        #    for w in v.get_connections():
        #        vid = v.get_id()
        #        wid = w.get_id()
        #        print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    
    
    def getRawPath(self):

        dijkstra(g, g.get_vertex(self.grid[0][0].get_string_id()), g.get_vertex(self.grid[4][4].get_string_id())) 
    
        target = g.get_vertex(self.grid[4][4].get_string_id())
        path = [target.get_id()]
        shortest(target, path)
        print ('The shortest path : %s', (path[::-1]))     
        
        