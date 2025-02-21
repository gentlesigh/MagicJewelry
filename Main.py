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
game_state = "start"  # 可取值为 'start'、'single'、'multi'
center_panel = None  # 游戏逻辑面板的初始值（在需要时动态初始化）
is_logged_in = False  # 登录状态
logged_in_user = {}  # 存储登录用户信息，示例：{"account": "user123", "nickname": "Player1"}

# 加载字体
font = pygame.font.SysFont("微软雅黑", 36)


def run_login_window():
    """启动登录窗口并更新登录状态"""
    global is_logged_in, logged_in_user

    def login_callback(success, user_info=None):
        global is_logged_in, logged_in_user
        if success and user_info:
            is_logged_in = True
            logged_in_user = user_info  # 保存登录用户信息
            print(f"登录成功 - is_logged_in: {is_logged_in}, logged_in_user: {logged_in_user}")
        else:
            print("登录失败 - 用户信息未能识别")

    app = QApplication(sys.argv)
    login_window = LoginWindow(login_callback=login_callback)
    login_window.show()
    app.exec_()


def draw_start_screen():
    """绘制启动界面"""
    global is_logged_in, logged_in_user

    screen.fill((0, 0, 0))  # 使用黑色背景

    # 显示标题
    title_text = font.render("Magic Jewelry", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

    # 单人游戏按钮
    single_game_text = font.render("Single Player", True, (0, 255, 0))
    single_game_rect = pygame.Rect(WIDTH // 2 - 100, 150, 200, 50)
    pygame.draw.rect(screen, (50, 50, 50), single_game_rect)
    screen.blit(single_game_text, (WIDTH // 2 - single_game_text.get_width() // 2, 160))

    # 多人游戏按钮
    multi_game_text = font.render("Multiplayer", True, (255, 255, 0))
    multi_game_rect = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
    pygame.draw.rect(screen, (50, 50, 50), multi_game_rect)
    if not is_logged_in:
        pygame.draw.rect(screen, (100, 100, 100), multi_game_rect)  # 未登录显示灰色
    screen.blit(multi_game_text, (WIDTH // 2 - multi_game_text.get_width() // 2, 260))

    # 登录按钮
    login_text = font.render("Login", True, (0, 0, 255))
    login_game_rect = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)
    pygame.draw.rect(screen, (50, 50, 50), login_game_rect)
    screen.blit(login_text, (WIDTH // 2 - login_text.get_width() // 2, 360))

    # 显示当前已登录的用户信息（左上角）
    if is_logged_in and "nickname" in logged_in_user:
        user_status = f"User: {logged_in_user['nickname']}"  # 显示昵称
        user_text = font.render(user_status, True, (255, 255, 255))
        screen.blit(user_text, (10, 10))  # 左上角位置

    return single_game_rect, multi_game_rect, login_game_rect


# 主循环
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # 事件循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == "start":
            mouse_pos = pygame.mouse.get_pos()
            single_game_rect, multi_game_rect, login_game_rect = draw_start_screen()

            if single_game_rect.collidepoint(mouse_pos):
                game_state = "single"
                try:
                    center_panel = CenterPanel(screen=screen,
                                               get_user_info=lambda: logged_in_user if is_logged_in else None)
                except Exception as e:
                    print(f"初始化游戏时出错: {e}")
                    pygame.quit()
                    sys.exit(1)

            elif multi_game_rect.collidepoint(mouse_pos):
                if is_logged_in:  # 确保用户已登录
                    game_state = "multi"  # 更新游戏状态为多人游戏
                    try:
                        center_panel = CenterPanel(screen=screen,
                                                   get_user_info=lambda: logged_in_user if is_logged_in else None)
                    except Exception as e:
                        print(f"初始化多人游戏时出错: {e}")
                        pygame.quit()
                        sys.exit(1)
                    print(f"进入多人游戏模式 - 当前用户: {logged_in_user}")
                else:
                    print("请先登录！")

            elif login_game_rect.collidepoint(mouse_pos):
                threading.Thread(target=run_login_window, daemon=True).start()

    # 渲染逻辑
    if game_state == "start":
        draw_start_screen()
    elif game_state == "single" or game_state == "multi":
        if center_panel:  # 防止未初始化的调用
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    center_panel.key_pressed(event)
            if center_panel.state == 1:
                center_panel.update_logic()
            center_panel.paint()

    pygame.display.flip()

pygame.quit()
sys.exit()
