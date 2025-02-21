import pygame

class Jewelry:
    WIDTH = 30
    LEFT = 300
    TOP = 50

    def __init__(self):
        self.white = False
        self.inited = False
        self.empty = False
        self.row = 0
        self.col = 2
        self.color = pygame.Color('black')  # 默认颜色
        self.x = self.LEFT + self.col * self.WIDTH
        self.y = self.TOP + self.row * self.WIDTH

    @staticmethod
    def empty_jewelry(row, col):
        jewelry = Jewelry()
        jewelry.set_row(row)
        jewelry.set_col(col)
        jewelry.set_empty(True)
        jewelry.set_color(pygame.Color('black'))
        jewelry.set_white(False)
        return jewelry

    def is_white(self):
        return self.white

    def set_white(self, white):
        self.white = white

    def get_row(self):
        return self.row

    def set_row(self, row):
        self.row = row
        self.y = self.TOP + row * self.WIDTH

    def get_col(self):
        return self.col

    def set_col(self, col):
        self.col = col
        self.x = self.LEFT + col * self.WIDTH

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color
        print(f"Jewelry color set to: {self.color}")  # 调试信息

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

    def is_inited(self):
        return self.inited

    def set_inited(self, inited):
        self.inited = inited

    def is_empty(self):
        return self.empty

    def set_empty(self, empty):
        self.empty = empty

    def left(self):
        self.col -= 1
        self.x -= self.WIDTH

    def right(self):
        self.col += 1
        self.x += self.WIDTH