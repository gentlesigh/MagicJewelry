import math
import threading
import pygame
from pygame.key import key_code
import GameConst
from Jewelry import Jewelry
from Shape import Shape
from CalcUtil import CalcUtil

class CenterPanel():
    def __init__(self, screen, get_user_info=None):
        self.state = 0
        self.fail = False
        self.jewelry_count = 0  # 初始化珠宝数量
        # Jewelry 是一个假想的类，在此处你需要定义或导入它
        self.all_jewelry = [[None for _ in range(GameConst.All_Rows())] for _ in range(GameConst.All_Cols())]
        self.screen = screen  # 显示的屏幕
        self.get_user_info = get_user_info  # 用于获取当前用户信息的回调函数
        self.score = 0
        self.level = 0
        self.jewelry = 0
        self.jel_cnt = 0
        self.speed_count = 0
        self.check_times = 0
        self.cur_remove_cnt = 0
        self.curr_shape = Shape.next_shape()  # 确保初始化的当前形状有颜色
        self.next_shape = Shape.next_shape()  # 生成下一个形状 # Shape 也需要定义或导入
        self.color = (0, 0, 0)  # 背景颜色为黑色
        self.delay = 1000
        self.timer = pygame.time.Clock()
        self.next_shape = Shape.next_shape()  # Assumes you have a Shape class with a next_shape method
        # 初始化所有方块
        self.init_all_square()
        # CenterPanel.py 中修复音乐加载部分
        try:
            pygame.mixer.init()
            music_path = GameConst.get_music(0)  # 获取第一个音乐文件路径
            if music_path:
                pygame.mixer.music.load(music_path)  # 加载音乐
                pygame.mixer.music.play(-1)  # 循环播放音乐
            else:
                print("未找到音乐文件")
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")

    def can_drop(self, shape):
        """
        判断当前形状是否可以继续下落
        """
        for jewelry in shape.get_jewelrys():  # 遍历当前形状的每块宝石
            next_row = jewelry.get_row() + 1  # 预测下一步的行位置
            col = jewelry.get_col()  # 当前列

            # 如果超出网格底部，则返回 False
            if next_row >= GameConst.All_Rows():
                return False

            # 如果目标位置已被占用，则返回 False
            if self.all_jewelry[col][next_row] is not None and not self.all_jewelry[col][next_row].is_empty():
                return False

        return True  # 如果所有珠宝位置都有效，则可以继续下落

    def timer_event(self):    # 计时器事件
        # 在这里定义计时器触发时的行为
        print("Timer event triggered")
        self.timer = threading.Timer(self.delay / 1000, self.timer_event)
        self.timer.start()

    def init_all_square(self):    # 初始化所有方块
        for i in range(len(self.all_jewelry)):
            for k in range(len(self.all_jewelry[i])):
                jewelry = Jewelry()
                jewelry.set_row(k)
                jewelry.set_col(i)
                jewelry.set_empty(True)
                if not jewelry.is_empty():  # 确保只对空块操作
                    jewelry.set_color(pygame.Color('black'))    # 使用 Pygame 的 Color 类
                self.all_jewelry[i][k] = jewelry

    def paint(self):  # 绘制游戏界面
        # 绘制背景
        background_image = GameConst.background
        if background_image:
            self.screen.blit(background_image, (0, 0))  # 绘制背景图像
        else:
            self.screen.fill((0, 0, 0))  # 如果背景为空，则填充为黑色

        # 绘制暂停状态
        if self.state == 2:  # 如果游戏处于暂停状态
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Pause", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))  # 将暂停文字绘制到屏幕
            return  # 返回，不继续绘制

        # 绘制 "NEXT" 提示文字
        font = pygame.font.SysFont("微软雅黑", 18, bold=True)
        text = font.render("NEXT", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

        # 类型保护：检查 self.next_shape
        if not isinstance(self.next_shape, Shape):
            raise TypeError(f"next_shape 不是有效的 Shape 实例，而是 {type(self.next_shape)}")

        # 绘制下一个形状
        for jewelry in self.next_shape.get_jewelrys():
            x_offset = 50  # 设置 "NEXT" 提示右侧的偏移量
            y_offset = 80  # 设置 "NEXT" 提示下侧的偏移量
            x = x_offset + jewelry.get_col() * Jewelry.WIDTH
            y = y_offset + jewelry.get_row() * Jewelry.WIDTH
            pygame.draw.rect(self.screen, jewelry.get_color(), (x, y, Jewelry.WIDTH, Jewelry.WIDTH))

        # 绘制主游戏界面
        if not self.fail:  # 游戏未失败时绘制游戏状态
            self.draw_all_jewelry()
        else:  # 显示游戏结束文字
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Over", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))  # 显示 "Game Over"
            return  # 游戏结束后不再继续绘制

        # 绘制蓝色下划线
        for i in range(GameConst.ALL_COLS):
            for j in range(GameConst.ALL_ROWS):
                pygame.draw.line(self.screen, (0, 0, 255), (300 + i * 30, 50 + (j + 1) * 30),
                (300 + (i + 1) * 30 - 2, 50 + (j + 1) * 30))

        # 类型保护：检查 self.curr_shape
        if not isinstance(self.curr_shape, Shape):
            raise TypeError(f"curr_shape 不是有效的 Shape 实例，而是 {type(self.curr_shape)}")

        # 控制延迟下落
        current_time = pygame.time.get_ticks()  # 获取当前时间（毫秒）
        if current_time - self.speed_count >= self.delay:  # 检查是否超过延迟时间
            can_drop = self.can_drop(self.curr_shape)  # 检查当前形状能否下落
            if can_drop:  # 如果可以下落
                for jewelry in self.curr_shape.get_jewelrys():
                    jewelry.set_row(jewelry.get_row() + 1)  # 更新行号（下落）
            else:  # 无法下落时，固定当前形状，并生成新形状
                self.place_square(self.curr_shape)  # 固定到网格中
                self.curr_shape = Shape.next_shape()  # 换成新形状
            self.speed_count = current_time  # 重置计时器

        # 绘制当前形状
        for jewelry in self.curr_shape.get_jewelrys():
            x = Jewelry.LEFT + jewelry.get_col() * Jewelry.WIDTH  # 按列计算横向位置
            y = Jewelry.TOP + jewelry.get_row() * Jewelry.WIDTH  # 按行计算纵向位置
            pygame.draw.rect(self.screen, jewelry.get_color(), (x, y, Jewelry.WIDTH, Jewelry.WIDTH))

        # 绘制主游戏网格
        self.draw_all_jewelry()

        # 绘制游戏的分数和数据
        self.draw_data()

        # 获取用户信息（如果已登录）
        if self.get_user_info:
            user_info = self.get_user_info()  # 返回用户信息字典
            if user_info and "nickname" in user_info:
                font = pygame.font.SysFont("微软雅黑", 24, bold=True)
                user_info_text = font.render(f"current user: {user_info['nickname']}", True, (255, 255, 255))
                self.screen.blit(user_info_text, (10, self.screen.get_height() - 40))

    def draw_all_jewelry(self):
        for i in range(len(self.all_jewelry)):
            for k in range(len(self.all_jewelry[i])):
                jewelry = self.all_jewelry[i][k]
                if not jewelry.is_empty():
                    pygame.draw.rect(self.screen, jewelry.get_color(),
                                     (jewelry.get_x(), jewelry.get_y(), Jewelry.WIDTH, Jewelry.WIDTH))

    def draw_data(self):
        # 设置字体
        font = pygame.font.SysFont(None, 36)  # 使用默认字体，大小为36

        # 设置文本颜色为黑色
        color = pygame.Color('black')

        # 绘制数据
        score_text = font.render(f"SCORE: {self.score}", True, color)
        jewelry_text = font.render(f"JEWELRY: {self.jewelry_count}", True, color)
        level_text = font.render(f"LEVEL: {self.level}", True, color)

        # 在屏幕上绘制文本
        self.screen.blit(score_text, (600, 50))
        self.screen.blit(jewelry_text, (600, 100))
        self.screen.blit(level_text, (600, 150))

    def place_square(self, shape):
        """放置方块到游戏区域"""
        self.check_times = 0

        white = shape.is_white()
        if not white:
            # 检查是否超出第一行
            for cur in shape.get_jewelrys():
                if cur.get_row() < 0:
                    self.fail = True
                    # 停止计时器逻辑
                    self.timer.tick(60)
                    return

            # 将方块放置到游戏区域
            for cur in shape.get_jewelrys():
                self.all_jewelry[cur.get_col()][cur.get_row()] = cur

            # 调用消除逻辑
            self.remove(shape)

        else:
            # 检查是否超出第一行
            for cur in shape.get_jewelrys():
                if cur.get_row() < 0:
                    self.fail = True
                    self.timer.tick(0)  # 停止计时器
                    break

            # 获取需要变化的方块并进行处理
            jewelry = self.get_change_jewelry(shape.get_jewelrys()[0])
            if jewelry is not None:
                for i in range(6):  # 假设有 6 列
                    for j in range(15):  # 假设有 15 行
                        c = self.all_jewelry[i][j]
                        if c and jewelry.get_color() == c.get_color():
                            self.check_times += 1
                            self.remove(c)

        # 更新当前形状和下一个形状
        self.curr_shape = self.next_shape  # 将下一个形状设置为当前形状
        self.next_shape = Shape.next_shape()  # 生成新的下一个形状
        self.check_fail(self.curr_shape)
        # 调整时间间隔
        self.delay = max(100, 1000 - 3 * ((self.level + 1) % 256))  # 确保时间间隔不低于100ms
        self.timer.tick(self.delay)  # 使用 Pygame 的计时逻辑
        # 调用检查失败逻辑


    def remove(self, target):
        """
        移除单个珠宝块或整形状，根据输入参数的类型决定操作。
        - 如果 target 是单个珠宝块，则只处理这个珠宝块。
        - 如果 target 是形状，则进行形状及多方向的消除判定。
        """
        if isinstance(target, Jewelry):  # 处理单个珠宝块
            target.set_empty(True)
            target.set_color(pygame.Color('black'))  # 将颜色设置为黑（空块）
            #print(f"Removed single jewelry at ({target.get_row()}, {target.get_col()})")

        elif isinstance(target, Shape):  # 处理整个形状
            for jewelry in target.get_jewelrys():
                col, row = jewelry.get_col(), jewelry.get_row()

                # 从当前珠宝扩展检测四个方向
                left = CalcUtil.calc_left(jewelry, self.all_jewelry)
                right = CalcUtil.calc_right(jewelry, self.all_jewelry)
                top = CalcUtil.calc_top(jewelry, self.all_jewelry)
                down = CalcUtil.calc_down(jewelry, self.all_jewelry)
                left_top = CalcUtil.calc_left_top(jewelry, self.all_jewelry)
                right_down = CalcUtil.calc_right_down(jewelry, self.all_jewelry)
                left_down = CalcUtil.calc_left_down(jewelry, self.all_jewelry)
                right_top = CalcUtil.calc_right_top(jewelry, self.all_jewelry)

                # 消除横向连块
                if left + right + 1 >= 3:
                    for c in range(col - left, col + right + 1):
                        self.all_jewelry[c][row].set_empty(True)
                        self.all_jewelry[c][row].set_color(pygame.Color('black'))
                        #print(f"Removed horizontal block at ({row}, {c})")

                # 消除纵向连块
                if top + down + 1 >= 3:
                    for r in range(row - top, row + down + 1):
                        self.all_jewelry[col][r].set_empty(True)
                        self.all_jewelry[col][r].set_color(pygame.Color('black'))
                        #print(f"Removed vertical block at ({r}, {col})")

                # 消除左上-右下对角线
                if left_top + right_down + 1 >= 3:
                    for offset in range(-left_top, right_down + 1):
                        self.all_jewelry[col + offset][row + offset].set_empty(True)
                        self.all_jewelry[col + offset][row + offset].set_color(pygame.Color('black'))
                        #print(f"Removed left-top to right-down diagonal block at ({row + offset}, {col + offset})")

                # 消除左下-右上对角线
                if left_down + right_top + 1 >= 3:
                    for offset in range(-left_down, right_top + 1):
                        self.all_jewelry[col + offset][row - offset].set_empty(True)
                        self.all_jewelry[col + offset][row - offset].set_color(pygame.Color('black'))
                        #print(f"Removed left-down to right-top diagonal block at ({row - offset}, {col + offset})")

            # 触发下落逻辑
            self.fall_jewelry()
            self.remove_cycle()

        else:
            raise TypeError(f"Unexpected type for target: {type(target)}")

    def get_change_jewelry(self, jewelry):
        """获取指定珠宝下一个位置的珠宝对象"""
        row = jewelry.get_row() + 1
        if row >= 15:
            return None
        return self.all_jewelry[jewelry.get_col()][row]

    def action_performed(self):
        """相当于 Java 中的 actionPerformed，用于重绘屏幕"""
        self.repaint()

    def repaint(self):
        """重新绘制屏幕内容"""
        self.screen.fill((255, 255, 255))  # 将屏幕填充为白色
        pygame.display.flip()  # 刷新屏幕显示

    def key_pressed(self, event):
        """
        键盘事件处理逻辑
        使用 event.key 直接获取按键值，修复 key_code 未定义问题
        """
        print(f"Key pressed: {event.key}")

        # Enter 键：开始游戏或恢复暂停状态
        if event.key == pygame.K_RETURN:
            if self.state == 0 or self.state == 2:  # 未启动或暂停状态
                self.timer.tick(self.delay)
                self.state = 1

        # Esc 键：暂停游戏
        elif event.key == pygame.K_ESCAPE:
            # 如果已经失败则不处理
            if self.fail:
                return
            if self.state == 1:  # 游戏运行中，按下暂停
                self.timer.tick(0)  # 停止计时器
                self.repaint()  # 重绘暂停界面
                self.state = 2

        # A 键：向左移动当前形状
        elif event.key == pygame.K_a:
            if self.curr_shape:
                self.curr_shape.left()
                self.repaint()

        # D 键：向右移动当前形状
        elif event.key == pygame.K_d:
            if self.curr_shape:
                self.curr_shape.right()
                self.repaint()

        # S 键：快速下落（加速）
        elif event.key == pygame.K_s:
            self.delay = 100  # 设置快速下落的延迟
            self.speed_count += 1
            self.timer.tick(self.delay)

        # Q 键：向下颜色交换
        elif event.key == pygame.K_q:
            if self.curr_shape:
                self.curr_shape.down()

        # E 键：向上颜色交换
        elif event.key == pygame.K_e:
            if self.curr_shape:
                self.curr_shape.up()

    def remove_cycle(self):
        """
        消除循环逻辑，确保所有符合条件的珠宝都被移除
        """
        to_remove = []  # 存储需要移除的珠宝位置
        for col in range(GameConst.All_Cols()):
            for row in range(GameConst.All_Rows()):
                jewelry = self.all_jewelry[col][row]
                if jewelry.is_empty():
                    continue  # 跳过空块

                # 逐方向检查所有可能消除的条件
                left = CalcUtil.calc_left(jewelry, self.all_jewelry)
                right = CalcUtil.calc_right(jewelry, self.all_jewelry)
                top = CalcUtil.calc_top(jewelry, self.all_jewelry)
                down = CalcUtil.calc_down(jewelry, self.all_jewelry)
                left_top = CalcUtil.calc_left_top(jewelry, self.all_jewelry)
                right_down = CalcUtil.calc_right_down(jewelry, self.all_jewelry)
                left_down = CalcUtil.calc_left_down(jewelry, self.all_jewelry)
                right_top = CalcUtil.calc_right_top(jewelry, self.all_jewelry)

                # 检查消除条件，行/列/对角线均至少 3 连
                if left + right + 1 >= 3:  # 横向
                    to_remove.extend([(col - x, row) for x in range(left)] + [(col + x, row) for x in range(right + 1)])
                if top + down + 1 >= 3:  # 纵向
                    to_remove.extend([(col, row - x) for x in range(top)] + [(col, row + x) for x in range(down + 1)])
                if left_top + right_down + 1 >= 3:  # 左上右下对角线
                    to_remove.extend([(col - x, row - x) for x in range(left_top)] +
                                     [(col + x, row + x) for x in range(right_down + 1)])
                if left_down + right_top + 1 >= 3:  # 左下右上对角线
                    to_remove.extend([(col - x, row + x) for x in range(left_down)] +
                                     [(col + x, row - x) for x in range(right_top + 1)])

        # 遍历并消除需要移除的所有珠宝
        for col, row in to_remove:
            self.all_jewelry[col][row].set_empty(True)
            self.all_jewelry[col][row].set_color(pygame.Color('black'))  # 保持空黑块一致性

        # 触发下落逻辑
        if to_remove:
            self.fall_jewelry()
            self.remove_cycle()  # 再次检测，确保连续消除

    def fall_jewelry(self):
        """
        实现方块向下掉落的功能，同时处理空白填充问题
        """
        remove_cnt = 0

        # 遍历每一列，从底部向顶部检查珠宝
        for col in range(GameConst.All_Cols()):
            for row in range(GameConst.All_Rows() - 1, -1, -1):  # 从底部向上
                cur_block = self.all_jewelry[col][row]
                if cur_block.is_empty():  # 当前是空块
                    # 继续向上寻找一个非空块进行交换
                    for above_row in range(row - 1, -1, -1):  # 遍历上方的元素
                        above_block = self.all_jewelry[col][above_row]
                        if not above_block.is_empty():  # 找到非空方块
                            # 将上方非空块移动到底部，当前块清空
                            cur_block.set_color(above_block.get_color())
                            cur_block.set_empty(False)

                            above_block.set_color(pygame.Color('black'))  # 上方块变为空块
                            above_block.set_empty(True)

                            remove_cnt += 1
                            break
        return remove_cnt

    def check_fail(self, shape):
        """
        检查游戏失败条件：新形状生成位置被占用
        """
        for jewelry in shape.get_jewelrys():
            row = jewelry.get_row()
            col = jewelry.get_col()

            # 检查形状生成位置是否已经被占用或超出顶部范围
            if row < 0 or self.all_jewelry[col][row] is not None and not self.all_jewelry[col][row].is_empty():
                self.fail = True
                print("Game Over")
                return  # 一旦失败，直接返回，避免多余操作

        self.fail = False  # 如果没有触发失败条件，则游戏继续