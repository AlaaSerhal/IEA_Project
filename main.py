import pygame
from vacuum import vacuum
import PySimpleGUI as sg
from room import room
from dirt import dirt


def main():
    rows, cols = 15, 15
    while(rows >= 15 or cols >= 15 or rows==0 or cols==0):
        try:
            layout = [  [sg.Text('Necessary Inputs')],
            [sg.Text('Please enter number of rows as an integer:'), sg.InputText()],
            [sg.Text('Please enter number of cols as an integer:'), sg.InputText()],
            [sg.Submit(), sg.Cancel()]]
            window = sg.Window('Vacuum Cleaner Agent', layout)
            event, values = window.Read()
            rows=int(values[0])
            cols=int(values[1])
            if event in (None, 'Cancel'):
                print('Canceled')
                exit()
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
    path = ["D", "L", "U", "R"]
    while run:
        d.rnd_dirt(1)
        pygame.time.delay(50)
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
