import pygame
import datetime
import math
from tools import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    canvas = pygame.surface.Surface((800, 600))
    canvas.fill(BLACK)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    curr_color = BLUE
    curr_tool = 'pencil'
    thickness = 2
    drawing = False
    start_pos = (0, 0)
    last_pos = (0, 0)
    
    typing = False
    text_buffer = ""
    text_pos = (0, 0)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if typing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        txt_surf = font.render(text_buffer, True, curr_color)
                        canvas.blit(txt_surf, text_pos)
                        typing = False
                    elif event.key == pygame.K_ESCAPE: typing = False
                    elif event.key == pygame.K_BACKSPACE: text_buffer = text_buffer[:-1]
                    else: text_buffer += event.unicode
                continue

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_r: curr_color = RED
                if event.key == pygame.K_g: curr_color = GREEN
                if event.key == pygame.K_b: curr_color = BLUE
                
                # Толщина
                if event.key == pygame.K_1: thickness = 2
                if event.key == pygame.K_2: thickness = 5
                if event.key == pygame.K_3: thickness = 10
                
                # Инструменты (Ваши клавиши)
                if event.key == pygame.K_p: curr_tool = 'pencil'
                if event.key == pygame.K_s: curr_tool = 'square'
                if event.key == pygame.K_t: curr_tool = 'right_tri'
                if event.key == pygame.K_l: curr_tool = 'equi_tri'
                if event.key == pygame.K_h: curr_tool = 'rhombus'
                if event.key == pygame.K_f: curr_tool = 'fill'
                if event.key == pygame.K_e: curr_tool = 'eraser'
                
                # Очистка
                if event.key == pygame.K_z:
                    canvas.fill(BLACK)
                
                # Сохранение (Ctrl+S)
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    pygame.image.save(canvas, f"art_{ts}.png")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if curr_tool == 'fill':
                    flood_fill(canvas, event.pos, curr_color)
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if curr_tool == 'pencil':
                        # Рисуем сразу на холсте, чтобы не было прерываний
                        pygame.draw.line(canvas, curr_color, last_pos, mouse_pos, thickness)
                        last_pos = mouse_pos
                    elif curr_tool == 'eraser':
                        pygame.draw.circle(canvas, BLACK, mouse_pos, thickness * 2)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    # Финализация фигур на холсте
                    pts = get_points(curr_tool, start_pos, event.pos)
                    if pts:
                        pygame.draw.polygon(canvas, curr_color, pts, thickness)
                    elif curr_tool == 'line': # Если добавите линию
                        pygame.draw.line(canvas, curr_color, start_pos, event.pos, thickness)
                    
                    drawing = False

        # Отрисовка интерфейса
        screen.blit(canvas, (0, 0))

        # Предпросмотр геометрии (рисуем на экране поверх холста)
        if drawing and curr_tool not in ['pencil', 'eraser', 'fill']:
            pts = get_points(curr_tool, start_pos, mouse_pos)
            if pts:
                pygame.draw.polygon(screen, curr_color, pts, thickness)

        # Текст
        if typing:
            screen.blit(font.render(text_buffer + "|", True, curr_color), text_pos)

        pygame.display.set_caption(f"Tool: {curr_tool} | Size: {thickness} | Ctrl+S: Save | Z: Clear")
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()