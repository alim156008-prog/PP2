import pygame
import random
import sys

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BD = (72, 61, 139)
HD = (25, 25, 112)
ORANGE = (255, 140, 0)

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: Multi-Coins")

font_info = pygame.font.SysFont("Verdana", 20)
font_gameover = pygame.font.SysFont("Verdana", 60)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.dead = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        if (self.body[0].x >= WIDTH // CELL or self.body[0].x < 0 or
            self.body[0].y >= HEIGHT // CELL or self.body[0].y < 0):
            self.dead = True

        for segment in self.body[1:]:
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                self.dead = True

    def draw(self):
        for i, segment in enumerate(self.body):
            color = HD if i == 0 else BD
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)
        self.weight = 1
        self.color = GREEN
        self.start_ticks = pygame.time.get_ticks() # Исправлено здесь
        self.max_time = 15 # Добавь дефолтное значение
        self.size_padding = 2 
        self.generate_random_pos(snake_body)

    def draw(self):
        # Рисуем еду с учетом отступа (padding) для изменения визуального размера
        rect_x = self.pos.x * CELL + self.size_padding
        rect_y = self.pos.y * CELL + self.size_padding
        rect_size = CELL - (self.size_padding * 2)
        pygame.draw.rect(screen, self.color, (rect_x, rect_y, rect_size, rect_size))


    def generate_random_pos(self, snake_body):
        # 1. Сначала выбираем тип монетки
        if random.random() < 0.1: 
            self.weight = 3
            self.color = RED
            self.max_time = 5   # Сделаем красную быстрой (5 сек)
            self.size_padding = 0  
        elif random.random() < 0.3:
            self.weight = 2
            self.color = ORANGE
            self.max_time = 8   # Оранжевая (8 сек)
            self.size_padding = 5
        else:
            self.weight = 1
            self.color = GREEN 
            self.max_time = 12  # Зеленая (12 сек)
            self.size_padding = 10  

        # ВАЖНО: Вместо 0 ставим текущее время программы
        self.start_ticks = pygame.time.get_ticks() 

        # 2. Поиск свободного места
        while True:
            self.pos.x = random.randint(0, WIDTH // CELL - 1)
            self.pos.y = random.randint(0, HEIGHT // CELL - 1)
            
            on_snake = any(s.x == self.pos.x and s.y == self.pos.y for s in snake_body)
            if not on_snake:
                break

# Инициализация игры
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
base_fps = 5 
clock = pygame.time.Clock()

game_start_ticks = pygame.time.get_ticks()

running = True
while running:
    current_fps = base_fps + (level - 1) * 2 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    screen.fill(BLACK)
    
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (i, 0), (i, HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i), (WIDTH, i))

    snake.move()
    
    food_seconds_passed = (pygame.time.get_ticks() - food.start_ticks) / 1000
    food_time_left = max(0, food.max_time - food_seconds_passed)
    if food_time_left <= 0:
        food.generate_random_pos(snake.body)


    total_seconds = (pygame.time.get_ticks() - game_start_ticks) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60


    if snake.dead:
        screen.fill(BLACK)
        msg = font_gameover.render("GAME OVER", True, RED)
        screen.blit(msg, (WIDTH//2 - 180, HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    # Проверка столкновения с едой
    if snake.body[0].x == food.pos.x and snake.body[0].y == food.pos.y:
        score += food.weight # Добавляем вес текущей монетки
        snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))
        
        # Запоминаем старый уровень для проверки повышения
        old_level = score // 3
        
        food.generate_random_pos(snake.body)
        
        # Обновление уровня на основе каждых 3 очков
        level = (score // 3) + 1

    snake.draw()
    food.draw()
    
    game_timer_text = font_info.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE)
    
    score_text = font_info.render(f"Score: {score}", True, WHITE)
    level_text = font_info.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))
    screen.blit(game_timer_text, (WIDTH - 200, 10)) 
    
    pygame.display.flip()
    clock.tick(current_fps)

pygame.quit()