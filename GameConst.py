import os
import random
import pygame


# 定义常量
BACKGROUND_IMAGE_PATH = 'resource/background.png'
MUSIC_FILES = [
    'resource/Lv0AllKindsofEverything.wav',
    'resource/Lv1HappyChineseFestival.wav',
    'resource/Lv2DescendantsoftheDragon.wav',
    'resource/Lv3RisefromYourGrave.wav',
    'resource/Lv4HuntersChorus.wav',
    'resource/Lv5Moonlight OnTheColorado.wav',
    'resource/Lv6Greensleeves.wav',
    'resource/Lv7SpeakSoftlyLove.wav'
]


# 加载背景图像
def load_background():
    if os.path.exists(BACKGROUND_IMAGE_PATH):
        return pygame.image.load(BACKGROUND_IMAGE_PATH)
    else:
        print(f"Background image not found at {BACKGROUND_IMAGE_PATH}")
        # 如果路径错误，加载创建纯黑背景替代
        surface = pygame.Surface((800, 600))
        surface.fill((0, 0, 0))  # 默认黑色
        return surface


# 颜色列表
COLOR_LIST = [
    pygame.Color('red'),
    pygame.Color('orange'),
    pygame.Color('yellow'),
    pygame.Color('green'),
    pygame.Color('cyan'),
    pygame.Color('magenta')
]


# 获取下一个颜色
def next_color():
    return random.choice(COLOR_LIST)

# 获取音乐文件路径
def get_music(index):
    """根据索引获取音乐文件路径"""
    if index < len(MUSIC_FILES):
        return MUSIC_FILES[index]
    else:
        return None  # 索引超出范围

# 加载音乐
def load_music():
    music_list = []
    for music_file in MUSIC_FILES:
        if os.path.exists(music_file):
            music_list.append(music_file)
        else:
            print(f"Music file not found: {music_file}")
    return music_list


# 行和列的常量
ALL_ROWS = 15
ALL_COLS = 6
REMOVE_CNT = 3
def All_Rows():
    return ALL_ROWS
def All_Cols():
    return ALL_COLS
# 加载资源
background = load_background()
music_list = load_music()

