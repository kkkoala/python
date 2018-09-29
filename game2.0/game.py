# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:45:22 2018

@author: emmm
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 16:32:29 2018

@author: emmm
"""
import pygame
from pygame.locals import *
from sys import exit
from random import randint
import time

score=0
tscore=0
ss=1#每一次加的分数
enemyss=2
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
blue = (0,0,255)
#定义窗口的分辨率
sw=1600
sh=840
frame_rate=60
animate_cycle=30
clock=pygame.time.Clock()
offset={pygame.K_LEFT:0,pygame.K_RIGHT:0,pygame.K_UP:0,pygame.K_DOWN:0}

#初始化游戏
pygame.init()
pygame.mixer.init()
screen=screen=pygame.display.set_mode([sw,sh])
pygame.display.set_caption('审美疲劳的沙雕游戏')#title
#相关图片资源的导入
shootimg=pygame.image.load('p01.png')
enemyimg=pygame.image.load('p03.jpg')
boomimg=pygame.image.load('p07.png')
heroboomimg=pygame.image.load('p04.jpg')
bomm=pygame.mixer.Sound('5652.wav')
bgm=pygame.mixer.Sound('1388.wav')

hero_surface=[]
#use subsurface to cut the img
hero_surface.append(shootimg.subsurface(pygame.Rect(30,190,130,130)))
hero_surface.append(shootimg.subsurface(pygame.Rect(30,191,130,130)))
hero_surface.append(shootimg.subsurface(pygame.Rect(31,191,130,130)))
hero_surface.append(shootimg.subsurface(pygame.Rect(32,192,130,130)))#left,top,width,height
enemy1_surface=enemyimg.subsurface(pygame.Rect(15,110,145,150))
eds=[]
eds.append(boomimg.subsurface(pygame.Rect(0,90,140,230)))
eds.append(boomimg.subsurface(pygame.Rect(0,90,150,230)))
eds.append(boomimg.subsurface(pygame.Rect(0,90,150,240)))
eds.append(boomimg.subsurface(pygame.Rect(0,90,190,260)))
boom_surface=[]
boom_surface.append(heroboomimg.subsurface(pygame.Rect(70,70,82,70)))
boom_surface.append(heroboomimg.subsurface(pygame.Rect(70,70,100,100)))
boom_surface.append(heroboomimg.subsurface(pygame.Rect(70,70,110,110)))
boom_surface.append(heroboomimg.subsurface(pygame.Rect(70,70,112,112)))
bullet1_surface=shootimg.subsurface(pygame.Rect(185, 210,45, 45))
hero_pos=[0,350]


#相关变量的定义
enemy_group=pygame.sprite.Group()
enemy1_down_group=pygame.sprite.Group()
bullet_down_group=pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullte_surface,bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullte_surface
        self.rect=self.image.get_rect()
        self.rect.topleft=bullet_init_pos
        self.speed=6
    
    def update(self):
        self.rect.left+=self.speed
        if self.rect.left<+self.rect.height:
            self.kill()

class Hero(pygame.sprite.Sprite):
    def __init__(self,hero_surface,hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=hero_surface
        self.rect=self.image.get_rect()
        self.rect.topleft=hero_init_pos
        self.speed=6
        self.is_hit=False
        self.bullets1=pygame.sprite.Group()
        self.down_index=1
        
    def single_shoot(self,bullet1_surface):
        bullet1=Bullet(bullet1_surface,self.rect.midtop)
        self.bullets1.add(bullet1)
    
    def move(self,offset):
        x=self.rect.left+offset[pygame.K_RIGHT]-offset[pygame.K_LEFT]
        y=self.rect.top+offset[pygame.K_DOWN]-offset[pygame.K_UP]
        if x<0:
            self.rect.left=0
        elif x>sw-self.rect.width:
            self.rect.left=sw-self.rect.width
        else:
            self.rect.left=x
        
        if y<0:
            self.rect.top=0
        elif y>sh-self.rect.height:
            self.rect.top=sh-self.rect.height
        else:
            self.rect.top=y


class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_surface,enemy_init_pos,enemyss):
        pygame.sprite.Sprite.__init__(self)
        self.image=enemy_surface
        self.rect=self.image.get_rect()
        self.rect.topleft=enemy_init_pos
        self.speed=enemyss
        self.down_index=0
    
    def update(self):
        self.rect.left-=self.speed
        if self.rect.left<0:
            self.kill()



hero=Hero(hero_surface[0],hero_pos)
        


#相应函数
#判断hero是否被敌人碰撞
def herohit(ticks):
    #判断是hero是否与enemy碰撞
    enemy1_down_list = pygame.sprite.spritecollide(hero, enemy_group, True)
    if len(enemy1_down_list) > 0: # 不空
        enemy1_down_group.add(enemy1_down_list)
        hero.is_hit = True
        
    if hero.is_hit:
        if ticks%(animate_cycle//2)==0:
            hero.down_index+=1
        hero.image=hero_surface[hero.down_index]
        if hero.down_index==3:
            for i in range(0,3):
                screen.blit(boom_surface[i],hero.rect)
            
            hero.down_index=0
            return 0
    else:
        hero.image=hero_surface[ticks//(animate_cycle//2)]

#enymy是否被子弹击中      
def enemys(ticks):
    if ticks%100==0:
        enemy=Enemy(enemy1_surface, [sw,randint(0,sh-enemy1_surface.get_height()), ],enemyss)
        enemy_group.add(enemy)
    enemy_group.update()
    enemy_group.draw(screen)
    
    enemy1_down_group.add(pygame.sprite.groupcollide(enemy_group,hero.bullets1,True,True))
    #第一二两个是进行碰撞检测的精灵组，34是是否碰撞后kill
    
    
    for enemy1_down in enemy1_down_group:
        screen.blit(eds[enemy1_down.down_index],enemy1_down.rect)
        bomm.play()
        if ticks%(animate_cycle//2)==0:
            if enemy1_down.down_index < 3:
                enemy1_down.down_index +=1
                
            else:
                enemy1_down_group.remove(enemy1_down)
                global score
                score+=ss

#子弹的相关函数
def bullets(ticks):
    if ticks%20==0:
        hero.single_shoot(bullet1_surface)
    
    hero.bullets1.update()
    hero.bullets1.draw(screen)
   
    
def showscore(score):
    font=pygame.font.SysFont(None, 25)
    text=font.render("Score:"+str(score), True, (255,255,255))
    screen.blit(text,(0,0))
    
def run():#相关的操作函数，写在一个函数里方便对游戏过程整体的操作
    ticks=0#count
    global enemy_group
    global enemy1_down_group
    global hero
    global score
    global ss
    global enemyss
    global tscore
    ss=1
    score=0
    hero=Hero(hero_surface[0],hero_pos)
    enemy_group.empty()
    enemy1_down_group.empty()
    while True:
        bgm.play()
        if score%100==0 and score>0:
            a=score//100
            #enemyss+=a
            ss+=a
            Enemy.speed=Enemy.speed+a
        clock.tick(frame_rate)#限制帧率
        #screen.blit(background,(0,0))#设置背景
        screen.fill(black)
        showscore(score)
        #for butterfly
        if ticks>=animate_cycle:
            ticks=0
        #hero.image=hero_surface[ticks//(animate_cycle//2)]#cahnge pic
        flag=1#设置flag判断是否被撞击
        flag=herohit(ticks)
        if flag==0:
            if score>tscore:
                tscore=score
            break
        bullets(ticks)#shoot
        enemys(ticks) #for enemy
        screen.blit(hero.image,hero.rect)#draw butterfly
        ticks+=1
        pygame.display.update()#updatescreen
       
        #for quit
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type==pygame.KEYDOWN:
                if event.key in offset:
                    offset[event.key]=hero.speed
            elif event.type==pygame.KEYUP:
                if event.key in offset:
                    offset[event.key]=0
        hero.move(offset)#hero的移动
        
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def quitgame():
    pygame.quit()
    quit()


def test():
    screen.fill(white)
    time.sleep(60)
    
    
def button (msg, x, y, w, h, ic):
    mouse=pygame.mouse.get_pos()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen,bright_red, (x,y,w,h))#
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    #smallText = pygame.font.Font("freesansbold.ttf", 20)
    smallText = pygame.font.SysFont('arial', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)

def text(msg,x,y,w,h):
    smallText = pygame.font.SysFont('arial', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)
    
    
    
    
def mouse(x,y,w,h,ac):
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))#鼠标在按钮上时高亮显示
        if click[0] == 1:#如果鼠标在按钮上并且按下，执行操作
            return 1 

           
def main0():
    mouse1=0
    mouse2=0
   
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(black)
        #screen.blit(gameover,(0,0))
        button("GO", 100, 250, 100, 50, (26,26,26))#循环出现问题--尝试将button的显示和判断分开写
        button("Quit",300, 250, 100, 50,(26,26,26))#分开后依然不对，
        mouse1=mouse(100, 250, 100, 50,bright_red)#最后发现是别的函数报错,但是依然存在run函数只是闪过一瞬的情况
        mouse2=mouse(300, 250, 100, 50,bright_red)#原因是没有进行初始化每一次开始run各个类都还停留在上一次死掉的状态
        text('score',100,400,100,50)
        text(str(score),300,400,100,50)
        text('highest',100,500,100,50)
        text(str(tscore),300,500,100,50)
        if mouse1==1:
            run()
            mouse1=0
        elif mouse2==1:
            quitgame()
                
        pygame.display.update()
        clock.tick(60)

main0()
pygame.quit()