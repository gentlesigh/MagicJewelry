import pygame
import os

pygame.init()

# 创建窗口
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("背景测试")

# 测试背景路径
background_path = 'resource/background.png'
if not os.path.exists(background_path):
    print("背景图文件未找到")
else:
    try:
        bg_image = pygame.image.load(background_path)
        print("背景图加载成功")
    except pygame.error as e:
        print(f"加载背景图失败，错误信息: {e}")
        bg_image = None

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制背景
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((0, 0, 0))  # 如果未加载图片，显示黑屏作为背景

    pygame.display.flip()  # 刷新屏幕显示

pygame.quit()
