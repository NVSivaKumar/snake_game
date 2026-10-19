import sys
import random
import pygame
from pygame.math import Vector2
from pygame import K_ESCAPE, KEYDOWN, QUIT
import cv2
import mediapipe as mp

# ---------------- SETTINGS ----------------
CONTROL_MODE = "KEYBOARD"   # default mode

# ---------------- HAND TRACKING ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_x, prev_y = 0, 0
MOVE_THRESHOLD = 0.05

def get_hand_direction():
    global prev_x, prev_y

    success, frame = cap.read()
    if not success:
        return None

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    direction = None

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]

        x = hand.landmark[8].x
        y = hand.landmark[8].y

        dx = x - prev_x
        dy = y - prev_y

        if abs(dx) > abs(dy):
            if dx > MOVE_THRESHOLD:
                direction = "RIGHT"
            elif dx < -MOVE_THRESHOLD:
                direction = "LEFT"
        else:
            if dy > MOVE_THRESHOLD:
                direction = "DOWN"
            elif dy < -MOVE_THRESHOLD:
                direction = "UP"

        prev_x, prev_y = x, y
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Control", frame)
    cv2.waitKey(1)
    return direction

# ---------------- GAME OBJECTS ----------------

class Fruit:
    def __init__(self):
        self.random_fruit()

    def draw_fruit(self):
        rect = pygame.Rect(int(self.pos.x*cellsize), int(self.pos.y*cellsize), cellsize, cellsize)
        screen.blit(food, rect)

    def random_fruit(self):
        self.x = random.randint(0, cellnum - 1)
        self.y = random.randint(0, cellnum - 1)
        self.pos = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(0,0)
        self.body_img = pygame.image.load('images/body_horizontal.png').convert_alpha()
        self.crunch = pygame.mixer.Sound('crunch.wav')

    def draw_snake(self):
        for block in self.body:
            rect = pygame.Rect(int(block.x*cellsize), int(block.y*cellsize), cellsize, cellsize)
            screen.blit(self.body_img, rect)

    def move_snake(self):
        if self.direction == Vector2(0,0):
            return
        bodycopy = self.body[:-1]
        bodycopy.insert(0, bodycopy[0] + self.direction)
        self.body = bodycopy

    def addblock(self):
        bodycopy = self.body[:]
        bodycopy.insert(0, bodycopy[0] + self.direction)
        self.body = bodycopy

    def reset(self):
        self.body = [Vector2(7,10), Vector2(6,10), Vector2(5,10)]
        self.direction = Vector2(0,0)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.eat()
        self.over()

    def draw(self):
        self.grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_mode()

    def grass(self):
        for row in range(cellnum):
            for col in range(cellnum):
                if (row+col)%2==0:
                    rect = pygame.Rect(col*cellsize,row*cellsize,cellsize,cellsize)
                    pygame.draw.rect(screen,(167,209,61),rect)

    def eat(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.random_fruit()
            self.snake.addblock()
            self.snake.crunch.play()

    def over(self):
        if not 0 <= self.snake.body[0].x < cellnum:
            self.gameover()
        if not 0 <= self.snake.body[0].y < cellnum:
            self.gameover()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameover()

    def gameover(self):
        global GAME_ACTIVE
        GAME_ACTIVE = False

    def draw_mode(self):
        text = gamefont.render(f"Mode: {CONTROL_MODE}  (1=Keyboard 2=Hand)", True, (56,74,12))
        screen.blit(text, (10, 10))

# ---------------- GAME SETUP ----------------

pygame.init()
cellsize = 40
cellnum = 20
screen = pygame.display.set_mode((cellsize*cellnum, cellnum*cellsize))
pygame.display.set_caption("Snake Control Modes")

gamefont = pygame.font.SysFont(None, 28)

maingame = Main()
GAME_ACTIVE = True

food = pygame.image.load('images/apple.png').convert_alpha()
scrupdate = pygame.USEREVENT
pygame.time.set_timer(scrupdate, 150)

# ---------------- GAME LOOP ----------------

while True:
    for event in pygame.event.get():

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

        if event.type == QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()

        # -------- SWITCH CONTROL MODE --------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                CONTROL_MODE = "KEYBOARD"
            if event.key == pygame.K_2:
                CONTROL_MODE = "HAND"

        # -------- KEYBOARD CONTROL --------
        if CONTROL_MODE == "KEYBOARD":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and maingame.snake.direction.y != 1:
                    maingame.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN and maingame.snake.direction.y != -1:
                    maingame.snake.direction = Vector2(0,1)
                if event.key == pygame.K_RIGHT and maingame.snake.direction.x != -1:
                    maingame.snake.direction = Vector2(1,0)
                if event.key == pygame.K_LEFT and maingame.snake.direction.x != 1:
                    maingame.snake.direction = Vector2(-1,0)

        if event.type == scrupdate and GAME_ACTIVE:
            maingame.update()

    # -------- HAND CONTROL --------
    if GAME_ACTIVE and CONTROL_MODE == "HAND":
        hand_dir = get_hand_direction()

        if hand_dir == "UP" and maingame.snake.direction.y != 1:
            maingame.snake.direction = Vector2(0, -1)
        elif hand_dir == "DOWN" and maingame.snake.direction.y != -1:
            maingame.snake.direction = Vector2(0, 1)
        elif hand_dir == "RIGHT" and maingame.snake.direction.x != -1:
            maingame.snake.direction = Vector2(1, 0)
        elif hand_dir == "LEFT" and maingame.snake.direction.x != 1:
            maingame.snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))

    if GAME_ACTIVE:
        maingame.draw()

    pygame.display.update()
