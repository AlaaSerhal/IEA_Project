
from GA import GA

class GASolver:
    
    def __init__(self):
        pass

    def worker(self):

        ga = GA(5)

        initPool = ga.createRandomInitPool(5,5)

        for pos in initPool:
            
            #explore it then !!!!
            
            ga.updateMatrixData(pos[0],pos[1],True)
huvyc
        ga.obtainFitnessFromData()

        #explore something outside pool low or no
        for _ in range(3):
            row_col = ga.getUnscoredORlowScored()

            #explore tile then !!!!

            ga.updateMatrixData(row_col[0],row_col[1],True)


        ga.obtainFitnessFromData()

        ga.updatePool( ga.selectForPopulationPool(5) )


        for pos in ga.getPool():

            #explore it then !!!!
            
            ga.updateMatrixData(pos[0],pos[1],True)