
from dij import Graph
from dij import dijkstra
from dij import shortest

import copy

class solver:


    def __init__(self, grid):
        
        self.actualMovedPath = []

        self.trueGrid = grid
        
        self.exploredGrid = [ [False]*len(grid[0]) for _ in range(0,len(grid)) ]
        self.exploredGridActual = [ [None]*len(grid[0]) for _ in range(0,len(grid)) ]


        for row in range(0,len(grid)):
            for col in range(0,len(grid[0])):

                self.exploredGridActual[row][col] = copy.deepcopy( grid[row][col] )

                if ( not self.exploredGrid[row][col] ):
                    self.exploredGridActual[row][col].set_borders(False, False, False, False)
                    self.exploredGridActual[row][col].set_vacuum()
                    self.exploredGridActual[row][col].clean()
                    self.exploredGridActual[row][col].remove_vacuum()

                    if(row == 0):
                        self.exploredGridActual[row][col].set_up_border()
                    if(col == 0):
                        self.exploredGridActual[row][col].set_left_border()
                    if(row == len(grid)-1):
                        self.exploredGridActual[row][col].set_down_border()
                    if(col == len(grid[0])-1):
                        self.exploredGridActual[row][col].set_right_border()                    
                    

    def isMapExplored(self):
        for row in range(0,len(self.exploredGrid)):
            for col in range(0,len(self.exploredGrid[0])):
                if( not self.exploredGrid[row][col] ):
                    return False
                
        return True
    
    def discoverMapIter(self,currPos):
        
    
        if(not self.isMapExplored() ):

            currentGraph = self.transformGridToGraph(self.getExploredGrid())
            
            destPos = self.getUnexploredTile()
           
            pathDir = self.getPathDirections(self.getExploredGrid()
            ,currentGraph,currPos[0],currPos[1],destPos[0],destPos[1])
            
            newCurrPos = self.exploreByPath(self.trueGrid,currPos[0],currPos[1],pathDir)
            
            
            #for m in range(0,len(data1)):
            #    for n in range (len(data1[0])):
            #        if( not data1[m][n].get_data_string() == data2[m][n].get_data_string()):
            #            print(data1[m][n].get_data_string())
            #            print(data2[m][n].get_data_string())

            return newCurrPos
            
        return [-1,-1]

    #
    # add discovered something new since last path as a variable as to not update graph needlessly
    #
    #
    
    def getUnexploredTile(self):
        for row in range(0,len(self.exploredGrid)):
            for col in range(0,len(self.exploredGrid[0])):
                if( not self.exploredGrid[row][col] ):
                    return [row,col]
                
        return None    
    
    def getExploredGrid(self):
        return self.exploredGridActual

    def addExploredToGrid(self,grid,row,col):
        self.exploredGrid[row][col] = True
        self.exploredGridActual[row][col] = copy.deepcopy( grid[row][col] )
        
        if( grid[row][col].has_right_border() and col+1 < len(grid[0]) ):
            self.exploredGridActual[row][col+1].set_left_border()
        if( grid[row][col].has_left_border() and col-1 >= 0 ):
            self.exploredGridActual[row][col-1].set_right_border()
        if( grid[row][col].has_up_border() and row-1 >= 0 ):
            self.exploredGridActual[row-1][col].set_down_border()
        if( grid[row][col].has_down_border() and row+1 < len(grid) ):
            self.exploredGridActual[row+1][col].set_up_border()
                
        
        
    def exploreByPath(self,grid,srcRow,srcCol,path):

        currentPos = [srcRow, srcCol]
        
        self.actualMovedPath = []

        self.addExploredToGrid(grid,currentPos[0] , currentPos[1])
        
        for  idx in range(0,len(path)) :
            if(path[idx] == 'U'):
                if( grid[currentPos[0]][currentPos[1]].has_up_border() ):
                    #the end
                    print("path hit U")
                    return currentPos
                else:
                    currentPos = [currentPos[0] -1, currentPos[1]]
                    self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    self.actualMovedPath.append( copy.deepcopy( path[idx] ) )

            elif(path[idx] == 'R'):
                if( grid[currentPos[0]][currentPos[1]].has_right_border() ):
                    #the end
                    print("path hit R")
                    return currentPos
                else:
                    currentPos = [currentPos[0], currentPos[1] + 1]
                    self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    self.actualMovedPath.append( copy.deepcopy( path[idx] ) )
                    
            elif(path[idx] == 'L'):
                if( grid[currentPos[0]][currentPos[1]].has_left_border() ):
                    #the end
                    print("path hit L")
                    return currentPos
                else:
                    currentPos = [currentPos[0], currentPos[1] - 1]
                    self.addExploredToGrid(grid,currentPos[0] , currentPos[1])


                    self.actualMovedPath.append( copy.deepcopy( path[idx] ) )

            elif(path[idx] == 'D'):
                if( grid[currentPos[0]][currentPos[1]].has_down_border() ):
                    #the end
                    print("path hit D")
                    return currentPos
                else:
                    currentPos = [currentPos[0] +1, currentPos[1]]
                    self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    self.actualMovedPath.append( copy.deepcopy( path[idx] ) )
        
        

        return currentPos
            

    def getLastActualUsedPath(self):

        return self.actualMovedPath

    @staticmethod
    def transformGridToGraph(grid):
    
        g = Graph()
        
        #print (g.get_vertices() )
            
        for row in range(0,len(grid)):
            for col in range(0, len(grid[0]) ):  
                g.add_vertex(grid[row][col].get_string_id())
                
        for y in range(0,len(grid)):
            for x in range(0,len(grid[0])):  
                
                if(not grid[y][x].has_up_border() ):
                    g.add_edge(grid[y][x].get_string_id(), grid[y-1][x].get_string_id(), 1)     
        
                if(not grid[y][x].has_down_border()):
                    g.add_edge(grid[y][x].get_string_id(), grid[y+1][x].get_string_id(), 1)     
                    
                if(not grid[y][x].has_left_border() ):
                    g.add_edge(grid[y][x].get_string_id(), grid[y][x-1].get_string_id(), 1)     
                
                if(not grid[y][x].has_right_border()  ):
                    g.add_edge(grid[y][x].get_string_id(), grid[y][x+1].get_string_id(), 1)     
    
        return g
    
        #print ('Graph data:')
        #for v in g:
        #    for w in v.get_connections():
        #        vid = v.get_id()
        #        wid = w.get_id()
        #        print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    
    @staticmethod
    def getPathDirections(grid,g,y1,x1,y2,x2):
    
        dijkstra(g, g.get_vertex(grid[y1][x1].get_string_id()), g.get_vertex(grid[y2][x2].get_string_id())) 
    
        target = g.get_vertex(grid[y2][x2].get_string_id())
        path = [target.get_id()]
        shortest(target, path)
    
        pathSrcToDest = path[::-1]
        
        drctPath = []
        

        for index, obj in enumerate(pathSrcToDest):
            if index > 0:
                if (obj[1] > pathSrcToDest[index -1][1] ):
                    drctPath.append("D")
                elif (obj[1] < pathSrcToDest[index -1][1] ):
                    drctPath.append("U")
                elif (obj[3] < pathSrcToDest[index -1][3] ):
                    drctPath.append("L")
                elif (obj[3] > pathSrcToDest[index -1][3] ):
                    drctPath.append("R")     
        
        
        #print (pathSrcToDest)
        
        return drctPath
                

  