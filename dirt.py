import pygame
import random
from room import room

class dirt:
    def __init__(self, room, window, initial_number):
        self.room = room
        self.window = window
        self.initial_number = initial_number
        i = 0
        count = 0
        while(i < initial_number and count < 10):
            col = random.randint(0, self.room.get_cols()-1)
            row = random.randint(0, self.room.get_rows()-1)
            if(self.room.get_array()[row][col].has_dirt() or self.room.get_array()[row][col].has_vacuum()):
                count += 1
            else:
                self.room.set_dirt(row, col)
                i += 1


    def rnd_dirt(self, number):
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
