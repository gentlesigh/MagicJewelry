import pygame
import sys
from CenterPanel import CenterPanel

# 初始化 Pygame
pygame.init()

# 定义窗口尺寸
WIDTH, HEIGHT = 800, 600

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Magic Jewelry')

# 初始化中心面板并绑定 `screen`
try:
    center_panel = CenterPanel()
    assert center_panel is not None, "CenterPanel 实例化失败，导致 center_panel 为 None"
    center_panel.screen = screen  # 绑定 screen 到 center_panel
except Exception as e:
    print(f"实例化 CenterPanel 时发生错误：{e}")
    pygame.quit()
    sys.exit(1)

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # 处理按键事件
            center_panel.key_pressed(event)

    # 绘制中心面板内容
    center_panel.paint()

    # 更新显示内容
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()

