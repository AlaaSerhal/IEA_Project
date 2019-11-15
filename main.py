import pygame as pygame
from vacuum import vacuum
import PySimpleGUI as sg
from room import room
from dirt import dirt


from solver import solver
import copy


def main():
    rows, cols = 15, 15
    while(rows >= 15 or cols >= 15 or rows==0 or cols==0):
        try:
            layout = [  [sg.Text('Necessary Inputs')],
            [sg.Text('Please enter number of rows as an integer:'), sg.InputText()],
            [sg.Text('Please enter number of cols as an integer:'), sg.InputText()],
            [sg.Frame(layout=[
            [sg.Radio('Case1 (Fully observable map and once generated dirt):', "Case1", default=False)],
            [sg.Radio('Case2 (Fully observable map and continuously added dirt):', "Case1", default=False)],
            [sg.Radio('Case3 (Fully observable borders and unknown dirt positions):', "Case1", default=False)],
            [sg.Radio('Case4 (Unknown borders and dirt positions):', "Case1", default=False)]],
            title='Choose Any of these Cases',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
            [sg.Submit()]]
            window = sg.Window('Vacuum Cleaner Agent', layout)
            event, values = window.Read()
            case1=values[2]
            case2=values[3]
            case3=values[4]
            case4=values[5]
            rows=int(values[0])
            cols=int(values[1])
            if event in ('Submit'):
                print('Borders are placed randomly')
            window.Close()
        except ValueError:
            print("No valid integer! Please try again ...")
    CELL_SIZE = 40
    window_size = [cols * CELL_SIZE, rows * CELL_SIZE]
    pygame.init()

    # dirt_img = pygame.image.load("dirt.png")

    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Vacuum Cleaner Agent")
    run = True
    clock = pygame.time.Clock()
    r = room(CELL_SIZE, rows, cols, window)
    r.draw_grid()
    r.draw_borders()

    # r.add_nodes()

    v = vacuum(r, window)
    d = dirt(r, window, 4)
    # window.blit(vacuum_img, (50,50))
    # window.blit(dirt_img, (200,200))

    pos = None
    mySolver = solver(r.get_array())        

    tempLastLoc = None
    pos2 = None

    path = ["D", "L", "U", "R"]
    while run:
        d.rnd_dirt(1)
        pygame.time.delay(50)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #EXPLORE MAP CODE
        #CASE 4

        

        if(pos is None):
            pos = mySolver.discoverMapIter( copy.deepcopy(r.vacuum_position()) )
            print('target pos: ' + str(pos) )
        
        if (not pos[0] == -1):
    
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
            pygame.time.delay(500)

        pygame.display.update()

    pygame.quit()

main()
