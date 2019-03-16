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
# 移动兔子，keys记录键盘按键情况
keys=[False,False,False,False]
playerpos=[100,100]
# 跟踪玩家的精度变量，记录了射出的箭头数和被击中的獾的数量
# 之后会根据这些数据计算玩家射击精确度
acc=[0,0]
# 跟踪箭头变量
arrows=[]
# 定义一个计时器，使得游戏经过一段时间就新建一只獾
badtimer=100
badtimer1=0
badguys=[[640,100]]
healthvalue=194
# 播放声音初始化
pygame.mixer.init()

# 加载图片
rabbit_img=pygame.image.load('resources/images/dude.png')
grass_img=pygame.image.load('resources/images/grass.png')
castle_img=pygame.image.load('resources/images/castle.png')
# 箭头
arrow_img=pygame.image.load('resources/images/bullet.png')
# 獾
badguy_img1=pygame.image.load('resources/images/badguy.png')
badguy_img=badguy_img1
# 血量
healthbar_img=pygame.image.load('resources/images/healthbar.png')
health_img=pygame.image.load('resources/images/health.png')
# 胜利与失败
gameover_img=pygame.image.load('resources/images/gameover.png')
youwin_img=pygame.image.load('resources/images/youwin.png')
# 加载声音文件并配置音量
hit=pygame.mixer.Sound('resources/audio/explode.wav')
enemy=pygame.mixer.Sound('resources/audio/enemy.wav')
shoot=pygame.mixer.Sound('resources/audio/shoot.wav')
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
# 加载游戏的背景音乐并且一直播放
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.25)
# 循环的停止与否
# running变量跟踪游戏是否结束
# exitcode变量跟踪玩家是否胜利
running=True
exitcode=False
#
# 循环
while running:
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
    # 首先获取鼠标和兔子的位置，然后获取通过atan2函数得出的旋转角度和弧度
    # 当兔子被旋转的时候，他的位置会改变
    # 所以需要重新计算兔子的位置，然后在屏幕上显示出来
    position=pygame.mouse.get_pos()
    angle=math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot=pygame.transform.rotate(rabbit_img,360-angle*57.29)
    playerpos_new=(playerpos[0]-playerrot.get_rect().width/2,playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot,playerpos_new)
    # 在屏幕上画出箭头
    # velx,vely的值表示行进距离，10表示速度
    # if表达式检查箭头是否超出了屏幕范围，超出就删除该箭头
    # 第二个for是循环每一个箭头，画出旋转的箭头
    for bullet in arrows:
        index=0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index) #删除箭头
        index+=1
        for projectile in arrows:
            arrow1=pygame.transform.rotate(arrow_img,360-projectile[0]*57.29)
            screen.blit(arrow1,(projectile[1],projectile[2]))

    # 更新并显示獾
    # 检查badtimer是否为0，如果为0则创建一个獾然后重新设置badtimer
    # 第一个循环更新獾的x坐标，检查獾是否超出屏幕的范围，如果超出则删除
    # 第二个循环是来画出所有的獾
    if badtimer==0:
        badguys.append([640,random.randint(50,430)])
        badtimer=100-(badtimer1*2)
        if badtimer1>=35:
            badtimer1=35
        else:
            badtimer1+=5
    index_badguy=0
    for badguy in badguys:
        if badguy[0]<-64:
            hit.play() #獾击中城堡音效
            badguys.pop(index_badguy)
        badguy[0]-=7
        # 獾可以炸掉城堡
        # 如果獾的x坐标离坐标小于64，则删除该獾并且减少血量，减小的大小为5-20的一个随机数
        badrect=pygame.Rect(badguy_img.get_rect())
        badrect.top=badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            healthvalue-=random.randint(5,20)
            badguys.pop(index_badguy)
        # 獾与箭头的碰撞
        index_arrow=0
        for bullet in arrows:
            bulletrect=pygame.Rect(arrow_img.get_rect())
            bulletrect.left=bullet[1]
            bulletrect.top=bullet[2]
            if badrect.collidedict(bulletrect):
                enemy.play() # 射中獾音效
                acc[0]+=1 # 打中个数合计
                badguys.pop(index_badguy) #删除獾
                arrows.pop(index_arrow) # 删除箭头
            index_arrow+=1
        index_badguy+=1
    for badguy in badguys:
        screen.blit(badguy_img,badguy)
    # 添加时间显示
    font=pygame.font.Font(None,24)
    survivedtext=font.render(str((pygame.time.get_ticks())//60000)+':'
                             +str((pygame.time.get_ticks())//1000%60).zfill(2),True,(0,0,0))
    textRect=survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext,textRect)
    # 添加血量条
    screen.blit(healthbar_img,(5,5))
    for health1 in range(healthvalue):
        screen.blit(health_img,(health1+8,8))
    # 更新屏幕
    pygame.display.flip()
    # 检查一些新的事件，如果有退出的命令，则终止程序运行
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        # 根据按键来更新按键记录数组
        if event.type==pygame.KEYDOWN:
            if event.key==K_w:
                keys[0]=True
            elif event.key==K_a:
                keys[1]=True
            elif event.key==K_s:
                keys[2]=True
            elif event.key==K_d:
                keys[3]=True
        if event.type==pygame.KEYUP:
            if event.key==K_w:
                keys[0]=False
            elif event.key==K_a:
                keys[1]=False
            elif event.key==K_s:
                keys[2]=False
            elif event.key==K_d:
                keys[3]=False
        # 玩家点击鼠标，射出一支箭
        if event.type==pygame.MOUSEBUTTONDOWN:
            shoot.play() #射箭音效
            position=pygame.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(playerpos_new[1]+32)
                                      ,position[0]-(playerpos_new[0]+26))
                              ,playerpos_new[0]+32,playerpos_new[1]+26])

    # 移动兔子
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5
    # 獾的计时器
    badtimer-=1

    # 胜利与失败的判断条件
    # 如果时间到了（90s）,那么停止运行游戏，设置游戏的输出
    # 如果城堡被毁了，那么停止运行游戏，设置游戏的输出
    # 计算玩家射击精确度

    #是否时间到了+没血了+计算射击精确度
    if pygame.time.get_ticks()>=90000:
        running=False
        exitcode=True
    if healthvalue<=0:
        running=False
        exitcode=False
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
        accuracy=('%.2f'%accuracy)
    else:
        accuracy=0
if exitcode==False:
    pygame.font.init()
    font=pygame.font.Font(None,24)
    text=font.render('Accuracy: '+str(accuracy)+'%',True,(255,0,0))
    textRect=text.get_rect()
    textRect.centerx=screen.get_rect().centerx
    textRect.centery=screen.get_rect().centery+24
    screen.blit(gameover_img,(0,0))
    screen.blit(text,textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render('Accuracy: ' + str(accuracy) + '%', True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin_img, (0, 0))
    screen.blit(text, textRect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.flip()
