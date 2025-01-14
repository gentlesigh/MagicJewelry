import math
import threading
import pygame
from pygame.key import key_code

import GameConst
from Jewelry import Jewelry
from Shape import Shape
from CalcUtil import CalcUtil

class CenterPanel():
    def __init__(self):
        self.state = 0
        self.fail = False
        self.jewelry_count = 0  # 初始化珠宝数量
        # Jewelry 是一个假想的类，在此处你需要定义或导入它
        self.all_jewelry = [[None for _ in range(GameConst.All_Rows())] for _ in range(GameConst.All_Cols())]

        self.score = 0
        self.level = 0
        self.jewelry = 0
        self.jel_cnt = 0
        self.speed_count = 0
        self.check_times = 0
        self.cur_remove_cnt = 0
        self.screen = None
        self.next_shape = None
        self.curr_shape = Shape()  # Shape 也需要定义或导入
        self.color = (0, 0, 0)  # 背景颜色为黑色
        self.delay = 1000
        self.timer = pygame.time.Clock()
        self.next_shape = Shape.next_shape()  # Assumes you have a Shape class with a next_shape method

        # Initialize all squares or other necessary components
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

    def place_square(self, shape):
        """
        将当前形状固定在网格中，并更新网格状态
        """
        for jewelry in shape.get_jewelrys():
            row = jewelry.get_row()
            col = jewelry.get_col()

            # 放置当前形状到网格中
            self.all_jewelry[col][row] = jewelry

        # 调用消除逻辑检查是否有需要消除的行/列
        self.remove()

        # 检查游戏失败状态
        self.check_fail(shape)

        # 切换到下一个形状
        self.curr_shape = self.next_shape
        self.next_shape = Shape.next_shape()

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
                jewelry.set_color(pygame.Color('black'))  # 使用 Pygame 的 Color 类
                self.all_jewelry[i][k] = jewelry

    def paint(self):    # 绘制游戏界面
        # 绘制背景
        background_image = GameConst.background
        if background_image:
            self.screen.blit(background_image, (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # 绘制暂停状态
        if self.state == 2:
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Pause", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))
            return

        # 绘制 "NEXT" 提示文字
        font = pygame.font.SysFont("微软雅黑", 18, bold=True)
        text = font.render("NEXT", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

        # 绘制下一个形状
        for i, jewelry in enumerate(self.next_shape.get_jewelrys()):
            pygame.draw.rect(self.screen, jewelry.get_color(),
                             (Jewelry.LEFT + i * Jewelry.WIDTH, 80, Jewelry.WIDTH, Jewelry.WIDTH))

        # 绘制主游戏界面
        if not self.fail:  # 游戏未失败时绘制游戏状态
            self.draw_all_jewelry()
        else:  # 显示游戏结束文字
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Over", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))
        # 绘制蓝色下划线
        for i in range(GameConst.ALL_COLS):
            for j in range(GameConst.ALL_ROWS):
                pygame.draw.line(self.screen, (0, 0, 255), (300 + i * 30, 50 + (j + 1) * 30),
                                 (300 + (i + 1) * 30 - 2, 50 + (j + 1) * 30))

        if self.fail:
            self.draw_all_jewelry()
            self.draw_data()
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Over", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))
            return

        jewelry_one = self.curr_shape.get_jewelrys()[0]
        if jewelry_one.get_row() == 1:
            if self.jel_cnt > GameConst.REMOVE_CNT:
                pass
            else:
                self.next_shape = Shape.next_shape()
        elif jewelry_one.get_row() == 0:
            for i, jewelry in enumerate(self.curr_shape.get_jewelrys()):
                jewelry.set_color(self.next_shape.get_jewelrys()[2 - i].get_color())

        # 检查是否可以下落
        can_drop = self.can_drop(self.curr_shape)

        if can_drop:
            for jewelry in self.curr_shape.get_jewelrys():
                pygame.draw.rect(self.screen, jewelry.get_color(),
                                 (jewelry.get_x(), jewelry.get_y(), Jewelry.WIDTH, Jewelry.WIDTH))
                jewelry.set_row(jewelry.get_row() + 1)
        else:
            self.place_square(self.curr_shape)
            if self.curr_shape.is_white():
                pass

        if not can_drop:
            if self.jel_cnt > GameConst.REMOVE_CNT:
                self.curr_shape = Shape()
                self.curr_shape.set_white(True)
                self.next_shape = Shape.white_shape()
                self.jel_cnt = 0
                self.level += 1
            else:
                self.curr_shape = Shape()
            self.cur_remove_cnt = 0

        self.draw_all_jewelry()
        self.draw_data()

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

        # 调整时间间隔
        self.delay = max(100, 1000 - 3 * ((self.level + 1) % 256))  # 确保时间间隔不低于100ms
        self.timer.tick(self.delay)  # 使用 Pygame 的计时逻辑

    def remove(self, c):
        """消除方块并处理得分、等级逻辑以及音频播放"""
        c.set_empty(True)

        # 调用 fallJewelry 检查是否有方块需要下落
        remove_count = self.fall_jewelry()
        if remove_count > 0:
            self.cur_remove_cnt += remove_count
            self.repaint()  # 调用重新绘制画面
            self.remove_cycle()

        # 计算分数
        self.score += int(math.pow(2, (self.check_times - 1))) * (
                    self.cur_remove_cnt * (100 + self.level * self.speed_count))

        # 计算等级
        if self.jel_cnt > GameConst.REMOVE_CNT:
            music_index = self.level % 8
            try:
                # 播放音乐
                pygame.mixer.init()
                if self.music_clip:
                    pygame.mixer.music.stop()  # 停止当前播放的音乐
                music_index = 0 if music_index + 1 > 7 else music_index + 1
                self.music_clip = self.music_list[music_index]
                pygame.mixer.music.load(self.music_clip)
                pygame.mixer.music.play(-1)  # 循环播放

            except pygame.error as e:
                print(f"音乐播放错误: {e}")

            # 如果等级到达 256，则重置等级并恢复初始延迟
            if self.level % 256 == 0:
                self.level = 0
                self.delay = 1000
                self.timer.tick(self.delay)

    def get_change_jewelry(self, jewelry):
        """获取指定珠宝下一个位置的珠宝对象"""
        row = jewelry.get_row() + 1
        if row >= 15:
            return None
        return self.all_jewelry[jewelry.get_col()][row]

    def action_performed(self):
        """相当于 Java 中的 actionPerformed，用于重绘屏幕"""
        self.repaint()

    def key_typed(self, event):
        """相当于 Java 中的 keyTyped，处理键盘按键事件"""
        pass  # 当前没有实现任何逻辑

    def repaint(self):
        """重新绘制屏幕内容"""
        self.screen.fill((255, 255, 255))  # 将屏幕填充为白色
        pygame.display.flip()  # 刷新屏幕显示

    def key_pressed(self, event):
        # 键盘事件处理逻辑（可自定义）
        print(f"Key pressed: {event.key}")

        if key_code == pygame.K_RETURN:  # 对应 Java 的 KeyEvent.VK_ENTER
            # 未启动和暂停状态可以启动
            if self.state == 0 or self.state == 2:
                self.timer.tick(self.delay)
                self.state = 1

        elif key_code == pygame.K_ESCAPE:  # 对应 Java 的 KeyEvent.VK_ESCAPE
            # 失败状态下按暂停无效
            if self.fail:
                return
            if self.state == 1:
                self.timer.tick(0)  # 停止计时器
                self.repaint()
                self.state = 2

        elif key_code == pygame.K_a:  # 对应 Java 的 KeyEvent.VK_A
            if self.curr_shape:
                self.curr_shape.left()
                self.repaint()

        elif key_code == pygame.K_d:  # 对应 Java 的 KeyEvent.VK_D
            if self.curr_shape:
                self.curr_shape.right()
                self.repaint()

        elif key_code == pygame.K_s:  # 对应 Java 的 KeyEvent.VK_S
            self.delay = 100
            self.speed_count += 1
            self.timer.tick(self.delay)

        elif key_code == pygame.K_q:  # 对应 Java 的 KeyEvent.VK_Q
            if self.curr_shape:
                self.curr_shape.down()

        elif key_code == pygame.K_e:  # 对应 Java 的 KeyEvent.VK_E
            if self.curr_shape:
                self.curr_shape.up()

    def remove(self, shape):
        """移除逻辑，用于消除匹配的方块"""
        self.check_times = 0

        # 遍历当前形状中的所有珠宝
        for jewelry in shape.get_jewelrys():
            self.check_times += 1

            # 行消除逻辑
            left = CalcUtil.calc_left(jewelry, self.all_jewelry)
            right = CalcUtil.calc_right(jewelry, self.all_jewelry)
            cnt = left + right + 1
            if cnt >= 3:
                for col in range(jewelry.get_col() - left, jewelry.get_col() + right + 1):
                    self.all_jewelry[col][jewelry.get_row()].set_empty(True)
                self.jeweley += cnt
                self.jel_cnt += cnt
                self.cur_remove_cnt += cnt

            # 列消除逻辑
            top = CalcUtil.calc_top(jewelry, self.all_jewelry)
            down = CalcUtil.calc_down(jewelry, self.all_jewelry)
            cnt = top + down + 1
            if cnt >= 3:
                print(f"col {cnt}")
                for row in range(jewelry.get_row() - top, jewelry.get_row() + down + 1):
                    self.all_jewelry[jewelry.get_col()][row].set_empty(True)
                self.jewelry += cnt
                self.jel_cnt += cnt
                self.cur_remove_cnt += cnt

            # 左上到右下的对角线消除
            lefttop = CalcUtil.calc_left_top(jewelry, self.all_jewelry)
            rightdown = CalcUtil.calc_right_down(jewelry, self.all_jewelry)
            cnt = lefttop + rightdown + 1
            if cnt >= 3:
                print(f"lefttop {cnt}")
                for row, col in zip(
                        range(jewelry.get_row() - lefttop, jewelry.get_row() + rightdown + 1),
                        range(jewelry.get_col() - lefttop, jewelry.get_col() + rightdown + 1),
                ):
                    self.all_jewelry[col][row].set_empty(True)
                self.jewelry += cnt
                self.jel_cnt += cnt
                self.cur_remove_cnt += cnt

            # 左下到右上的对角线消除
            leftdown = CalcUtil.calc_left_down(jewelry, self.all_jewelry)
            righttop = CalcUtil.calc_right_top(jewelry, self.all_jewelry)
            cnt = leftdown + righttop + 1
            if cnt >= 3:
                print(f"righttop {cnt}")
                for row, col in zip(
                        range(jewelry.get_row() + leftdown, jewelry.get_row() - righttop - 1, -1),
                        range(jewelry.get_col() - leftdown, jewelry.get_col() + righttop + 1),
                ):
                    self.all_jewelry[col][row].set_empty(True)
                self.jewelry += cnt
                self.jel_cnt += cnt
                self.cur_remove_cnt += cnt

        # 触发方块下落逻辑
        remove_count = self.fall_jewelry()
        if remove_count > 0:
            self.cur_remove_cnt += remove_count
            self.repaint()
            self.remove_cycle()

        # 更新分数
        self.score += int(math.pow(2, (self.check_times - 1))) * (
                    self.cur_remove_cnt * (100 + self.level * self.speed_count))

        # 更新等级并切换音乐
        if self.jel_cnt > GameConst.REMOVE_CNT:
            music_index = self.level % 8
            try:
                # 播放下一首音乐
                pygame.mixer.init()
                if self.music_clip:
                    pygame.mixer.music.stop()
                music_index = 0 if music_index + 1 > 7 else music_index + 1
                self.music_clip = self.music_list[music_index]
                pygame.mixer.music.load(self.music_clip)
                pygame.mixer.music.play(-1)  # 循环播放

            except pygame.error as e:
                print(f"音乐播放错误: {e}")

            # 如果等级达到 256，重置等级并恢复初始延迟
            if self.level % 256 == 0:
                self.level = 0
                self.delay = 1000
                self.timer.tick(self.delay)

    def remove_cycle(self):
        """执行消除循环，检查并消除所有满足条件的珠宝，并触发下落逻辑"""
        cur_rm_cnt = 0

        # 遍历所有的珠宝格子
        for i in range(6):  # 假设游戏区域为 6 列
            for j in range(15):  # 假设游戏区域为 15 行
                cur = self.all_jewelry[i][j]

                # 行消除逻辑
                left = CalcUtil.calc_left(cur, self.all_jewelry)
                right = CalcUtil.calc_right(cur, self.all_jewelry)
                cnt = left + right + 1
                if cnt >= 3:
                    print(f"row {cnt}")
                    for col in range(cur.get_col() - left, cur.get_col() + right + 1):
                        self.all_jewelry[col][cur.get_row()].set_empty(True)
                    self.jewelry += cnt
                    self.jel_cnt += cnt

                # 列消除逻辑
                top = CalcUtil.calc_top(cur, self.all_jewelry)
                down = CalcUtil.calc_down(cur, self.all_jewelry)
                cnt = top + down + 1
                if cnt >= 3:
                    print(f"col {cnt}")
                    for row in range(cur.get_row() - top, cur.get_row() + down + 1):
                        self.all_jewelry[cur.get_col()][row].set_empty(True)
                    self.jewelry += cnt
                    self.jel_cnt += cnt

                # 左上到右下的对角线消除
                lefttop = CalcUtil.calc_left_top(cur, self.all_jewelry)
                rightdown = CalcUtil.calc_right_down(cur, self.all_jewelry)
                cnt = lefttop + rightdown + 1
                if cnt >= 3:
                    print(f"lefttop {cnt}")
                    for row, col in zip(
                            range(cur.get_row() - lefttop, cur.get_row() + rightdown + 1),
                            range(cur.get_col() - lefttop, cur.get_col() + rightdown + 1),
                    ):
                        self.all_jewelry[col][row].set_empty(True)
                    self.jewelry += cnt
                    self.jel_cnt += cnt

                # 左下到右上的对角线消除
                leftdown = CalcUtil.calc_left_down(cur, self.all_jewelry)
                righttop = CalcUtil.calc_right_top(cur, self.all_jewelry)
                cnt = leftdown + righttop + 1
                if cnt >= 3:
                    print(f"righttop {cnt}")
                    for row, col in zip(
                            range(cur.get_row() + leftdown, cur.get_row() - righttop - 1, -1),
                            range(cur.get_col() - leftdown, cur.get_col() + righttop + 1),
                    ):
                        self.all_jewelry[col][row].set_empty(True)
                    self.jewelry += cnt
                    self.jel_cnt += cnt

        # 触发珠宝下落逻辑
        remove = self.fall_jewelry()
        if remove > 0:
            print(f"remove: {remove}")
            self.repaint()
            # 多次执行，直到没有可消除的珠宝
            self.remove_cycle()

    def fall_jewelry(self):
        """处理珠宝下落逻辑"""
        remove_cnt = 0

        # 遍历所有列
        for i in range(6):  # 假设游戏区域为 6 列
            # 从每列底部向上遍历
            for k in range(14, 0, -1):  # 假设游戏区域为 15 行，索引从 14 到 0
                jewelry = self.all_jewelry[i][k]
                if jewelry.is_empty():
                    # 向上查找不为空的珠宝
                    for x in range(k - 1, -1, -1):
                        up_jewelry = self.all_jewelry[i][x]
                        if not up_jewelry.is_empty():
                            # 将上方珠宝移动到当前空格位置
                            jewelry.set_color(up_jewelry.get_color())
                            jewelry.set_empty(False)

                            # 重新生成一个新的空格
                            n_jewelry = Jewelry()
                            n_jewelry.set_row(x)
                            n_jewelry.set_col(i)
                            n_jewelry.set_color((0, 0, 0))  # 假设黑色表示空格
                            n_jewelry.set_empty(True)
                            self.all_jewelry[i][x] = n_jewelry

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