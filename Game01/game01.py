#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: game01.py
@time: 2019/3/16 15:06
'''
import pygame
from pygame.locals import *
import math
import random

# 初始化pygame，设置展示窗口
pygame.init()
width,height=640,480
screen=pygame.display.set_mode((width,height))

# 加载图片
rabbit_img=pygame.image.load('resources/images/dude.png')
grass_img=pygame.image.load('resources/images/grass.png')
castle_img=pygame.image.load('resources/images/castle.png')
# 循环
while True:
    # 在给屏幕画任何东西之前用黑色进行填充
    screen.fill(0)
    # 添加草地和塔
    for x in range(width//grass_img.get_width()+1):
        for y in range(height//grass_img.get_height()+1):
            screen.blit(grass_img,(x*100,y*100))
    screen.blit(castle_img,(0,30))
    screen.blit(castle_img, (0, 135))
    screen.blit(castle_img, (0, 240))
    screen.blit(castle_img, (0, 345))
    # 在屏幕的（100,100）坐标处添加加载的兔子图片
    screen.blit(rabbit_img,(100,100))
    # 更新屏幕
    pygame.display.flip()
    # 检查一些新的事件，如果有退出的命令，则终止程序运行
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
