import pygame
import operator
import random
from math import hypot

class vacuum:
    def __init__(self, room, window):
        self.img = pygame.image.load("vacuum.png")
        self.room = room
        self.window = window
        self.prev_move = None
        self.prev_prev_move = None
        self.loop = False

    def set_position(self, row, col):
        old = self.room.vacuum_position()
        old_col = old[1]
        old_row = old[0]
        cell_size = self.room.get_cell_size()
        self.room.set_vacuum(row, col)
        left = int((col*cell_size)+2)
        top = int((row*cell_size)+2)
        pygame.draw.rect(self.window, (0,0,0),((old_col*cell_size)+1, (old_row*cell_size)+1, cell_size-2, cell_size-2), False)
        if(self.room.get_array()[row][col].has_dirt()):
            self.room.clean_tile(row, col)
            pygame.draw.rect(self.window, (0,0,0),((old_col*cell_size)+1, (old_row*cell_size)+1, cell_size-2, cell_size-2), False)
        self.window.blit(self.img, (left, top))
        pygame.display.update()

    def move_up(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_up_border() and row > 0):
            self.set_position(row-1, col)
            self.prev_prev_move = self.prev_move
            self.prev_move = 1
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def move_down(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_down_border() and row < self.room.get_rows()-1):
            self.set_position(row+1, col)
            self.prev_prev_move = self.prev_move
            self.prev_move = -1
        else:
            raise Exception("Invalid move! Cannot move down from current position.")

    def move_right(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_right_border() and col < self.room.get_cols()-1):
            self.set_position(row, col+1)
            self.prev_prev_move = self.prev_move
            self.prev_move = 2
        else:
            raise Exception("Invalid move! Cannot move right from current position.")

    def move_left(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position()
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_left_border() and col > 0):
            self.set_position(row, col-1)
            self.prev_prev_move = self.prev_move
            self.prev_move = -2
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def get_valid_moves(self):
        moves = []
        tile = self.room.get_vacuum_tile()
        if(not tile.has_up_border()):
            moves.append("U")
        if(not tile.has_left_border()):
            moves.append("L")
        if(not tile.has_down_border()):
            moves.append("D")
        if(not tile.has_right_border()):
            moves.append("R")
        return moves

    def calculate_distance(self, pos1, pos2):
        if(pos1[0] == pos2[0]):
            dist = abs(pos1[1] - pos2[1])
        elif(pos1[1] == pos2[1]):
            dist = abs(pos1[0] - pos2[0])
        else:
            delta_r = abs(pos1[0] - pos2[0])
            delta_c = abs(pos1[1] - pos2[1])
            dist = hypot(delta_c, delta_r)
        return dist

    def move_to_closest_dirt(self):
        distances = []
        valid_moves = self.get_valid_moves()
        min_distance = 10000
        closest_dirt = None
        current_position = self.room.vacuum_position()

        for dirt in self.room.get_dirt_list():
            if(len(valid_moves) != 0):
                dist = self.calculate_distance(current_position, dirt)
                distances.append(dist)
                if(dist < min_distance):
                    min_distance = dist
                    closest_dirt = [dirt[0], dirt[1]]
        # print("closest dirt: ", closest_dirt, " at distance: ", min_distance)

        min_new_dist = 10000
        best_move = ""

        # if(len(valid_moves) == 1):
        #     pass
        # elif(self.prev_move == "U"):
        #     valid_moves.remove("D")
        # elif(self.prev_move == "D"):
        #     valid_moves.remove("U")
        # elif(self.prev_move == "R"):
        #     valid_moves.remove("L")
        # elif(self.prev_move == "L"):
        #     valid_moves.remove("R")
        # else:
        #     pass
        dict = {}
        for move in valid_moves:
            if(move == "U"):
                new_pos = [current_position[0]-1, current_position[1]]
            elif(move == "D"):
                new_pos = [current_position[0]+1, current_position[1]]
            elif(move == "L"):
                new_pos = [current_position[0], current_position[1]-1]
            elif(move == "R"):
                new_pos = [current_position[0], current_position[1]+1]
            else:
                pass
            new_dist = self.calculate_distance(new_pos, closest_dirt)
            dict[new_dist] = move
            # if(new_dist < min_new_dist):
            #     min_new_dist = new_dist
            #     best_move = move
        # print("best move is: ", best_move)
        sorted_dict = sorted(dict.items(), key=operator.itemgetter(0))
        best_move = sorted_dict[0][1]


        if(best_move == "U"):
            x = 1
        elif(best_move == "D"):
            x = -1
        elif(best_move == "R"):
            x = 2
        elif(best_move == "L"):
            x = -2
        else:
            x = 0

        if(self.loop is True):
            if(len(sorted_dict) > 1):
                best_move = sorted_dict[random.randint(1, len(sorted_dict)-1)][1]
            print("getting unstuck")
            self.loop = False

        if(x == self.prev_prev_move and x == -self.prev_move):
            self.loop = True

        if(best_move == "U"):
            self.move_up()
        elif(best_move == "D"):
            self.move_down()
        elif(best_move == "L"):
            self.move_left()
        elif(best_move == "R"):
            self.move_right()
        else:
            pass
