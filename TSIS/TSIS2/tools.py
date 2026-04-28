import math
import pygame

# Цвета
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

def get_points(shape_type, start, end):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1

    if shape_type == 'square':
        side = max(abs(dx), abs(dy))
        sx = x1 if x2 > x1 else x1 - side
        sy = y1 if y2 > y1 else y1 - side
        return [(sx, sy), (sx + side, sy), (sx + side, sy + side), (sx, sy + side)]

    elif shape_type == 'right_tri':
        return [(x1, y1), (x1, y2), (x2, y2)]

    elif shape_type == 'equi_tri':
        height = dy
        side = abs(height * 2 / math.sqrt(3))
        return [(x1, y1), (x1 - side/2, y1 + height), (x1 + side/2, y1 + height)]

    elif shape_type == 'rhombus':
        return [(x1 + dx/2, y1), (x2, y1 + dy/2), (x1 + dx/2, y2), (x1, y1 + dy/2)]
    return []

def flood_fill(surface, start_pos, fill_color):
    width, height = surface.get_size()
    target_color = surface.get_at(start_pos)
    if target_color == fill_color:
        return

    pixels = pygame.PixelArray(surface)
    stack = [start_pos]
    fill_rgb = surface.map_rgb(fill_color)
    target_rgb = surface.map_rgb(target_color)

    while stack:
        x, y = stack.pop()
        if 0 <= x < width and 0 <= y < height:
            if pixels[x, y] == target_rgb:
                pixels[x, y] = fill_rgb
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    del pixels