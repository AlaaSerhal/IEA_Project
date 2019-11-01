
from dij import Graph
from dij import dijkstra
from dij import shortest

class solver:

    def transformGridToGraph(grid):
    
        g = Graph()
        
            
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
    
    
    def getPathDirections(grid,g,y1,x1,y2,x2):
    
        dijkstra(g, g.get_vertex(grid[y1][x1].get_string_id()), g.get_vertex(grid[y2][x2].get_string_id())) 
    
        target = g.get_vertex(grid[y2][x2].get_string_id())
        path = [target.get_id()]
        shortest(target, path)
    
        pathSrcToDest = path[::-1]
        
        drctPath = []
        
        previous = next_ = None
        l = len(pathSrcToDest)
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
        
        
        print (pathSrcToDest)
        
        return drctPath
                

  