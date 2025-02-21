import pygame
import sys
import threading

from PyQt5.QtWidgets import QApplication

from LoginModule import LoginWindow
from CenterPanel import CenterPanel

# 初始化 Pygame
pygame.init()

# 定义窗口尺寸
WIDTH, HEIGHT = 800, 600

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Jewelry")

# 游戏状态变量
game_state = "start"  # 可取值为 'start'（启动界面）、'single'（单人游戏）、'multi'（多人游戏）
center_panel = None  # 游戏主要逻辑面板，仅在进入游戏时初始化

# 加载字体
font = pygame.font.SysFont("微软雅黑", 36)


def run_login_window():
    """运行登录窗口"""
    app = QApplication(sys.argv)
    login_window = LoginWindow()  # 调用独立的登录窗口模块
    login_window.show()
    app.exec_()


def draw_start_screen():
    """绘制启动界面的内容"""
    screen.fill((0, 0, 0))  # 使用黑色背景

    # 标题
    title_text = font.render("Magic Jewelry", True, (255, 255, 255))  # 标题文字
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # 单人游戏按钮
    single_game_text = font.render("Single Player", True, (0, 255, 0))  # 单人游戏文字
    single_game_rect = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
    pygame.draw.rect(screen, (50, 50, 50), single_game_rect)  # 按钮底色
    screen.blit(single_game_text, (WIDTH // 2 - single_game_text.get_width() // 2, 210))

    # 多人游戏
    multi_game_text = font.render("Multiplayer", True, (255, 255, 0))
    multi_game_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, (50, 50, 50), multi_game_rect)  # 按钮底色
    screen.blit(multi_game_text, (WIDTH // 2 - multi_game_text.get_width() // 2, 310))

    return single_game_rect, multi_game_rect


# 主循环
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "start":
            # 获取鼠标点击位置
            mouse_pos = pygame.mouse.get_pos()

            # 检测点击是否在按钮区域
            single_game_rect, multi_game_rect = draw_start_screen()  # 绘制并获取按钮区域
            if single_game_rect.collidepoint(mouse_pos):
                game_state = "single"  # 切换到单人游戏模式
                try:
                    center_panel = CenterPanel()  # 初始化单人游戏逻辑
                    center_panel.screen = screen  # 绑定窗口到 center_panel
                except Exception as e:
                    print(f"初始化游戏时出错: {e}")
                    pygame.quit()
                    sys.exit(1)
            elif multi_game_rect.collidepoint(mouse_pos):
                # 初始化登录界面
                threading.Thread(target=run_login_window, daemon=True).start()

    if game_state == "start":
        # 绘制启动界面
        single_game_rect, multi_game_rect = draw_start_screen()
    elif game_state == "single":
        # 单人游戏逻辑
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                center_panel.key_pressed(event)

        # 更新游戏逻辑
        if center_panel.state == 1:  # 游戏运行
            center_panel.update_logic()

        # 绘制内容
        center_panel.paint()

    # 刷新画面
    pygame.display.flip()

pygame.quit()
sys.exit()
