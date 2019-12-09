import globals
class tile:  # class defines one tile
    def __init__(self, x_pos, y_pos):
        self.probability = 0
        self.dirt = False
        self.vacuum = None
        self.left_border = False
        self.right_border = False
        self.down_border = False
        self.up_border = False
        self.x_pos = x_pos
        self.y_pos = y_pos

    def set_proba(self, proba):
        self.probability = proba

    def get_proba(self):
        return int(self.probability)

    def set_x_pos(self, x_pos):
        self.x_pos = x_pos

    def set_y_pos(self,y_pos):
        self.y_pos = y_pos

    def set_vacuum(self):
        self.vacuum = True

    def remove_vacuum(self):
        self.vacuum = None

    def set_borders(self, up, down, left, right):
        self.left_border = left
        self.right_border = right
        self.down_border = down
        self.up_border = up
        return self.has_borders()

    def set_up_border(self):
        self.up_border = True

    def set_down_border(self):
        self.down_border = True

    def set_left_border(self):
        self.left_border = True

    def set_right_border(self):
        self.right_border = True

    def dirty(self):
        self.dirt = True

    def set_dirty(self,hasDirt):
        self.dirt = hasDirt
        if(not self.dirty()):
            globals.globals.nb_added_dirt +=1

    def clean(self):
        if(self.vacuum and self.dirt):
            self.dirt = False
            return "success"
        elif(self.vacuum and not self.dirt):
            return "success"
        else:
            raise Exception("Cannot clean without vacuum")

    def has_dirt(self):
        return self.dirt

    def has_vacuum(self):
        if self.vacuum is None:
            return False
        else:
            return True

    def has_borders(self):
        return [self.up_border, self.down_border, self.left_border, self.right_border]

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def has_up_border(self):
        return self.up_border

    def has_down_border(self):
        return self.down_border

    def has_left_border(self):
        return self.left_border

    def has_right_border(self):
        return self.right_border

    def get_vacuum(self):
        return self.vacuum

    def get_string_id(self):
        return "y" + str(self.x_pos) + "x" + str(self.y_pos)

    def get_data_string(self):
        return "Pos:" + self.get_string_id() + " - Borders" + str(self.has_borders())
