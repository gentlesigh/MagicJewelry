import pygame
import sys
import threading
import ctypes
from PyQt5.QtWidgets import QApplication
import GameConst
from LoginModule import LoginWindow
from CenterPanel import CenterPanel

def set_input_language_to_english():
        """ 使用 Windows API 切换输入法到英文 """
        HWND = ctypes.windll.user32.GetForegroundWindow()  # 获取当前前台窗口句柄
        LANG = 0x0409  # 英文键盘布局的语言标识符
        HKL = ctypes.windll.user32.LoadKeyboardLayoutW(hex(LANG), 1)  # 加载英文键盘布局
        ctypes.windll.user32.SendMessageW(HWND, 0x0050, 0, HKL)  # 0x0050 为 WM_INPUTLANGCHANGEREQUEST 消息切换语言布局
        print("输入法已切换到英文")

def bring_pygame_window_to_foreground():
    """将 Pygame 窗口移至前台"""
    hwnd = ctypes.windll.user32.GetForegroundWindow()  # 获取当前的前台窗口句柄
    pygame_hwnd = pygame.display.get_wm_info()["window"]  # 获取 Pygame 窗口的句柄
    if hwnd != pygame_hwnd:
        ctypes.windll.user32.SetForegroundWindow(pygame_hwnd)  # 将 Pygame 窗口设置为前台窗口


# 初始化 Pygame
pygame.init()

if __name__ == "__main__":
    set_input_language_to_english()  # 初始化时强制切换为英文输入法

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

    # 显示背景图片（修改部分）
    background_image = GameConst.background
    if background_image:  # 确保背景图片加载成功
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))  # 如果背景图片加载失败，使用黑色填充

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
# 将 Pygame 窗口前置
bring_pygame_window_to_foreground()
# 设置输入法为英文
set_input_language_to_english()
# 主循环
while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif center_panel and game_state in {"single", "multi"}:
            center_panel.key_pressed(event)  # 将键盘事件传递给 CenterPanel
            menu_signal = center_panel.handle_mouse_event(event)  # 处理鼠标事件
            if menu_signal == "start":
                game_state = "start"
                center_panel = None  # 清空当前游戏面板
        elif game_state == "start" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            single_game_rect, multi_game_rect, login_game_rect = draw_start_screen()
            if single_game_rect.collidepoint(mouse_pos):
                game_state = "single"
                center_panel = CenterPanel(screen=screen,
                                           get_user_info=lambda: logged_in_user if is_logged_in else None)
            elif multi_game_rect.collidepoint(mouse_pos):
                if is_logged_in:
                    game_state = "multi"
                    center_panel = CenterPanel(screen=screen,
                                               get_user_info=lambda: logged_in_user if is_logged_in else None)
                else:
                    print("请先登录！")
            elif login_game_rect.collidepoint(mouse_pos):
                threading.Thread(target=run_login_window, daemon=True).start()

    # 渲染逻辑
    if game_state == "start":
        draw_start_screen()
    elif game_state in {"single", "multi"}:
        if center_panel:
            center_panel.paint()

    pygame.display.flip()


pygame.quit()
sys.exit()
