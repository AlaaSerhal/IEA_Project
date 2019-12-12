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
            [sg.Text('Speed:'),sg.Slider(range=(1000,100),default_value=1000,size=(20,15),orientation='horizontal', disable_number_display=True)],
            [sg.Frame(layout=[
            [sg.Radio('Case1 (Fully observable map and once generated dirt):', "Case1", default=False)],
            [sg.Radio('Case2 (Fully observable map and continuously added dirt):', "Case1", default=False)],
            [sg.Radio('Case3 (Fully observable borders and unknown dirt positions):', "Case1", default=False)],
            [sg.Radio('Case4 (Unknown borders and dirt positions):', "Case1", default=False)]],
            title='Choose Any of these Cases',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
            [sg.Submit()]]
            window = sg.Window('Vacuum Cleaner Agent', layout)
            event, values = window.Read()
            case1=values[5]
            case2=values[6]
            case3=values[7]
            case4=values[8]
            rows=int(values[0])
            cols=int(values[1])
            dirty_tiles= int(values[2])
            borders=int(values[3])
            globals.globals.speed=int(values[4])
            print(int(values[4]))
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

    v = vacuum(r, window)
    machine = dirt_machine(r, window)
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
                    v.set_position((rows//2)+1,(cols//2)-1)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)
                    v.move_left()
                    pygame.time.delay(500)
                    v.move_right()
                    pygame.time.delay(500)
                    v.move_right()
                    pygame.time.delay(500)
                    v.move_right()

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
                v.move_to_closest_dirt()
                machine.move_from_closest_dirt()

    elif(case2):  # fully observable and dirt keeps getting added
        count = 0
        while run:
            if(count == 4):
                d.probabilistic_dirt(1)
                count = 0
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
                    v.set_position((rows//2)+1,(cols//2)-1)
                    pygame.mixer.music.load('game-over.wav')
                    pygame.mixer.music.play(2)
                    v.move_left()
                    pygame.time.delay(500)
                    v.move_right()
                    pygame.time.delay(500)
                    v.move_right()
                    pygame.time.delay(500)
                    v.move_right()

                    run = False
                    #arrows as input
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(5000)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if(not game_over):
                v.move_to_closest_dirt()
                machine.move_from_closest_dirt()
            count += 1

    #Partially visible in HERE
    elif(case3):

        path = []

        count = 0

        mySolver.expoloreAllBorders()

        while run:

            if(count >= 3):
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
                    v.set_position((rows//2)+1,(cols//2)-1)
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
            #CASE 4


            if(pos2 is None):
                pos2 = r.vacuum_position()



            pos2 = mySolver.dirtPathIterator( copy.deepcopy( pos2 ) )

            print("pos 2")
            print(pos2)
            if(not game__over):
                path = mySolver.getLastActualUsedPath()

            #END OF EXPLORATION

            for p in path:
                if(p == "L"):
                    v.move_left()
                elif(p == "R"):
                    v.move_right()
                elif(p == "U"):
                    v.move_up()
                elif(p == "D"):
                    v.move_down()
                pygame.time.delay(globals.globals.speed)

            pygame.display.update()

    elif(case4):

        path = []

        count = 0

        while run:

            if(count >= 3):
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
            #CASE 4



            if(pos is None):
                pos = mySolver.discoverMapIter( copy.deepcopy(r.vacuum_position()) )
                print('target pos: ' + str(pos) )

            if (not pos[0] == -1):
                if(not game__over):
                    path = mySolver.getLastActualUsedPath()

                print('path: ' + str(path) )

                print(r.vacuum_position() )

                tempLastLoc = copy.deepcopy( pos )

                pos = mySolver.discoverMapIter( copy.deepcopy( pos ) )

                print('target pos: ' + str(pos) )

                #pygame.display.update()

            else:

                if(pos2 is None):
                    pos2 = tempLastLoc



                pos2 = mySolver.dirtPathIterator( copy.deepcopy( pos2 ) )

                print("pos 2")
                print(pos2)
                if(not game__over):
                    path = mySolver.getLastActualUsedPath()

                #path = []

            #END OF EXPLORATION

            for p in path:
                if(p == "L"):
                    v.move_left()
                elif(p == "R"):
                    v.move_right()
                elif(p == "U"):
                    v.move_up()
                elif(p == "D"):
                    v.move_down()
                pygame.time.delay(globals.globals.speed)

            pygame.display.update()



    pygame.quit()
main()

