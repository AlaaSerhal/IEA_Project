import pygame
import random
from room import room
from math import hypot

class dirt:
    def __init__(self, room, window, initial_number=6):
        self.room = room
        self.window = window
        self.initial_number = initial_number
        self.tile_dirt = []

        # pick random position for an open window at the borders
        rnd = random.randint(0,4)
        if(rnd == 0):
            self.entrance = [random.randint(0, self.room.get_rows()-1), 0]
        elif(rnd == 1):
            self.entrance = [random.randint(0, self.room.get_rows()-1), self.room.get_cols()-1]
        elif(rnd == 2):
            self.entrance = [0, random.randint(0, self.room.get_cols()-1)]
        else:
            self.entrance = [self.room.get_rows()-1, random.randint(0, self.room.get_cols()-1)]

        print("Open window at: ", self.entrance)

        # assign priority to cells
        # cells near the window have higher priority and ths more cances of having dirt generated on them
        for row in range(self.room.get_rows()):
            for col in range(self.room.get_cols()):
                dist = self.calculate_distance(self.entrance, [row,col])
                proba = int(max(self.room.get_rows(),self.room.get_cols())-dist)
                if(proba == 0 or proba == -1):
                    proba = 1
                x = [[row, col]]*proba  # position of cell is inserted as many times as its priority
                self.tile_dirt.extend(x)
        i = 0
        count = 0
        while(i < initial_number and count < 10):  # randomly spread specified number of dirt
            col = random.randint(0, self.room.get_cols()-1)
            row = random.randint(0, self.room.get_rows()-1)
            # cell is already occupied by dirt or vacuum
            if(self.room.get_array()[row][col].has_dirt() or self.room.get_array()[row][col].has_vacuum()):
                count += 1
            else:  # set dirt
                self.room.set_dirt(row, col)
                i += 1
        
        random.shuffle(x)

    def calculate_distance(self, pos1, pos2):  # calculate distance between 2 cells
        if(pos1[0] == pos2[0]):
            dist = abs(pos1[1] - pos2[1])
        elif(pos1[1] == pos2[1]):
            dist = abs(pos1[0] - pos2[0])
        else:
            delta_r = abs(pos1[0] - pos2[0])
            delta_c = abs(pos1[1] - pos2[1])
            dist = hypot(delta_c, delta_r)
        return dist

    def rnd_dirt(self, number):  # generate random dirt with no specific distribution
        i = 0
        count = 0
        while(i < number and count < 10):
            col = random.randint(0, self.room.get_cols()-1)
            row = random.randint(0, self.room.get_rows()-1)

            if(self.room.get_array()[row][col].has_dirt() or self.room.get_array()[row][col].has_vacuum()):
                count += 1
            else:
                self.room.set_dirt(row, col)
                i += 1


    def rnd_dirt_DEBUG(self, number):  # for debugging, generate dirt in one quadrant
        i = 0
        count = 0
        while(i < number and count < 10):
            #col = random.randint(0, self.room.get_cols()-1)
            #row = random.randint(0, self.room.get_rows()-1)
            col = random.randint(0, 2)
            row = random.randint(0, 2)
            if(self.room.get_array()[row][col].has_dirt() or self.room.get_array()[row][col].has_vacuum()):
                count += 1
            else:
                self.room.set_dirt(row, col)
                i += 1

    def probabilistic_dirt(self, number):  # generate dirt according to priorities of cells
        i = 0
        count = 0
        while(i < number and count < 10):
            x = random.randint(0, len(self.tile_dirt)-1)  # pick a random index
            row = self.tile_dirt[x][0]
            col = self.tile_dirt[x][1]
            # cell is already occupied by dirt or vacuum
            if(self.room.get_array()[row][col].has_dirt() or self.room.get_array()[row][col].has_vacuum()):
                count += 1
            elif(not self.room.get_array()[row][col].is_occupied()):  # set dirt
                self.room.set_dirt(row, col)
                i += 1
