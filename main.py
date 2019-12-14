import pygame as pygame
from vacuum import vacuum
import PySimpleGUI as sg
from room import room
from dirt import dirt
from dirt_machine import dirt_machine
from datetime import datetime
import globals

from solver import solver
import copy


def isVacuumInPos( room, vacuums, pos):

    index = -1
    for _ in vacuums:

        index += 1
        if room.vacuum_position(index)[0] == pos[0] and room.vacuum_position(index)[1] == pos[1]:
            return True
    return False

def isVacuumNeghbr(room,vacuums,pos, boxIn):
    index = -1

    if(not boxIn):
        return False

    for _ in vacuums:

        index += 1
        if room.vacuum_position(index)[0] == pos[0] - 1 and room.vacuum_position(index)[1] == pos[1]:
            return True
        if room.vacuum_position(index)[0] == pos[0] + 1 and room.vacuum_position(index)[1] == pos[1]:
            return True
        if room.vacuum_position(index)[0] == pos[0] and room.vacuum_position(index)[1] == pos[1] + 1:
            return True
        if room.vacuum_position(index)[0] == pos[0] and room.vacuum_position(index)[1] == pos[1] - 1:
            return True

    return False


def main():
    game_over = False
    game__over=False
    rows, cols = 15, 15
    borders = 0
    dirty_tiles=0
    while(rows >= 15 or cols >= 15 or rows==0 or cols==0 or borders==0 or dirty_tiles==0):
        try:

            layout = [  [sg.Text('Necessary Inputs')],
            [sg.Text('Please enter number of rows as an integer:'), sg.InputText()],
            [sg.Text('Please enter number of cols as an integer:'), sg.InputText()],
            [sg.Text('Please enter number of dirty tiles:'), sg.InputText()],
            [sg.Text('Please enter number of borders:'), sg.InputText()],
            [sg.Text('Speed:'),sg.Slider(range=(1000,30),default_value=1000,size=(20,15),orientation='horizontal', disable_number_display=True)],
            [sg.Text('Window dirt Period'),sg.Slider(range=(2,10),default_value=5,size=(20,15),orientation='horizontal', disable_number_display=True)],
            [sg.Text('Agent Period'),sg.Slider(range=(2,10),default_value=5,size=(20,15),orientation='horizontal', disable_number_display=True)],
            [sg.Spin([i for i in range(1,5)], initial_value=1), sg.Text('Cleaning Agents')],
            [sg.Spin([i for i in range(0,5)], initial_value=0), sg.Text('Dirt Agents')],
            [sg.Frame(layout=[
            [sg.Radio('Case1 (Fully observable map and once generated dirt):', "Case1", default=False)],
            [sg.Radio('Case2 (Fully observable map and continuously added dirt):', "Case1", default=False)],
            [sg.Radio('Case3 (Fully observable borders and unknown dirt positions):', "Case1", default=False)],
            [sg.Radio('Case4 (Unknown borders and dirt positions):', "Case1", default=False)],

            [sg.Checkbox('Alternate Dirt Algorithm',  default=False)],
            [sg.Checkbox('Box In',  default=False)]],

            title='Choose Any of these Cases',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
            [sg.Submit()]]
            window = sg.Window('Vacuum Cleaner Agent', layout)
            event, values = window.Read()
            case1=values[9]
            case2=values[10]
            case3=values[11]
            case4=values[12]
            
            intelligenceDirtFirst=values[13]

            boxIn = values[14]
            
            rows=int(values[0])
            cols=int(values[1])
            dirty_tiles= int(values[2])
            borders=int(values[3])
            globals.globals.speed=int(values[4])
            globals.globals.frequency=int(values[5])
            globals.globals.period=int(values[6])
            globals.globals.cleaning_agents=int(values[7])
            globals.globals.dirt_agents=int(values[8])
            if event in ('Submit'):
                print('Borders are placed randomly')
            window.Close()
        except ValueError:
            print("No valid integer! Please try again ...")
    CELL_SIZE = 40
    window_size = [cols * CELL_SIZE, rows * CELL_SIZE]


    pygame.init()

    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Vacuum Cleaner Agent")
    run = True
    clock = pygame.time.Clock()
    r = room(CELL_SIZE, rows, cols, window)
    r.draw_grid()
    r.draw_borders(borders)
    vacuums = []
    dirt_machines = []

    for x in range(globals.globals.cleaning_agents):
        vacuums.append(vacuum(r, window, x))
        print("creating vacuum with ID: ",  x)

    if(globals.globals.dirt_agents > 0):
        for x in range(globals.globals.dirt_agents):
            dirt_machines.append(dirt_machine(r, window, x))
            print("creating dirt machine with ID: ", x)
    else:
        pass
    # print(dirt_machines)
    d = dirt(r, window, dirty_tiles)

    pos = None
    mySolver = solver(r.get_array())

    tempLastLoc = None
    pos2 = None

    globals.globals.start_duration = datetime.now().timestamp()

    

# depending on the Specific case
    if(case1):  # fully observable with set amount of dirt
        while run:

            pygame.time.delay(globals.globals.speed)
            clock.tick(10)
            for event in pygame.event.get():

                #gameover
                if (event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (event.key == pygame.K_ESCAPE))):
                    globals.globals.end_duration= datetime.now().timestamp()
                    layout2 = [[sg.Text('Duration: ' + str(round(globals.globals.end_duration-globals.globals.start_duration,3)))],
                    [sg.Text('Number of cleaned tiles: '+ str(globals.globals.nb_clean_tiles))],
                    [sg.Text('Number of steps: '+ str(globals.globals.nb_steps))],
                    [sg.Text('Number of added dirt: '+ str(globals.globals.nb_added_dirt))],
                    [sg.Text('Average number of steps per dirt: '+ str(round(globals.globals.nb_steps/globals.globals.nb_clean_tiles)))],
                    [sg.Text('Average time to clean a dirt: ' + str(round(round(globals.globals.end_duration-globals.globals.start_duration,3)/globals.globals.nb_clean_tiles, 2)))],
                    [sg.Button('Exit')]]
                    window1 = sg.Window('Measures', layout2)
                    window1.Read()
                    game_over = True
                    r.clear_room()
                    window.fill((0,0,0))
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text_surface = font.render("Game Over", True, (150,150,150))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (window.get_width()//2, window.get_height()//2)
                    window.blit(text_surface, text_rect)
                    pygame.display.update()
                    vacuums[0].set_position((rows//2)+1,(cols//2)-1)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)
                    vacuums[0].move_left()
                    pygame.time.delay(500)
                    vacuums[0].move_right()
                    pygame.time.delay(500)
                    vacuums[0].move_right()
                    pygame.time.delay(500)
                    vacuums[0].move_right()

                    run = False
                    #arrows as input
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        v.move_left()
                    if event.key == pygame.K_RIGHT:
                        v.move_right()
                    if event.key == pygame.K_UP:
                        v.move_up()
                    if event.key == pygame.K_DOWN:
                        v.move_down()
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(5000)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if(not game_over):
                
                if(not intelligenceDirtFirst):
                    for x in vacuums:
                        x.move_to_closest_dirt()
                
                
                
                if(globals.globals.dirt_agents != 0):
                    if(intelligenceDirtFirst):
                       #Alternate Algrthm 
                        paths = mySolver.getFirstPathForDirt(r,dirt_machines,vacuums, boxIn)
                       
                        index = -1
                        if(not paths is None):
                            
                            m = len(paths[0])
                            for p in paths:
                                if(len(p) < m):
                                    m = len(p)
                            
                            for idx in range(0,m):
                                for pathX in paths:
                                    index += 1

                                    if( pathX is None or pathX == [] or len(pathX) == 0 or pathX[0] == None):
                                        continue

                                    if(idx >= len(pathX)):
                                        continue    

                                    try:
                                        
                                        didMove = False

                                        if(pathX[idx] == 'L'):
                                            dirt_machines[index].move_left()
                                            didMove = True
                                        if(pathX[idx] == 'U'):
                                            dirt_machines[index].move_up()
                                            didMove = True
                                        if(pathX[idx] == 'D'):
                                            dirt_machines[index].move_down()
                                            didMove = True
                                        if(pathX[idx] == 'R'):
                                            dirt_machines[index].move_right()
                                            didMove = True

                                       # if(idx >= 1):
                                        for x in vacuums:
                                            x.move_to_closest_dirt()
                            
                                        if( intelligenceDirtFirst):
                                            pygame.time.delay(globals.globals.speed)

                                    except Exception:
                                        pass
                                    
                                    

                                
                                
                    else:
                        for x in dirt_machines:
                            x.move_from_closest_dirt()


    elif(case2):  # fully observable and dirt keeps getting added
        count = 0
        while run:
            if(count == globals.globals.frequency):
                d.probabilistic_dirt(1)
                count = 0
            
            if(not intelligenceDirtFirst):
                pygame.time.delay(globals.globals.speed)
            clock.tick(10)

            for event in pygame.event.get():

                #gameover
                if (event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (event.key == pygame.K_ESCAPE))):
                    globals.globals.end_duration= datetime.now().timestamp()
                    layout2 = [[sg.Text('Duration: ' + str(round(globals.globals.end_duration-globals.globals.start_duration,3)))],
                    [sg.Text('Number of cleaned tiles: '+ str(globals.globals.nb_clean_tiles))],
                    [sg.Text('Number of steps: '+ str(globals.globals.nb_steps))],
                    [sg.Text('Number of added dirt: '+ str(globals.globals.nb_added_dirt))],
                    [sg.Text('Average number of steps per dirt: '+ str(round(globals.globals.nb_steps/globals.globals.nb_clean_tiles)))],
                    [sg.Text('Average time to clean a dirt: ' + str(round(round(globals.globals.end_duration-globals.globals.start_duration,3)/globals.globals.nb_clean_tiles, 2)))],
                    [sg.Button('Exit')]]
                    window1 = sg.Window('Measures', layout2)
                    window1.Read()
                    game_over = True
                    r.clear_room()
                    window.fill((0,0,0))
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text_surface = font.render("Game Over", True, (150,150,150))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (window.get_width()//2, window.get_height()//2)
                    window.blit(text_surface, text_rect)
                    pygame.display.update()
                    vacuums[0].set_position((rows//2)+1,(cols//2)-1)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)
                    vacuums[0].move_left()
                    pygame.time.delay(500)
                    vacuums[0].move_right()
                    pygame.time.delay(500)
                    vacuums[0].move_right()
                    pygame.time.delay(500)
                    vacuums[0].move_right()

                    run = False
                    #arrows as input
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(5000)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if(not game_over):
                
                if(not intelligenceDirtFirst):
                    for x in vacuums:
                        x.move_to_closest_dirt()
                
                
                
                if(globals.globals.dirt_agents != 0):
                    if(intelligenceDirtFirst):
                       #Alternate Algrthm 
                        paths = mySolver.getFirstPathForDirt(r,dirt_machines,vacuums, boxIn)
                       
                        index = -1
                        if(not paths is None):
                            
                            m = len(paths[0])
                            for p in paths:
                                if(len(p) < m):
                                    m = len(p)
                            
                            for idx in range(0,m):
                                for pathX in paths:
                                    index += 1

                                    if( pathX is None or pathX == [] or len(pathX) == 0 or pathX[0] == None):
                                        continue

                                    if(idx >= len(pathX)):
                                        continue    

                                    try:
                                        
                                        didMove = False

                                        if(pathX[idx] == 'L'):
                                            dirt_machines[index].move_left()
                                            didMove = True
                                        if(pathX[idx] == 'U'):
                                            dirt_machines[index].move_up()
                                            didMove = True
                                        if(pathX[idx] == 'D'):
                                            dirt_machines[index].move_down()
                                            didMove = True
                                        if(pathX[idx] == 'R'):
                                            dirt_machines[index].move_right()
                                            didMove = True

                                       # if(idx >= 1):
                                        for x in vacuums:
                                            x.move_to_closest_dirt()
                            
                                        if( intelligenceDirtFirst):
                                            pygame.time.delay(globals.globals.speed)

                                    except Exception:
                                        pass
                                    
                                    

                                
                                
                    else:
                        for x in dirt_machines:
                            x.move_from_closest_dirt()

            count += 1

    #Partially visible in HERE
    elif(case3):

        dirtMachineIntelligence = 0
        if(intelligenceDirtFirst):
            dirtMachineIntelligence = 1

        path = []
        pathDirt = []

        count = 0

        mySolver.expoloreAllBorders()

        cyclesStuckCount = [1]
        cycleStuckPos = [ [0,0] ]

        cyclesStuckCountDirt = [1]
        cycleStuckPosDirt = [ [0,0] ]

        while run:

            if(count >= globals.globals.frequency):
                d.probabilistic_dirt(1)
                count = 0
            #FOR DEBUGGING
            #NOTE TO SELF => REMOVE LATER ON
            #d.rnd_dirt_DEBUG(1)
            count += 1
            #////////////////////////////////////

            pygame.time.delay(globals.globals.speed)
            clock.tick(10)

            for event in pygame.event.get():
                #gameover
                if (event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (event.key == pygame.K_ESCAPE))):
                    game__over=True
                    globals.globals.end_duration= datetime.now().timestamp()
                    layout2 = [[sg.Text('Duration: ' + str(round(globals.globals.end_duration-globals.globals.start_duration,3)))],
                    [sg.Text('Number of cleaned tiles: '+ str(globals.globals.nb_clean_tiles))],
                    [sg.Text('Number of steps: '+ str(globals.globals.nb_steps))],
                    [sg.Text('Number of added dirt: '+ str(globals.globals.nb_added_dirt))],
                    [sg.Text('Average number of steps per dirt: '+ str(round(globals.globals.nb_steps/globals.globals.nb_clean_tiles)))],
                    [sg.Text('Average time to clean a dirt: ' + str(round(round(globals.globals.end_duration-globals.globals.start_duration,3)/globals.globals.nb_clean_tiles, 2)))],
                    [sg.Button('Exit')]]
                    window1 = sg.Window('Measures', layout2)
                    window1.Read()
                    r.clear_room()
                    path=["R","R","R","R"]
                    window.fill((0,0,0))
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text_surface = font.render("Game Over", True, (150,150,150))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (window.get_width()//2, window.get_height()//2)
                    window.blit(text_surface, text_rect)
                    pygame.display.update()
                    vacuums[0].set_position((rows//2)+1,(cols//2)-1)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)

                    run = False
                    #arrows as input
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(5000)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            index = -1
            for v in vacuums:

                index += 1
                if(len(path) < index + 1):
                    path.append([])
                if(len(cyclesStuckCount) < index + 1):
                    cyclesStuckCount.append(1)
                    cycleStuckPos.append( [0,0] )

                if(pos2 is None):
                    pos2 = r.vacuum_position(index)

                pos2 = copy.deepcopy ( r.vacuum_position(index) )
                #pos2 = r.vacuum_position()

                pos2 = mySolver.dirtPathIterator( copy.deepcopy( pos2 ) )

                #print("pos 2")
                #print(pos2)

                if(not game__over):
                    path[index] = mySolver.getLastActualUsedPath()
                    #machine.move_from_closest_dirt()


                # Take care of dynmaic collision

                #if stuck by other agent abort mission
                if(cyclesStuckCount[index] > 1):
                    #print(cycleStuckPos[index])
                    cyclesStuckCount[index] = 1
                    mySolver.escapeFromAgent(r.vacuum_position(index), cycleStuckPos[index] )
                    path[index] = mySolver.getLastActualUsedPath();

            if(dirtMachineIntelligence == 0):
                index = -1
                for _ in dirt_machines:

                    index += 1
                    if(len(pathDirt) < index + 1):
                        pathDirt.append([])
                    if(len(cyclesStuckCountDirt) < index + 1):
                        cyclesStuckCountDirt.append(1)
                        cycleStuckPosDirt.append( [0,0] )

                    if(pos2 is None):
                        pos2 = r.dirt_machine_position(index)

                    pos2 = copy.deepcopy ( r.dirt_machine_position(index) )
                    #pos2 = r.vacuum_position()

                    pos2 = mySolver.addDirtPathIterator( copy.deepcopy( pos2 ) )

                    #print("pos 2")
                    #print(pos2)

                    if(not game__over):
                        pathDirt[index] = mySolver.getLastActualUsedPath()
                        #machine.move_from_closest_dirt()


                    # Take care of dynmaic collision

                    #if stuck by other agent abort mission
                    if(cyclesStuckCountDirt[index] > 1):
                        #print(cycleStuckPos[index])
                        cyclesStuckCountDirt[index] = 1
                        mySolver.escapeFromAgent(r.dirt_machine_position(index), cycleStuckPosDirt[index] )
                        pathDirt[index] = mySolver.getLastActualUsedPath();


            m = len(path[0])
            for p in path:
                if(len(p) < m):
                    m = len(p)

            if(dirtMachineIntelligence == 0):
                for p in pathDirt:
                    if(len(p) < m):
                        m = len(p)



            for idx in range(0,m):

                index = -1
                for pathX in path:

                    index += 1

                    #print(index)
                    #print(idx)

                    p = pathX[idx]

                    # Take care of dynmaic collision
                    if( not p in vacuums[index].get_valid_moves() ):
                        #print("Vacuum Was Gonna Hit")
                        #exit(0)
                        cyclesStuckCount[index] += 1

                        deltX = 0
                        deltaY = 0
                        if(p == "L"):
                            deltX = -1
                        elif(p == "R"):
                            deltX = 1
                        elif(p == "U"):
                            deltaY = -1
                        elif(p == "D"):
                            deltaY = 1

                        cycleStuckPos[index] = [r.vacuum_position(index)[0] + deltaY, r.vacuum_position(index)[1] + deltX, ]

                        continue;


                    if(p == "L"):
                        vacuums[index].move_left()
                    elif(p == "R"):
                        vacuums[index].move_right()
                    elif(p == "U"):
                        vacuums[index].move_up()
                    elif(p == "D"):
                        vacuums[index].move_down()

                    mySolver.addExploredToGrid(r.get_array(), r.vacuum_position(index)[0], r.vacuum_position(index)[1] )

                    # if(globals.globals.dirt_agents != 0):
                    #     for x in dirt_machines:
                    #         x.move_from_closest_dirt()
                    # else:
                    #     pass

                    #if(not game__over and globals.globals.dirt_agents > 0):
                    #    dirt_machines[0].move_from_closest_dirt()

                if(dirtMachineIntelligence == 0):
                    index = -1
                    for pathX in pathDirt:

                        index += 1

                        if(isVacuumNeghbr(r,vacuums, r.dirt_machine_position(index), boxIn )):
                            continue

                        p = pathX[idx]

                        # Take care of dynmaic collision
                        if( not p in dirt_machines[index].get_valid_moves() ):
                            #print("Vacuum Was Gonna Hit")
                            #exit(0)
                            cyclesStuckCountDirt[index] += 1

                            deltX = 0
                            deltaY = 0
                            if(p == "L"):
                                deltX = -1
                            elif(p == "R"):
                                deltX = 1
                            elif(p == "U"):
                                deltaY = -1
                            elif(p == "D"):
                                deltaY = 1

                            cycleStuckPosDirt[index] = [r.dirt_machine_position(index)[0] + deltaY, r.dirt_machine_position(index)[1] + deltX, ]

                            continue;


                        if(p == "L"):
                            dirt_machines[index].move_left()
                        elif(p == "R"):
                            dirt_machines[index].move_right()
                        elif(p == "U"):
                            dirt_machines[index].move_up()
                        elif(p == "D"):
                            dirt_machines[index].move_down()
                        
                        dirt_machines[index].incrementCountForDirt(8)


                if(dirtMachineIntelligence == 1):
                    for mac in dirt_machines:
                        mac.move_from_closest_dirt()

                pygame.time.delay(globals.globals.speed)

            #pos2 = r.vacuum_position();

            pygame.display.update()

    elif(case4):

        path = []

        count = 0

        dirtMachineIntelligence = 0
        if(intelligenceDirtFirst):
            dirtMachineIntelligence = 1

        cyclesStuckCount = [1]
        cycleStuckPos = [ [0,0] ]

        tempLastLoc = []

        pathDirt = []

        cyclesStuckCountDirt = [1]
        cycleStuckPosDirt = [ [0,0] ]

        while run:

            if(count >= globals.globals.frequency):
                d.probabilistic_dirt(1)
                count = 0
            #FOR DEBUGGING
            #NOTE TO SELF => REMOVE LATER ON
            #d.rnd_dirt_DEBUG(1)
            count += 1
            #////////////////////////////////////

            pygame.time.delay(globals.globals.speed)
            clock.tick(10)

            for event in pygame.event.get():
                #gameover
                if (event.type == pygame.QUIT or ((event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (event.key == pygame.K_ESCAPE))):
                    game__over=True
                    globals.globals.end_duration= datetime.now().timestamp()
                    layout2 = [[sg.Text('Duration: ' + str(round(globals.globals.end_duration-globals.globals.start_duration,3)))],
                    [sg.Text('Number of cleaned tiles: '+ str(globals.globals.nb_clean_tiles))],
                    [sg.Text('Number of steps: '+ str(globals.globals.nb_steps))],
                    [sg.Text('Number of added dirt: '+ str(globals.globals.nb_added_dirt))],
                    [sg.Text('Average number of steps per dirt: '+ str(round(globals.globals.nb_steps/globals.globals.nb_clean_tiles)))],
                    [sg.Text('Average time to clean a dirt: ' + str(round(round(globals.globals.end_duration-globals.globals.start_duration,3)/globals.globals.nb_clean_tiles, 2)))],
                    [sg.Button('Exit')]]
                    window1 = sg.Window('Measures', layout2)
                    window1.Read()
                    r.clear_room()
                    path=["R","R","R","R"]
                    window.fill((0,0,0))
                    font = pygame.font.Font('freesansbold.ttf', 20)
                    text_surface = font.render("Game Over", True, (150,150,150))
                    text_rect = text_surface.get_rect()
                    text_rect.center = (window.get_width()//2, window.get_height()//2)
                    window.blit(text_surface, text_rect)
                    pygame.display.update()
                    v.set_position((rows//2)+1,(cols//2)-3)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)

                    run = False
                    #arrows as input
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                       pygame.time.delay(5000)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #EXPLORE MAP CODE

            index = -1
            for v in vacuums:

                index += 1
                if(len(path) < index + 1):
                    path.append([])
                if(len(cyclesStuckCount) < index + 1):
                    cyclesStuckCount.append(1)
                    cycleStuckPos.append( [0,0] )
                if(len(tempLastLoc) < index + 1):
                    tempLastLoc.append( [] )

                #if(index > 1):
                #    print("Impossible Indx")
                #    exit(0)

                if (pos is None or not pos[0] == -1):

                    if(not pos is None):
                        tempLastLoc[index] = copy.deepcopy( pos )


                    pos = mySolver.discoverMapIter( copy.deepcopy(r.vacuum_position(index)) )
                    #print('target pos: ' + str(pos) )


                    if(not game__over):
                        path[index] = mySolver.getLastActualUsedPath()

                    #print('path: ' + str(path) )
                    #print(r.vacuum_position() )


                else:

                    #print("Dirt Phase")

                    if(pos2 is None):
                        pos2 = tempLastLoc[index]



                    pos2 = mySolver.dirtPathIterator( copy.deepcopy( r.vacuum_position(index) ) )

                    #pos2 = mySolver.dirtPathIterator( copy.deepcopy( pos2 ) )


                    #print("pos 2")
                    #print(pos2)
                    if(not game__over):
                        path[index] = mySolver.getLastActualUsedPath()

                pst = [-1,-1]
                #if stuck by other agent abort mission
                if(cyclesStuckCount[index] > 1):
                    #print("getting out")
                    cyclesStuckCount[index] = 1
                    pst = mySolver.escapeFromAgent(r.vacuum_position(index), cycleStuckPos[index] )
                    path[index] = mySolver.getLastActualUsedPath();
                    #print("agent")
                    #print(index)
                    #print(pst)

                #print(index)
                #print("My pos")
                #print(r.vacuum_position(index))
                #print("dest")
                #if(pst[0] == -1):
                #    print(pos2)
                #else:
                #    print(pst)
                #print("path")
                #print(path[index])

            if(dirtMachineIntelligence == 0):
                index = -1
                for _ in dirt_machines:

                    index += 1
                    if(len(pathDirt) < index + 1):
                        pathDirt.append([])
                    if(len(cyclesStuckCountDirt) < index + 1):
                        cyclesStuckCountDirt.append(1)
                        cycleStuckPosDirt.append( [0,0] )

                    if(pos2 is None):
                        pos2 = r.dirt_machine_position(index)

                    pos2 = copy.deepcopy ( r.dirt_machine_position(index) )
                    #pos2 = r.vacuum_position()

                    pos2 = mySolver.addDirtPathIterator( copy.deepcopy( pos2 ) )

                    #print("pos 2")
                    #print(pos2)

                    if(not game__over):
                        pathDirt[index] = mySolver.getLastActualUsedPath()
                        #machine.move_from_closest_dirt()


                    # Take care of dynmaic collision

                    #if stuck by other agent abort mission
                    if(cyclesStuckCountDirt[index] > 1):
                        #print(cycleStuckPos[index])
                        cyclesStuckCountDirt[index] = 1
                        mySolver.escapeFromAgent(r.dirt_machine_position(index), cycleStuckPosDirt[index] )
                        pathDirt[index] = mySolver.getLastActualUsedPath();


            #END OF EXPLORATION

            #print("paths")
            #print(path[0])
            #print(path[1])

            m = len(path[0])
            for p in path:
                if(len(p) < m):
                    m = len(p)

            if(dirtMachineIntelligence == 0):
                for p in pathDirt:
                    if(len(p) < m):
                        m = len(p)

            if(m < 2):
                m = 3

            #print("M value")
            #print(m)

            for idx in range(0,m):

                index = -1
                for pathX in path:

                    index += 1

                    #print(index)
                    #print(idx)

                    if(idx >= len(pathX)):
                        continue


                    p = pathX[idx]

                    #mySolver.addExploredToGrid(r.get_array(), r.vacuum_position(index)[0], r.vacuum_position(index)[1] )
                    #print("in pathX loop")

                    if( not p in vacuums[index].get_valid_moves() ):
                       # print(p + " Vacuum Was Gonna Hit")
                        #exit(0)

                        cyclesStuckCount[index] += 1

                        deltX = 0
                        deltaY = 0
                        if(p == "L"):
                            deltX = -1
                        elif(p == "R"):
                            deltX = 1
                        elif(p == "U"):
                            deltaY = -1
                        elif(p == "D"):
                            deltaY = 1

                        cycleStuckPos[index] = [r.vacuum_position(index)[0] + deltaY, r.vacuum_position(index)[1] + deltX ]

                        #print(cycleStuckPos[index])

                        #print(cyclesStuckCount[index])

                        continue;

                    if(p == "L"):
                        vacuums[index].move_left()
                    elif(p == "R"):
                        vacuums[index].move_right()
                    elif(p == "U"):
                        vacuums[index].move_up()
                    elif(p == "D"):
                        vacuums[index].move_down()

                    #print("moved vacuum " + str(index) )


                    mySolver.addExploredToGrid(r.get_array(), r.vacuum_position(index)[0], r.vacuum_position(index)[1] )

                    #if(not game__over):
                    #    machine.move_from_closest_dirt()

                if(dirtMachineIntelligence == 0):
                    index = -1
                    for pathX in pathDirt:

                        index += 1

                        if(isVacuumNeghbr(r,vacuums, r.dirt_machine_position(index) , boxIn)):
                            continue

                        if(idx >= len(pathX)):
                            continue

                        p = pathX[idx]

                        # Take care of dynmaic collision
                        if( not p in dirt_machines[index].get_valid_moves() ):
                            #print("Vacuum Was Gonna Hit")
                            #exit(0)
                            cyclesStuckCountDirt[index] += 1

                            deltX = 0
                            deltaY = 0
                            if(p == "L"):
                                deltX = -1
                            elif(p == "R"):
                                deltX = 1
                            elif(p == "U"):
                                deltaY = -1
                            elif(p == "D"):
                                deltaY = 1

                            cycleStuckPosDirt[index] = [r.dirt_machine_position(index)[0] + deltaY, r.dirt_machine_position(index)[1] + deltX, ]

                            continue;


                        if(p == "L"):
                            dirt_machines[index].move_left()
                        elif(p == "R"):
                            dirt_machines[index].move_right()
                        elif(p == "U"):
                            dirt_machines[index].move_up()
                        elif(p == "D"):
                            dirt_machines[index].move_down()

                        dirt_machines[index].incrementCountForDirt(8)


                        #print("moved machine " + str(index) )

                if(dirtMachineIntelligence == 1):
                    for mac in dirt_machines:
                        mac.move_from_closest_dirt()

                pygame.time.delay(globals.globals.speed)

            path[index] = []
            if(dirtMachineIntelligence == 0):
                pathDirt[index] = []
           

            #print("idx loop")

            pygame.display.update()



    pygame.quit()
main()
