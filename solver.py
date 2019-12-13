
from dij import Graph
from dij import dijkstra
from dij import shortest

import pygame as pygame

import copy
import random

from GA import GA

class solver:


    def __init__(self, grid):
        
        self.gntcAlgrth = GA(5)
        self.tempPool = []

        self.actualMovedPath = []

        lastGraph = None

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
    
    #add GA////////////////////

    def getNextDirt(self,currPos):

        dictionaryDistancePath = {}

        for row in range(0,len(self.exploredGridActual)):
            for col in range(0,len(self.exploredGridActual[0])):
                if(  self.exploredGridActual[row][col].has_dirt() ):
                    if(not ( currPos[0] == row and  currPos[1] == col)  ):
                        dictionaryDistancePath[ self.calculateDistanceLowCost( [row,col],currPos ) ] = [row,col]
                        #return [row,col]
        
        for key in sorted(dictionaryDistancePath):
            return dictionaryDistancePath[key]

        return [-1,-1]

    
    def calculateDistanceLowCost(self,pos1, pos2):
        if(pos1[0] == pos2[0]):
            dist = abs(pos1[1] - pos2[1])
        elif(pos1[1] == pos2[1]):
            dist = abs(pos1[0] - pos2[0])
        else:
            delta_r = abs(pos1[0] - pos2[0])
            delta_c = abs(pos1[1] - pos2[1])
            dist = delta_r + delta_c
        return dist

    def getTilePathForDirtExploration(self):

        rowCol = []
        
        if( not self.gntcAlgrth.hasPoolInit()):
            self.tempPool = self.gntcAlgrth.createRandomInitPool(len(self.exploredGrid) , len(self.exploredGrid[0]) )
        else:

            if(random.random() < 0.3):
                rowCol = self.gntcAlgrth.getUnscoredORlowScored()
                return [rowCol[0],rowCol[1]]
            else:
                self.gntcAlgrth.updatePool( self.gntcAlgrth.selectForPopulationPool(5) )
                if(  len(self.tempPool) == 0):
                    self.tempPool =  self.gntcAlgrth.getPool()
            

        if( len(self.tempPool) > 0 ):
            rowCol = self.tempPool.pop()
            return [rowCol[0],rowCol[1]]

        #col = random.randint(0, len(self.exploredGridActual[0])-1)
        #row = random.randint(0, len(self.exploredGridActual)-1)
        #print("can't reach here")
        #exit()

        return [rowCol[0],rowCol[1]]

    #///////////////////////////////////

    def dirtPathIterator(self,currPos):
        
        #if there is dirt previously explored g to it
        #else go to random place to discover dirt
        
        #print( "Dest to go to for dirt" )
        #print ( self.getNextDirt(currPos) )

        if( not self.getNextDirt(currPos)[0] == -1 ):

            currentGraph = copy.deepcopy (self.getLastGraph() )
            #currentGraph = self.transformGridToGraph(self.getExploredGrid())
            

            destPos = self.getNextDirt(currPos)
           
            pathDir = self.getPathDirections(self.getExploredGrid()
            ,currentGraph,currPos[0],currPos[1],destPos[0],destPos[1])
            
            #print("path dir")
            #print(pathDir)

            newCurrPos = self.exploreByPath(self.trueGrid,currPos[0],currPos[1],pathDir)
            
            #print("new pos")
            #print(newCurrPos)

            return newCurrPos
            

        else:

            #print(currPos)

            
            currentGraph = copy.deepcopy (self.getLastGraph() )

            #currentGraph = self.transformGridToGraph(grid)
            
            destPos = self.getTilePathForDirtExploration()

            pathDir = self.getPathDirections(self.getExploredGrid()
            ,currentGraph,currPos[0],currPos[1],destPos[0],destPos[1])
            
           
            #pathDir = self.getPathDirections(grid
            #,currentGraph,myPos[0],myPos[1],destPos[0],destPos[1])

            #print(pathDir)

            newCurrPos = self.exploreByPath(self.trueGrid,currPos[0],currPos[1],pathDir)
            
            if( not (destPos[0] == newCurrPos[0] and destPos[1] == newCurrPos[1]) ):
                print("path finder is faulty")
                print(destPos)
                print(newCurrPos)
                
                #while(True):
                #    _ = 1

                exit()

            return destPos

    def addDirtPathIterator(self,currPos):
        
        #where should i add dirt

        currentGraph = copy.deepcopy (self.getLastGraph() )
        #currentGraph = self.transformGridToGraph(self.getExploredGrid())
        

        destPos = self.getRandomTile()
        
        pathDir = self.getPathDirections(self.getExploredGrid()
        ,currentGraph,currPos[0],currPos[1],destPos[0],destPos[1])
        

        newCurrPos = self.exploreByPath(self.trueGrid,currPos[0],currPos[1],pathDir)
        

        return newCurrPos
        



    def expoloreAllBorders(self):

        self.exploredGridActual = [ [None]*len(self.trueGrid[0]) for _ in range(0,len(self.trueGrid)) ]


        for row in range(0,len(self.trueGrid)):
            for col in range(0,len(self.trueGrid[0])):

                self.exploredGridActual[row][col] = copy.deepcopy( self.trueGrid[row][col] )

                if ( not self.exploredGrid[row][col] ):
                    self.exploredGridActual[row][col].set_vacuum()
                    self.exploredGridActual[row][col].clean()
                    self.exploredGridActual[row][col].remove_vacuum()

        self.transformGridToGraph( copy.deepcopy( self.getExploredGrid()) )

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


    #If you get stuck you need to acknowledge the machine as a barrier

    def escapeFromAgent(self,currPos, machinePos):
        
        #print("remove me")
        #exit(0)

        #where to add fake barrier?
        #add around whole tile just to be sure
        #see if that causes any issue

        pathDir = []

        fakeGrid = copy.deepcopy(self.trueGrid)
        
        print(machinePos)

        fakeGrid[machinePos[0]][machinePos[1]].set_borders(True,True,True,True)

        counter = 1

        while(pathDir == []):

            counter += 1
            if(counter > 12):
                print("can't run away")
                exit(0)

            currentGraph = self.transformGridToGraph( copy.deepcopy(fakeGrid), False )
            
            destPos = self.getRandomTile()
            
            pathDir = self.getPathDirections(self.getExploredGrid()
            ,currentGraph,currPos[0],currPos[1],destPos[0],destPos[1])
            
            newCurrPos = self.exploreByPath(self.trueGrid,currPos[0],currPos[1],pathDir)

        return newCurrPos
       


    #
    # add discovered something new since last path as a variable as to not update graph needlessly
    #
    #
    #len(self.exploredGrid[0])
    def getUnexploredTile(self):
        for row in range(0,len(self.exploredGrid)):
            cols = len(self.exploredGrid[0])
            for col in range(0,cols):
                
                if(row % 2 == 0):
                    if( not self.exploredGrid[row][col] ):
                        return [row,col]
                else:
                    if( not self.exploredGrid[row][cols - col - 1] ):
                        #print(cols - col - 1)
                        return [row, int (cols - col - 1) ]

                
                
        return None    

    def getRandomTile(self):
        
        row = random.randint(0, len(self.trueGrid) - 1)
        col = random.randint(0, len(self.trueGrid[0]) - 1)
                
        return [row,col]    
    
    def getExploredGrid(self):
        
        #print("getExplored()")

        return self.exploredGridActual

    def addExploredToGrid(self,grid,row,col):

        #print("explored " + str(row) + " - " + str(col) )

        self.exploredGrid[row][col] = True
        self.exploredGridActual[row][col] = copy.deepcopy( grid[row][col] )
        
        self.exploredGridActual[row][col].set_dirty(grid[row][col].has_dirt()) 

        if(  col+1 < len(grid[0]) ):
            self.exploredGridActual[row][col+1].set_dirty(grid[row][col+1].has_dirt()) 
        if(  col-1 >= 0 ):
            self.exploredGridActual[row][col-1].set_dirty(grid[row][col-1].has_dirt()) 
        if( row-1 >= 0 ):
            self.exploredGridActual[row-1][col].set_dirty(grid[row-1][col].has_dirt()) 
        if( row+1 < len(grid) ):
            self.exploredGridActual[row+1][col].set_dirty(grid[row+1][col].has_dirt()) 
                

        if( grid[row][col].has_right_border() and col+1 < len(grid[0]) ):
            self.exploredGridActual[row][col+1].set_left_border()
        if( grid[row][col].has_left_border() and col-1 >= 0 ):
            self.exploredGridActual[row][col-1].set_right_border()
        if( grid[row][col].has_up_border() and row-1 >= 0 ):
            self.exploredGridActual[row-1][col].set_down_border()
        if( grid[row][col].has_down_border() and row+1 < len(grid) ):
            self.exploredGridActual[row+1][col].set_up_border()
                
    #def addTileToExplored(self):

        
        
    def exploreByPath(self,grid,srcRow,srcCol,path, savePath = True):

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
                    #self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    if(savePath):
                        self.actualMovedPath.append( copy.deepcopy( path[idx] ) )

                    if( self.gntcAlgrth.hasPoolInit()):
                        self.gntcAlgrth.updateMatrixData(currentPos[0] , currentPos[1], grid[currentPos[0]][currentPos[1]].has_dirt() )

            elif(path[idx] == 'R'):
                if( grid[currentPos[0]][currentPos[1]].has_right_border() ):
                    #the end
                    print("path hit R")
                    return currentPos
                else:
                    currentPos = [currentPos[0], currentPos[1] + 1]
                    #self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    if(savePath):
                        self.actualMovedPath.append( copy.deepcopy( path[idx] ) )

                    if( self.gntcAlgrth.hasPoolInit()):
                        self.gntcAlgrth.updateMatrixData(currentPos[0] , currentPos[1], grid[currentPos[0]][currentPos[1]].has_dirt() )

                    
            elif(path[idx] == 'L'):
                if( grid[currentPos[0]][currentPos[1]].has_left_border() ):
                    #the end
                    print("path hit L")
                    return currentPos
                else:
                    currentPos = [currentPos[0], currentPos[1] - 1]
                    #self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    if(savePath):
                        self.actualMovedPath.append( copy.deepcopy( path[idx] ) )


                    if( self.gntcAlgrth.hasPoolInit()):
                        self.gntcAlgrth.updateMatrixData(currentPos[0] , currentPos[1], grid[currentPos[0]][currentPos[1]].has_dirt() )


            elif(path[idx] == 'D'):
                if( grid[currentPos[0]][currentPos[1]].has_down_border() ):
                    #the end
                    print("path hit D")
                    return currentPos
                else:
                    currentPos = [currentPos[0] +1, currentPos[1]]
                    #self.addExploredToGrid(grid,currentPos[0] , currentPos[1])

                    if(savePath):
                        self.actualMovedPath.append( copy.deepcopy( path[idx] ) )

                    if( self.gntcAlgrth.hasPoolInit()):
                        self.gntcAlgrth.updateMatrixData(currentPos[0] , currentPos[1], grid[currentPos[0]][currentPos[1]].has_dirt() )

        
        

        return currentPos
            

    def getLastActualUsedPath(self):

        return self.actualMovedPath

    def getLastGraph(self):

        return self.lastGraph

    def transformGridToGraph(self,grid, saveGraph = True):
    
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
    
        if(saveGraph):
            self.lastGraph = copy.deepcopy (g)

        #print ('Graph data:')
        #for v in g:
        #    for w in v.get_connections():
        #        vid = v.get_id()
        #        wid = w.get_id()
        #        print ('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))
    

        return g
    
      
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

                obj = obj[1:]
                pathSrcToDest[index-1] = pathSrcToDest[index-1][1:]                

                rowCurr = int(obj.split("x")[0] )
                colCurr = int(obj.split("x")[1] )
                rowPrev = int(pathSrcToDest[index -1].split("x")[0] )
                colPrev = int(pathSrcToDest[index -1].split("x")[1] )

                if (rowCurr > rowPrev ):
                    drctPath.append("D")
                elif (rowCurr < rowPrev ):
                    drctPath.append("U")
                elif (colCurr < colPrev ):
                    drctPath.append("L")
                elif (colCurr > colPrev ):
                    drctPath.append("R")     
        
        
        #print (pathSrcToDest)
        
        return drctPath
                

  