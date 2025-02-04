import pygame
import GameConst
from Jewelry import Jewelry


class Shape:
    def __init__(self):
        self.white = False
        self.jewelrys = [Jewelry() for _ in range(3)]
        self.init()

    def init(self):
        # 修正对 Jewelry 实例的行位置
        self.jewelrys[0] = Jewelry()
        self.jewelrys[1] = Jewelry()
        self.jewelrys[2] = Jewelry()

        # 设置合理初始位置，防止溢出
        self.jewelrys[0].set_row(0)  # 第一块珠宝设置到第一行
        self.jewelrys[1].set_row(1)  # 第二块珠宝设置到第二行
        self.jewelrys[2].set_row(2)  # 第三块珠宝设置到第三行

        # 随机初始颜色
        for jewelry in self.jewelrys:
            jewelry.set_color(GameConst.next_color())  # 随机分配颜色
            jewelry.set_empty(False)  # 设置为非空

    def get_jewelrys(self):
        return self.jewelrys

    def set_jewelrys(self, jewelrys):
        self.jewelrys = jewelrys

    def left(self):
        for jewelry in self.jewelrys:
            if jewelry.get_col() > 0:
                jewelry.left()

    def right(self):
        for jewelry in self.jewelrys:
            if jewelry.get_col() < 5:
                jewelry.right()

    # 交换颜色
    def up(self):
        color = self.jewelrys[2].get_color()
        self.jewelrys[2].set_color(self.jewelrys[1].get_color())
        self.jewelrys[1].set_color(self.jewelrys[0].get_color())
        self.jewelrys[0].set_color(color)

    def down(self):
        color = self.jewelrys[0].get_color()
        self.jewelrys[0].set_color(self.jewelrys[1].get_color())
        self.jewelrys[1].set_color(self.jewelrys[2].get_color())
        self.jewelrys[2].set_color(color)

    @staticmethod
    def next_shape():
        shape = Shape()  # 创建新形状
        for jewelry in shape.get_jewelrys():
            color = GameConst.next_color()  # 随机颜色
            jewelry.set_color(color)
            jewelry.set_empty(False)
            #print(f"Set jewelry color to: {color}")  # 调试信息
        return shape  # 确认返回的是 Shape 对象

    @staticmethod
    def white_shape():
        shape = Shape()
        for jewelry in shape.get_jewelrys():
            jewelry.set_color(pygame.Color('white'))
            jewelry.set_white(True)
        return shape

    def is_white(self):
        return self.white

    def set_white(self, white):
        self.white = white
