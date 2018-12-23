class Block:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.visible = True

    def get_width(self):
        self.width
    def get_height(self):
        self.height
    def disappear(self):
        self.visible = False
    def reappear(self):
        self.visible = True

