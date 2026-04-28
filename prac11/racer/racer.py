import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

# ==========================================
# БЛОК ТОНКОЙ НАСТРОЙКИ (РЕДАКТИРУЙ ЗДЕСЬ)
# ==========================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800  # Подровнял под твой DISPLAYSURF

# Размеры персонажей (Ширина, Высота) в пикселях
PLAYER_SIZE = (300, 350)   # Сделал чуть меньше и стройнее
ENEMY_SIZE  = (300, 350)   # Враг чуть крупнее игрока

# Размеры монет (Ширина, Высота)
COIN1_SIZE = (70, 70)    # Самая большая
COIN2_SIZE = (100, 100)    # Средняя
COIN3_SIZE = (130, 130)    # Маленькая

# Скорости
START_SPEED = 5
FPS = 60
FramePerSec = pygame.time.Clock()
SPEED = START_SPEED
SCORE = 0
COIN_SCORE = 0 

# Цвета
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)
game_over_text = font_big.render("Game Over", True, RED)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load("as.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        img = pygame.image.load("e1.png").convert_alpha()
        # Используем константу ENEMY_SIZE
        self.image = pygame.transform.scale(img, ENEMY_SIZE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        img = pygame.image.load("p1.png").convert_alpha()
        # Используем константу PLAYER_SIZE
        self.image = pygame.transform.scale(img, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)       
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(7, 0)
        if pressed_keys[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 7)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Словарь настроек: картинка -> (размер, ценность)
        self.settings = {
            "coin1.png": {"size": COIN1_SIZE, "val": 1},
            "coin2.png": {"size": COIN2_SIZE, "val": 2},
            "coin3.png": {"size": COIN3_SIZE, "val": 5}
        }
        self.spawn()

    def spawn(self):
        self.image_name = random.choice(list(self.settings.keys()))
        conf = self.settings[self.image_name]
        
        raw_img = pygame.image.load(self.image_name).convert_alpha()
        self.image = pygame.transform.scale(raw_img, conf["size"])
        self.value = conf["val"]
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

# Инициализация объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2 # Чуть замедлил ускорение для баланса
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Отрисовка текста
    s_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    c_text = font_small.render(f"Coins: {COIN_SCORE}", True, RED)
    DISPLAYSURF.blit(s_text, (10, 10))
    DISPLAYSURF.blit(c_text, (SCREEN_WIDTH - 120, 10))

    # Движение и отрисовка
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
            
    # Сбор монет
    hit_coins = pygame.sprite.spritecollide(P1, coins, False, pygame.sprite.collide_mask)
    for coin in hit_coins:
        COIN_SCORE += coin.value
        try:
            pygame.mixer.Sound("kolco.mp3").play()
        except: pass
        coin.spawn()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies, pygame.sprite.collide_mask):
        try:
            pygame.mixer.Sound('crash.mp3').play()
        except: pass
        time.sleep(0.5)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)