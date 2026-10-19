import sys
import random
import pygame
from random import randint
import time
from pygame.math import Vector2
from pygame import K_ESCAPE, KEYDOWN, QUIT, K_RIGHT, K_LEFT, K_DOWN, K_UP
class Fruit:
    def __init__(self):
        self.random_fruit()
    def draw_fruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*cellsize),int(self.pos.y*cellsize),cellsize,cellsize)
        #pygame.draw.rect(screen,(126,166,114),fruit_rect)
        screen.blit(food,fruit_rect)
    def random_fruit(self):
        self.x = random.randint(0, cellnum - 1)
        self.y = random.randint(0, cellnum - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body=[Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction=Vector2(0,0)

        self.headup = pygame.image.load('images/head_up.png').convert_alpha()
        self.headright = pygame.image.load('images/head_right.png').convert_alpha()
        self.headdown = pygame.image.load('images/head_down.png').convert_alpha()
        self.headleft = pygame.image.load('images/head_left.png').convert_alpha()

        self.tailup = pygame.image.load('images/tail_up.png').convert_alpha()
        self.taildown = pygame.image.load('images/tail_down.png').convert_alpha()
        self.tailright = pygame.image.load('images/tail_right.png').convert_alpha()
        self.tailleft = pygame.image.load('images/tail_left.png').convert_alpha()

        self.bodyv = pygame.image.load('images/body_vertical.png').convert_alpha()
        self.bodyh = pygame.image.load('images/body_horizontal.png').convert_alpha()

        self.bodytl = pygame.image.load('images/body_tl.png').convert_alpha()
        self.bodytr = pygame.image.load('images/body_tr.png').convert_alpha()
        self.bodybr = pygame.image.load('images/body_br.png').convert_alpha()
        self.bodybl = pygame.image.load('images/body_bl.png').convert_alpha()

        self.crunch=pygame.mixer.Sound('crunch.wav')

    def draw_snake(self):
        self.headpos();
        self.tailpos()
        for index,block in enumerate(self.body):
            xpos=int(block.x * cellsize)
            ypos = int(block.y * cellsize)
            block_rect = pygame.Rect(xpos,ypos, cellsize, cellsize)
            if index==0:
                screen.blit(self.head,block_rect)
            elif index==len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                pblk=self.body[index+1]-block
                nblk = self.body[index - 1] - block
                if pblk.x==nblk.x:
                    screen.blit(self.bodyv,block_rect)
                elif pblk.y==nblk.y:
                    screen.blit(self.bodyh,block_rect)
                else:
                    if pblk.x==-1 and nblk.y==-1 or pblk.y==-1 and nblk.x==-1:
                        screen.blit(self.bodytl,block_rect)
                    elif pblk.x==1 and nblk.y==-1 or pblk.y==-1 and nblk.x==1:
                        screen.blit(self.bodytr,block_rect)
                    elif pblk.x==-1 and nblk.y==1 or pblk.y==1 and nblk.x==-1:
                        screen.blit(self.bodybl,block_rect)
                    elif pblk.x==1 and nblk.y==1 or pblk.y==1 and nblk.x==1:
                        screen.blit(self.bodybr,block_rect)


    def headpos(self):
        headposition=self.body[1]-self.body[0]
        if headposition==Vector2(1,0):self.head=self.headleft
        elif headposition==Vector2(-1,0):self.head=self.headright
        elif headposition==Vector2(0,-1):self.head=self.headdown
        if headposition==Vector2(0,1):self.head=self.headup
    def tailpos(self):
        tailposition = self.body[-2] - self.body[-1]
        if tailposition == Vector2(1, 0):
            self.tail = self.tailleft
        elif tailposition == Vector2(-1, 0):
            self.tail = self.tailright
        elif tailposition == Vector2(0, -1):
            self.tail = self.taildown
        if tailposition == Vector2(0, 1):
            self.tail = self.tailup

    def move_snake(self):
        if self.direction == Vector2(0, 0):
            return  # ⛔ do nothing until input
        bodycopy = self.body[:-1]
        bodycopy.insert(0, bodycopy[0] + self.direction)
        self.body = bodycopy

    def addblock(self):
        bodycopy = self.body[:]
        bodycopy.insert(0, bodycopy[0] + self.direction)
        self.body = bodycopy[:]
    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)

class Main:
    def __init__(self):
        self.snake=Snake()
        self.fruit=Fruit()
    def update(self):
        self.snake.move_snake()
        self.eat()
        self.over()

    def draw(self):
        self.grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.drawscore()

    def grass(self):
        for row in range(cellnum):
            if row%2==0:
                for col in range(cellnum):
                    if col%2==0:
                            grassrect=pygame.Rect(col*cellsize,row*cellsize,cellsize,cellsize)
                            pygame.draw.rect(screen,(167,209,61),grassrect)
            else:
                for col in range(cellnum):
                    if col%2!=0:
                            grassrect=pygame.Rect(col*cellsize,row*cellsize,cellsize,cellsize)
                            pygame.draw.rect(screen,(167,209,61),grassrect)
    def eat(self):
        if self.snake.body[0]==self.fruit.pos:
            self.fruit.random_fruit()
            self.snake.addblock()
            self.snake.crunch.play()
            for block in self.snake.body[1:]:
                if block == self.fruit.pos:
                    self.fruit.random_fruit()
    def over(self):
        if not 0<=self.snake.body[0].x<cellnum:
            self.gameover()
        if not 0 <= self.snake.body[0].y < cellnum:
            self.gameover()
        for block in self.snake.body[1:]:
            if block ==self.snake.body[0]:
                self.gameover()

    def gameover(self):
        global GAME_ACTIVE
        GAME_ACTIVE = False

    def draw_game_over(self):
        title = gamefont.render("GAME OVER", True, (255, 0, 0))
        restart = gamefont.render("Press SPACE to Restart", True, (56, 74, 12))
        score_text = gamefont.render(
            f"Score : {len(self.snake.body) - 3}", True, (56, 74, 12)
        )

        title_rect = title.get_rect(center=(cellsize * cellnum // 2, cellsize * cellnum // 2 - 40))
        score_rect = score_text.get_rect(center=(cellsize * cellnum // 2, cellsize * cellnum // 2))
        restart_rect = restart.get_rect(center=(cellsize * cellnum // 2, cellsize * cellnum // 2 + 40))

        screen.blit(title, title_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart, restart_rect)

    def drawscore(self):
        score=str(len(self.snake.body)-3)
        scoresurface=gamefont.render(score,True,(56,74,12))
        sx=int(cellsize*cellnum-60)
        sy = int(cellsize * cellnum - 40)
        srect=scoresurface.get_rect(center=(sx,sy))
        screen.blit(scoresurface,srect)


pygame.init()
cellsize=40
cellnum=20
screen=pygame.display.set_mode((cellsize*cellnum,cellnum*cellsize))
screen.fill((175, 215, 70))
gamefont=pygame.font.SysFont('StormGust.ttf',25)
maingame=Main()
GAME_ACTIVE = True

pygame.display.flip()
scrupdate=pygame.USEREVENT
food=pygame.image.load('images/apple.png').convert_alpha()
pygame.time.set_timer(scrupdate,150)
while True:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type==scrupdate and GAME_ACTIVE:
            maingame.update()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                if maingame.snake.direction.y !=1:
                    maingame.snake.direction=Vector2(0,-1)
            if event.key==pygame.K_DOWN:
                if maingame.snake.direction.y != -1:
                    maingame.snake.direction=Vector2(0,1)
            if event.key==pygame.K_RIGHT:
                if maingame.snake.direction.x != -1:
                    maingame.snake.direction=Vector2(1,0)
            if event.key==pygame.K_LEFT:
                if maingame.snake.direction.x != 1:
                    maingame.snake.direction=Vector2(-1,0)
            if event.key == pygame.K_SPACE and not GAME_ACTIVE:
                maingame = Main()
                GAME_ACTIVE = True

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((175, 215, 70))
    if GAME_ACTIVE:
        maingame.draw()
    else:
        maingame.draw_game_over()

    pygame.display.update()




