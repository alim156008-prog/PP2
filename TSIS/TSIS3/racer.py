import pygame
import random
import time
import os
from persistence import save_score

pygame.init()
pygame.mixer.init()

WIDTH = 400
HEIGHT = 600
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(name, size):
    return pygame.transform.scale(
        pygame.image.load(os.path.join(BASE_DIR, "assets", name)),
        size
    )

def load_sound(name):
    try:
        return pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", name))
    except:
        return None

# ASSETS
IMAGE_PLAYER = load_image("p1.png", (120, 150))
IMAGE_ANOTHERPLAYER = load_image("p2.png", (120, 150)) 
IMAGE_ENEMY = load_image("e1.png", (120, 150))
IMAGE_BG = load_image("as.png", (400, 600))
IMAGE_BONUS = load_image("bonus.png", (50, 50))   
IMAGE_SHIELD = load_image("shield.png", (50,70)) 

# COINS
COIN_IMAGES = [
    load_image("coin1.png", (50, 50)),
    load_image("coin2.png", (70, 70)),
    load_image("coin3.png", (100, 100))
]

sound_crash = load_sound("crash.mp3") # Изменено на mp3
sound_coin = load_sound("kolco.mp3")  # Изменено на kolco.mp3
sound_power = load_sound("bgs.mp3") # Можно оставить тот же звук

font_big = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 20)

def run_game(screen, username, settings):
    clock = pygame.time.Clock()
    player = IMAGE_PLAYER.get_rect(topleft=(180, 500))

    coins = 0
    distance = 0
    speed = 5
    
    enemy_speed = 5 if settings["difficulty"] == "easy" else 12 if settings["difficulty"] == "hard" else 8

    # --- ENEMY ---
    traffic = [IMAGE_ENEMY.get_rect(topleft=(random.randint(0, WIDTH-120), -150))]

    # --- OBSTACLE ---
    obstacle = pygame.Rect(random.randint(0, WIDTH-30), -30, 30, 30)
    
    # --- COIN ---
    current_coin_img = random.choice(COIN_IMAGES)
    coin = current_coin_img.get_rect(
        topleft=(random.randint(0, WIDTH - current_coin_img.get_width()), -50)
    )

    # --- POWER ---
    power = IMAGE_BONUS.get_rect(
        topleft=(random.randint(0, WIDTH - IMAGE_BONUS.get_width()), -50)
    )
    power_type = random.choice(["nitro","shield","repair"])
    player_power = None
    power_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player.x -= speed
        if keys[pygame.K_RIGHT]: player.x += speed

        player.clamp_ip(pygame.Rect(0,0,WIDTH,HEIGHT))
        distance += 1

        # ================= TRAFFIC =================
        for t in traffic:
            t.y += enemy_speed
            if t.top > HEIGHT:
                t.x = random.randint(0, WIDTH - t.width)
                t.y = -t.height

            # hitbox
            player_hitbox = player.inflate(-40, -40)
            enemy_hitbox = t.inflate(-40, -40)

            if player_hitbox.colliderect(enemy_hitbox):
                if player_power == "shield":
                    player_power = None
                    t.x = random.randint(0, WIDTH - t.width)
                    t.y = -t.height
                else:
                    if settings["sound"] and sound_crash: sound_crash.play()
                    save_score(username, coins*10+distance, distance)
                    screen.fill((0,0,0))
                    screen.blit(font_big.render("GAME OVER", True, (255,0,0)), (60,250))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    return "menu"

        # ================= OBSTACLE =================
        obstacle.y += 5
        if obstacle.top > HEIGHT:
            obstacle.x = random.randint(0, WIDTH - obstacle.width)
            obstacle.y = -30

        if player.inflate(-30, -30).colliderect(obstacle):
            speed = 2
        else:
            speed = 5

        # ================= COIN =================
        coin.y += 5
        if coin.top > HEIGHT:
            current_coin_img = random.choice(COIN_IMAGES)
            coin = current_coin_img.get_rect(
                topleft=(random.randint(0, WIDTH - current_coin_img.get_width()), -50)
            )

        if player.colliderect(coin):
            coins += 1
            if settings["sound"] and sound_coin: sound_coin.play()

            current_coin_img = random.choice(COIN_IMAGES)
            coin = current_coin_img.get_rect(
                topleft=(random.randint(0, WIDTH - current_coin_img.get_width()), -50)
            )

        # ================= POWER =================
        power.y += 5
        if power.top > HEIGHT:
            power.x = random.randint(0, WIDTH - power.width)
            power.y = -power.height
            power_type = random.choice(["nitro","shield","repair"])

        if player.colliderect(power):
            player_power = power_type
            power_timer = time.time()
            if settings["sound"] and sound_power: sound_power.play()
            power.x = random.randint(0, WIDTH - power.width)
            power.y = -power.height

        if player_power:
            if player_power == "nitro":
                speed = 10
            elif player_power == "repair":
                coins += 5
                player_power = None

            if player_power and time.time() - power_timer > 5:
                player_power = None
                speed = 5

        # ================= DRAW =================
        screen.blit(IMAGE_BG, (0,0))
        screen.blit(IMAGE_PLAYER, player)

        for t in traffic:
            screen.blit(IMAGE_ENEMY, t)

        screen.blit(current_coin_img, coin)
        pygame.draw.rect(screen,(0,0,0),obstacle)

        if power_type == "shield":
            screen.blit(IMAGE_SHIELD, power)
        else:
            screen.blit(IMAGE_BONUS, power)

        if player_power:
            screen.blit(font_small.render(f"Power: {player_power}", True,(255,255,0)),(10,40))
            if player_power == "shield":
                screen.blit(IMAGE_SHIELD, (150, 40))

        screen.blit(font_small.render(f"Coins:{coins} Dist:{distance}",True,(255,255,255)),(10,10))

        pygame.display.flip()
        clock.tick(60)