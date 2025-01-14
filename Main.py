import pygame
import sys
import GameConst
import CenterPanel
# 初始化 Pygame
pygame.init()

# 定义窗口尺寸
WIDTH, HEIGHT = 800, 600

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Window')
center_panel = CenterPanel.CenterPanel()
# 运行游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 用黑色填充屏幕（可以换成其他背景）
    screen.fill((0, 0, 0))
    # 在游戏循环中，你可以在此处添加渲染和更新逻辑
    screen.blit(GameConst.load_background(), (0, 0))
    # 更新显示内容
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
