import math
import threading
import pygame
import GameConst
from Jewelry import Jewelry
from Shape import Shape
from CalcUtil import CalcUtil

def CenterPanel():
    def __init__(self):
        self.state = 0
        self.fail = False

        # Jewelry 是一个假想的类，在此处你需要定义或导入它
        self.all_jewelry = [[None for _ in range(GameConst.All_Rows())] for _ in range(GameConst.All_Cols())]

        self.score = 0
        self.level = 0
        self.jewelry = 0
        self.jel_cnt = 0
        self.speed_count = 0
        self.check_times = 0
        self.cur_remove_cnt = 0

        self.next_shape = None
        self.curr_shape = Shape()  # Shape 也需要定义或导入

        self.delay = 1000
        self.timer = threading.Timer(self.delay / 1000, self.timer_event)
        # Set up shape
        self.next_shape = Shape.next_shape()  # Assumes you have a Shape class with a next_shape method

        # Initialize all squares or other necessary components
        self.init_all_square()

        # Load and play music
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(GameConst.music0)  # GameConst.music0 should be the path to your music file
            pygame.mixer.music.play(-1)  # Play the music indefinitely
        except pygame.error as e:
            print(f"Error loading or playing music: {e}")

    def timer_event(self):
        # 在这里定义计时器触发时的行为
        print("Timer event triggered")
        self.timer = threading.Timer(self.delay / 1000, self.timer_event)
        self.timer.start()

    def init_all_square(self):
        for i in range(len(self.all_jewelry)):
            for k in range(len(self.all_jewelry[i])):
                jewelry = Jewelry()
                jewelry.set_row(k)
                jewelry.set_col(i)
                jewelry.set_empty(True)
                jewelry.set_color(pygame.Color('black'))  # 使用 Pygame 的 Color 类
                self.all_jewelry[i][k] = jewelry

    def paint(self):
        # 绘制背景
        background_image = GameConst.BACKGROUND.get_image()
        self.screen.blit(background_image, (0, 0))

        # 提示暂停信息
        if self.state == 2:
            font = pygame.font.SysFont("微软雅黑", 72, bold=True)
            text = font.render("Game Pause", True, (255, 255, 255))
            self.screen.blit(text, (200, 300))
            return

        # 绘制下一个形状的提示
        font = pygame.font.SysFont("微软雅黑", 18, bold=True)
        text = font.render("NEXT", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

        # 画下一组方块
        for i, jewelry in enumerate(self.next_shape.get_jewelrys()):
            pygame.draw.rect(self.screen, jewelry.get_color(),
                             (Jewelry.TOP, 80 + i * Jewelry.WIDTH, Jewelry.WIDTH, Jewelry.WIDTH))

        # 画游戏主界面
        pygame.draw.rect(self.screen, (0, 0, 0), (300, Jewelry.TOP, 180, 450), 1)

        # 画蓝色的下划线
        for i in range(GameConst.ALLCOLS):
            for j in range(GameConst.ALLROWS):
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

        # 是否可以下落
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
                    self.timer.tick(0)  # 假设 tick(0) 类似于停止
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
        self.timer.tick(self.delay)  # 设置 timer 的延迟

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
        """处理按键按下事件"""
        key_code = event.key

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
                print(f"row {cnt}")
                for col in range(jewelry.get_col() - left, jewelry.get_col() + right + 1):
                    self.all_jewelry[col][jewelry.get_row()].set_empty(True)
                self.jelewey += cnt
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
                self.jelewey += cnt
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
                self.jelewey += cnt
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
                self.jelewey += cnt
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
                    self.jelewey += cnt
                    self.jel_cnt += cnt

                # 列消除逻辑
                top = CalcUtil.calc_top(cur, self.all_jewelry)
                down = CalcUtil.calc_down(cur, self.all_jewelry)
                cnt = top + down + 1
                if cnt >= 3:
                    print(f"col {cnt}")
                    for row in range(cur.get_row() - top, cur.get_row() + down + 1):
                        self.all_jewelry[cur.get_col()][row].set_empty(True)
                    self.jelewey += cnt
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
                    self.jelewey += cnt
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
                    self.jelewey += cnt
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