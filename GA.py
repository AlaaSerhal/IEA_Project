from dij import Graph
from dij import dijkstra
from dij import shortest

import copy
import random


class GA:

    def __init__(self,poolSize):
            
        self.pop = []

        self.hasPool = False

        self.matrixFitness = []
        self.matrixData = []

        self.poolSize = poolSize

        self.tempPopX = []
        self.tempPopY = []

    #def initPop(self,population):
        
    #    self.pop = population

    def hasPoolInit(self):

        return self.hasPool

    def createRandomInitPool(self,rows,cols):
    
        self.hasPool = True

        self.matrixFitness =  [ [-1]*cols for _ in range(0,rows) ]
        self.matrixData = [ [0,0]*len(cols) for _ in range(0,rows) ]


        row = random.randint(0,rows-1)
        col = random.randint(0,rows-1)

        while ( self.tempPopX.count(col) > 0 or self.tempPopY.count(row) > 0) :
            row = random.randint(0,rows-1)
            col = random.randint(0,rows-1)                  

        self.tempPopX.append( col )
        self.tempPopY.append( row )

        self.pop.append( [row,col] )

        return self.pop
    
    def updateMatrixData(self,row,col, foundDirt):
        
        visits = self.matrixData[row][col][0] + 1
        dirtCount = self.matrixData[row][col][1]
        if(foundDirt):
            dirtCount += 1
        
        self.matrixData[row][col] = [visits,dirtCount]

        data = [visits,dirtCount]
            
        score = data[1] / data[0]
        if(data[0] == 0):
            score = -1
        
        self.matrixFitness[row][col] = score

    def getUnscoredORlowScored(self):
        
        candidateLoc = []

        for row in range(len(self.matrixFitness) ) :
            for col in range(len(self.matrixFitness[0]) ) :
                if(self.matrixFitness[row][col] == -1):
                    candidateLoc.append( [row,col] )
        
        if( len(candidateLoc) == 0 ):
            dictionary = {}

            for row in range(len(self.matrixFitness) ) :
                for col in range(len(self.matrixFitness[0]) ) :
                    dictionary[self.matrixFitness[row][col]] = [row,col] 

            indx = 0

            for i in sorted (dictionary).reverse() : 
                print ((i, dictionary[i]), end =" ") 
                if(indx > 4):
                    break
                else:
                    indx+= 1
                    candidateLoc.append(dictionary[i])
                    
        return candidateLoc[ random.randint(0, len(candidateLoc) ) ]

    def obtainFitnessFromDataREMOVED(self):

        for poolItem in self.pop:
            
            data = self.matrixData[poolItem[0]][poolItem[1]]
            
            score = data[1] / data[0]
            if(data[0] == 0):
                score = -1
            
            self.matrixFitness[poolItem[0]][poolItem[1]] = score

    def selectForPopulationPool(self,maxSelection = 5):

        dictionary = {}

        for row in range(len(self.matrixFitness) ) :
            for col in range(len(self.matrixFitness[0]) ) :
                dictionary[self.matrixFitness[row][col]] = [row,col] 

        indx = 0
        selected = []

        for i in sorted (dictionary).reverse() : 
            print ((i, dictionary[i]), end =" ") 
            if(indx > maxSelection):
                break
            else:
                indx+= 1
                selected.append(dictionary[i])
                
        return selected

    def updatePool(self,newPop):

        self.pop = newPop

    def getPool(self):
        return self.pop

