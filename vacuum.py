import pygame
import operator
import random
from math import hypot
import globals
class vacuum:
    def __init__(self, room, window, id=0):
        self.img = pygame.image.load("vacuum.png")
        self.room = room
        self.window = window
        # used to keep track of last 4 moves
        self.prev_move = None
        self.prev_prev_move = None
        self.prev_prev_prev_move = None
        self.prev_prev_prev_prev_move = None
        self.loop = False
        self.id = id

    def set_position(self, row, col):  # sets position of vaccum and moves the image and deletes the old image
        old = self.room.vacuum_position(self.id)
        old_col = old[1]
        old_row = old[0]
        cell_size = self.room.get_cell_size()
        self.room.set_vacuum(self.id, row, col)
        left = int((col*cell_size)+2)
        top = int((row*cell_size)+2)
        pygame.draw.rect(self.window, (0,0,0),((old_col*cell_size)+1, (old_row*cell_size)+1, cell_size-2, cell_size-2), False)
        globals.globals.nb_steps +=1
        if(self.room.get_array()[row][col].has_dirt()):
            self.room.clean_tile(row, col)
            globals.globals.nb_clean_tiles +=1
            pygame.draw.rect(self.window, (0,0,0),((old_col*cell_size)+1, (old_row*cell_size)+1, cell_size-2, cell_size-2), False)
        self.window.blit(self.img, (left, top))
        pygame.display.update()

    def move_up(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position(self.id)
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_up_border() and row > 0):
            self.set_position(row-1, col)
            # keeping track of previous moves
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
            self.prev_prev_move = self.prev_move
            self.prev_move = 1
        else:  # cannot move up if there is a border
            raise Exception("Invalid move! Cannot move up from current position.")

    def move_down(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position(self.id)
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_down_border() and row < self.room.get_rows()-1):
            self.set_position(row+1, col)
            # keeping track of previous moves
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
            self.prev_prev_move = self.prev_move
            self.prev_move = -1
        else:  # cannot move up if there is a border
            raise Exception("Invalid move! Cannot move down from current position.")

    def move_right(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position(self.id)
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_right_border() and col < self.room.get_cols()-1):
            self.set_position(row, col+1)
            # keeping track of previous moves
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
            self.prev_prev_move = self.prev_move
            self.prev_move = 2
        else:  # cannot move up if there is a border
            raise Exception("Invalid move! Cannot move right from current position.")

    def move_left(self):
        grid = self.room.get_array()
        position = self.room.vacuum_position(self.id)
        row = position[0]
        col = position[1]
        if(not grid[row][col].has_left_border() and col > 0):
            self.set_position(row, col-1)
            # keeping track of previous moves
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
            self.prev_prev_move = self.prev_move
            self.prev_move = -2
        else:  # cannot move up if there is a border
            raise Exception("Invalid move! Cannot move up from current position.")

    def get_moves_at_pos(self, pos):  # returns valid moves from a certain position in a grid
        moves = []
        grid = self.room.get_array()
        tile = grid[pos[0]][pos[1]]
        if(not tile.has_up_border()):
            if(not grid[pos[0]-1][pos[1]].is_occupied()):
                moves.append("U")
        if(not tile.has_left_border()):
            if(not grid[pos[0]][pos[1]-1].is_occupied()):
                moves.append("L")
        if(not tile.has_down_border()):
            if(not grid[pos[0]+1][pos[1]].is_occupied()):
                moves.append("D")
        if(not tile.has_right_border()):
            if(not grid[pos[0]][pos[1]+1].is_occupied()):
                moves.append("R")
        return moves

    def get_valid_moves(self):  # gets valid moves from vacuum position
        moves = []
        pos = self.room.vacuum_position(self.id)
        grid = self.room.get_array()
        tile = self.room.get_vacuum_tile(self.id)
        if(not tile.has_up_border()):
            if(not grid[pos[0]-1][pos[1]].is_occupied()):
                moves.append("U")
        if(not tile.has_left_border()):
            if(not grid[pos[0]][pos[1]-1].is_occupied()):
                moves.append("L")
        if(not tile.has_down_border()):
            if(not grid[pos[0]+1][pos[1]].is_occupied()):
                moves.append("D")
        if(not tile.has_right_border()):
            if(not grid[pos[0]][pos[1]+1].is_occupied()):
                moves.append("R")
        return moves

    def calculate_distance(self, pos1, pos2):  # calculates straight line distance between 2 positions
        if(pos1[0] == pos2[0]):
            dist = abs(pos1[1] - pos2[1])
        elif(pos1[1] == pos2[1]):
            dist = abs(pos1[0] - pos2[0])
        else:
            delta_r = abs(pos1[0] - pos2[0])
            delta_c = abs(pos1[1] - pos2[1])
            dist = hypot(delta_c, delta_r)
        return dist

    def get_relative_position(self, src, dst):  # checks which direction the dirt is
        src_row = src[0]
        src_col = src[1]
        dst_row = dst[0]
        dst_col = dst[1]

        pos = []

        if(dst_row > src_row):  # dirt is below
            pos.append("D")
        elif(dst_row < src_row):  # dirt is above
            pos.append("U")
        else:  # dirt is at even horizontal location
            pos.append("E")

        if(dst_col > src_col):  # dirt is to the right
            pos.append("R")
        elif(dst_col < src_col):  # dirt is to the left
            pos.append("L")
        else:  # dirt is at same vertical location
            pos.append("E")

        return pos


    def move_to_closest_dirt(self):  # take one step closer to closest dirt

        next_pos = None

        distances = []
        valid_moves = self.get_valid_moves()
        min_distance = 10000
        closest_dirt = None
        current_position = self.room.vacuum_position(self.id)
        dirt_list = self.room.get_dirt_list()
        if(len(dirt_list) != 0):  # check if there is any dirt left on the map
            for dirt in dirt_list:  # calculate distance between vacuum and every dirt
                if(len(valid_moves) != 0):
                    dist = self.calculate_distance(current_position, dirt)
                    distances.append(dist)
                    if(dist < min_distance):  # get closest dirt
                        min_distance = dist
                        closest_dirt = [dirt[0], dirt[1]]

            min_new_dist = 10000
            best_move = ""

            # prevent vacuumfrom going back the same way it came if it can go elsewhere
            if(len(valid_moves) == 1):
                pass
            # we keep track of previous moves using nummbers of different signs to indicate direction
            elif(self.prev_move == 1 and "D" in valid_moves):
                valid_moves.remove("D")
            elif(self.prev_move == -1 and "U" in valid_moves):
                valid_moves.remove("U")
            elif(self.prev_move == 2 and "L" in valid_moves):
                valid_moves.remove("L")
            elif(self.prev_move == -2 and "R" in valid_moves):
                valid_moves.remove("R")
            else:
                pass

            # evaluate distance to closest dirt from each valid moves
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

                if(new_dist < min_new_dist): # chose move that minimizes distance
                    min_new_dist = new_dist
                    best_move = move
                    next_pos = new_pos

            if(next_pos is None):
                return;

            # prevent vacuum from getting stuck behind border in endless loop if dirt is directly behind it
            rel_pos = self.get_relative_position(next_pos, closest_dirt)
            next_valid_moves = self.get_moves_at_pos(next_pos)
            case_a = True if (min_new_dist == 1 and rel_pos[1] == "R" and not "R" in next_valid_moves) else False
            case_b = True if (min_new_dist == 1 and rel_pos[1] == "L" and not "L" in next_valid_moves) else False
            case_c = True if (min_new_dist == 1 and rel_pos[0] == "U" and not "U" in next_valid_moves) else False
            case_d = True if (min_new_dist == 1 and rel_pos[0] == "D" and not "D" in next_valid_moves) else False

            # if vacuum might get stuck, remove best move and go with safe sub optimal move
            if(case_a or case_b or case_c or case_d and len(valid_moves) > 1 and best_move in valid_moves):
                valid_moves.remove(best_move)
                # print("trying to escape")

            min_new_dist = 10000
            second_min = 10000
            second_best = None

            for move in valid_moves:  # re-evaluate moves if best option has been removed
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

                if(new_dist < min_new_dist):  # get best move and second best move
                    second_min = min_new_dist
                    second_best = best_move

                    min_new_dist = new_dist
                    best_move = move
                    next_pos = new_pos

                elif(new_dist < second_min and new_dist != min_new_dist):  # second best move
                    second_min = new_dist
                    second_best = move

            if(second_min == 10000):  # if second best move does not exist
                second_best = best_move

            # map best move to number
            if(best_move == "U"):
                x = 1
            elif(best_move == "D"):
                x = -1
            elif(best_move == "R"):
                x = 2
            else:
                x = -2

            # check if vacuum is going in a loop
            if(x == self.prev_prev_prev_prev_move and self.prev_move == -self.prev_prev_prev_move and self.prev_prev_move == -self.prev_prev_prev_prev_move and not self.loop):
                # print("making second best move")
                best_move = second_best  # if in a loop we go with the second best move to exit loop

            # move one step if the right direction
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
        else:  # no dirt left to chase
            pass
