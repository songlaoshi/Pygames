#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: pikachu.py
@time: 2019/3/16 22:11
'''

import cocos

class Pikachu(cocos.sprite.Sprite):
    def __init__(self):
        super(Pikachu,self).__init__('pikachu.png')
        # 是否可以跳跃
        self.able_jump=False
        # 速度
        self.speed=0
        # 锚点
        self.image_anchor=0,0
        # 皮卡丘的位置
        self.position=80,280
        self.schedule(self.update)
    # 声控跳跃
    def jump(self,h):
        if self.able_jump:
            self.y+=1
            self.speed-=max(min(h,10),7)
            self.able_jump=False
    # 着陆后静止
    def land(self,y):
        if self.y>y-25:
            self.able_jump=True
            self.speed=0
            self.y=y
    # 更新（重力下降）
    def update(self,dt):
        self.speed+=10*dt
        self.y-=self.speed
        if self.y<-85:
            self.reset()
    # 重置
    def reset(self):
        self.parent.reset()
        self.able_jump=False
        self.speed=0
        self.position=80,280