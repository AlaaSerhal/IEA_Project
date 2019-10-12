class tile:
    def __init__(self, has_dirt, up_border, down_border, left_border, right_border):
        self.dirt = has_dirt
        self.vacuum = False
        self.left_border = left_border
        self.right_border = right_border
        self.down_border = down_border
        self.up_border = up_border

    def dirty(self):
        self.dirt = True

    def set_vacuum(self, has_vacuum):
        self.vacuum = has_vacuum

    def set_borders(self, up, down, left, right):
        self.left_border = left
        self.right_border = right
        self.down_border = down
        self.up_border = up
        return has_borders()

    def clean(self):
        if(self.vacuum and self.dirt):
            self.dirt = False
            return "success"
        elif(self.vacuum and not self.dirt):
            return "success"
        else:
            raise Exception("Cannot clean without vacuum")

    def has_dirt(self):
        return self.has_dirt

    def has_vacuum(self):
        return self.vacuum

    def has_borders(self);
        return [self.up_border, self.down_border, self.left_border, self.right_border]
