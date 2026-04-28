import pygame
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def get_points(shape_type, start, end):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if shape_type == 'square':
        # Квадрат: берем минимальное расстояние, чтобы стороны были равны
        side = max(abs(dx), abs(dy))
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        return [(sx, sy), (sx + side, sy), (sx + side, sy + side), (sx, sy + side)]

    elif shape_type == 'right_tri':
        # Прямоугольный треугольник
        return [(x1, y1), (x1, y2), (x2, y2)]

    elif shape_type == 'equi_tri':
        # Равносторонний треугольник (вершина сверху, основание снизу)
        height = dy
        side = abs(height * 2 / math.sqrt(3))
        return [(x1, y1), (x1 - side/2, y1 + height), (x1 + side/2, y1 + height)]

    elif shape_type == 'rhombus':
        # Ромб: точки по центрам воображаемого прямоугольника
        return [
            (x1 + dx/2, y1),      # верх
            (x2, y1 + dy/2),      # право
            (x1 + dx/2, y2),      # низ
            (x1, y1 + dy/2)       # лево
        ]
    return []

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    radius = 15
    curr_color = BLUE
    curr_tool = 'brush' 
    shapes = [] 
    drawing = False
    start_pos = (0, 0)

    while True:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: curr_color = RED
                if event.key == pygame.K_2: curr_color = GREEN
                if event.key == pygame.K_3: curr_color = BLUE
                
                # Выбор инструментов
                if event.key == pygame.K_b: curr_tool = 'brush'
                if event.key == pygame.K_r: curr_tool = 'rect'
                if event.key == pygame.K_c: curr_tool = 'circle'
                if event.key == pygame.K_e: curr_tool = 'eraser'
                # Новые фигуры
                if event.key == pygame.K_s: curr_tool = 'square'
                if event.key == pygame.K_t: curr_tool = 'right_tri'
                if event.key == pygame.K_l: curr_tool = 'equi_tri'
                if event.key == pygame.K_h: curr_tool = 'rhombus'
                
                if event.key == pygame.K_z:
                    shapes.clear()  
                                
                if event.key == pygame.K_ESCAPE: return

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if curr_tool in ['brush', 'eraser']:
                    color = BLACK if curr_tool == 'eraser' else curr_color
                    shapes.append({'type': 'brush', 'color': color, 'pos': event.pos, 'radius': radius})

            if event.type == pygame.MOUSEMOTION:
                if drawing and curr_tool in ['brush', 'eraser']:
                    color = BLACK if curr_tool == 'eraser' else curr_color
                    shapes.append({'type': 'brush', 'color': color, 'pos': event.pos, 'radius': radius})

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    if curr_tool in ['rect', 'circle', 'square', 'right_tri', 'equi_tri', 'rhombus']:
                        shapes.append({
                            'type': curr_tool, 
                            'color': curr_color, 
                            'start': start_pos, 
                            'end': event.pos
                        })
                drawing = False

        # Отрисовка всех сохраненных фигур
        for shape in shapes:
            if shape['type'] == 'brush':
                pygame.draw.circle(screen, shape['color'], shape['pos'], shape['radius'])
            elif shape['type'] == 'rect':
                r = pygame.Rect(shape['start'], (shape['end'][0]-shape['start'][0], shape['end'][1]-shape['start'][1]))
                r.normalize()
                pygame.draw.rect(screen, shape['color'], r, 2)
            elif shape['type'] == 'circle':
                rad = int(math.hypot(shape['start'][0] - shape['end'][0], shape['start'][1] - shape['end'][1]))
                pygame.draw.circle(screen, shape['color'], shape['start'], rad, 2)
            else:
                # Рисование полигонов (квадрат, треугольники, ромб)
                pts = get_points(shape['type'], shape['start'], shape['end'])
                if pts: pygame.draw.polygon(screen, shape['color'], pts, 2)

        # Предпросмотр во время перетаскивания мыши
        if drawing:
            if curr_tool == 'rect':
                r = pygame.Rect(start_pos, (mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                r.normalize()
                pygame.draw.rect(screen, curr_color, r, 1)
            elif curr_tool == 'circle':
                rad = int(math.hypot(start_pos[0] - mouse_pos[0], start_pos[1] - mouse_pos[1]))
                pygame.draw.circle(screen, curr_color, start_pos, rad, 1)
            elif curr_tool in ['square', 'right_tri', 'equi_tri', 'rhombus']:
                pts = get_points(curr_tool, start_pos, mouse_pos)
                if pts: pygame.draw.polygon(screen, curr_color, pts, 1)

        pygame.display.set_caption(f"Tool: {curr_tool} | Color: {curr_color}")
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()