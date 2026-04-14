import pygame
from datetime import datetime
import sys
import math
import os

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🕒 Mickey's Clock")
clock = pygame.time.Clock()

CENTER = (WIDTH // 2, HEIGHT // 2)
FACE_X = -25
FACE_Y = -30

def prepare_hand(image_path):
    orig = pygame.image.load(image_path).convert_alpha()
    orig = pygame.transform.scale(orig, (500, 300)) 
    surrounding = pygame.Surface((orig.get_width() * 2, orig.get_height()), pygame.SRCALPHA)
    surrounding.blit(orig, (orig.get_width(), 0)) 
    return surrounding

try:
    mickey_face = pygame.image.load(os.path.join("images", "mickey_face.png")).convert_alpha()
    mickey_face = pygame.transform.scale(mickey_face, (700, 500)) 
 
    hand_img = prepare_hand(os.path.join("images", "mickey_hand.png"))
except Exception as e:
    print(f"Ошибка: {e}")
    sys.exit()

def rotate_hand(image, angle):
    rotated_hand = pygame.transform.rotate(image, angle)
    rect = rotated_hand.get_rect(center=CENTER)
    screen.blit(rotated_hand, rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    cur = datetime.now()
    sec_angle = - (cur.second * 6) - 180 
    min_angle = - (cur.minute * 6 + cur.second * 0.1) - 180

    screen.fill((30, 30, 40)) 
    
    pygame.draw.circle(screen, (0, 0, 0), CENTER, 380) 
    pygame.draw.circle(screen, (255, 223, 128), CENTER, 365) 

    for i in range(60):
        angle = math.radians(i * 6)
        start_dist = 330 if i % 5 == 0 else 350
        x1 = CENTER[0] + start_dist * math.sin(angle)
        y1 = CENTER[1] - start_dist * math.cos(angle)
        x2 = CENTER[0] + 365 * math.sin(angle)
        y2 = CENTER[1] - 365 * math.cos(angle)
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 5 if i % 5 == 0 else 2)

    face_pos_rect = mickey_face.get_rect(center=(CENTER[0] + FACE_X, CENTER[1] + FACE_Y))
    screen.blit(mickey_face, face_pos_rect)

    rotate_hand(hand_img, min_angle) 
    rotate_hand(hand_img, sec_angle) 
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()