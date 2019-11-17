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
        self.prev_prev_prev_move = None
        self.prev_prev_prev_prev_move = None
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
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
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
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
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
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
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
            self.prev_prev_prev_prev_move = self.prev_prev_prev_move
            self.prev_prev_prev_move = self.prev_prev_move
            self.prev_prev_move = self.prev_move
            self.prev_move = -2
        else:
            raise Exception("Invalid move! Cannot move up from current position.")

    def get_moves_at_pos(self, pos):
        moves = []
        tile = self.room.get_array()[pos[0]][pos[1]]
        if(not tile.has_up_border()):
            moves.append("U")
        if(not tile.has_left_border()):
            moves.append("L")
        if(not tile.has_down_border()):
            moves.append("D")
        if(not tile.has_right_border()):
            moves.append("R")
        return moves

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

    def get_relative_position(self, src, dst):
        src_row = src[0]
        src_col = src[1]
        dst_row = dst[0]
        dst_col = dst[1]

        pos = []

        if(dst_row > src_row):
            pos.append("D")
        elif(dst_row < src_row):
            pos.append("U")
        else:
            pos.append("E")

        if(dst_col > src_col):
            pos.append("R")
        elif(dst_col < src_col):
            pos.append("L")
        else:
            pos.append("E")

        return pos


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

        if(len(valid_moves) == 1):
            pass
        elif(self.prev_move == 1):
            valid_moves.remove("D")
        elif(self.prev_move == -1):
            valid_moves.remove("U")
        elif(self.prev_move == 2):
            valid_moves.remove("L")
        elif(self.prev_move == -2):
            valid_moves.remove("R")
        else:
            pass

        # dict = {}
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
            # dict[new_dist] = move

            if(new_dist < min_new_dist):
                min_new_dist = new_dist
                best_move = move
                next_pos = new_pos

        # sorted_dict = sorted(dict.items(), key=operator.itemgetter(0))
        # best_move = sorted_dict[0][1]

        rel_pos = self.get_relative_position(next_pos, closest_dirt)
        next_valid_moves = self.get_moves_at_pos(next_pos)
        case_a = True if (min_new_dist == 1 and rel_pos[1] == "R" and not "R" in next_valid_moves) else False
        case_b = True if (min_new_dist == 1 and rel_pos[1] == "L" and not "L" in next_valid_moves) else False
        case_c = True if (min_new_dist == 1 and rel_pos[0] == "U" and not "U" in next_valid_moves) else False
        case_d = True if (min_new_dist == 1 and rel_pos[0] == "D" and not "D" in next_valid_moves) else False

        if(case_a or case_b or case_c or case_d and len(valid_moves) > 1):
            valid_moves.remove(best_move)
            print("trying to escape")

        min_new_dist = 10000
        second_min = 10000

        second_best = None
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
            # dict[new_dist] = move

            if(new_dist < min_new_dist):
                second_min = min_new_dist
                second_best = best_move

                min_new_dist = new_dist
                best_move = move
                next_pos = new_pos

            elif(new_dist < second_min and new_dist != min_new_dist):
                second_min = new_dist
                second_best = move

        if(second_min == 10000):
            second_best = best_move
        # print("best move: ", best_move)
        # print("second best move: ", second_best)
        if(best_move == "U"):
            x = 1
        elif(best_move == "D"):
            x = -1
        elif(best_move == "R"):
            x = 2
        else:
            x = -2

        if(x == self.prev_prev_prev_prev_move and self.prev_move == -self.prev_prev_prev_move and self.prev_prev_move == -self.prev_prev_prev_prev_move and not self.loop):
            print("backtracking...")
            print("making second best move")
            best_move = second_best
            # self.loop = True
            # go_back = self.prev_prev_prev_move
            # if(go_back == 1):
            #     best_move = "D"
            # elif(go_back == -1):
            #     best_move == "U"
            # elif(go_back == 2):
            #     best_move = "L"
            # elif(go_back == -2):
            #     best_move == "R"
            # else:
            #     pass
        # elif(self.loop):
        #     print("making second best move")
        #     self.loop = False
            # best_move = second_best



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
