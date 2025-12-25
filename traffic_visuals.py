# traffic_visuals.py
import pygame
import math
import time
from traffic_config import *
import traffic_logic

# helper to draw lines that are dashed
def draw_dashed_line(surface, color, start_pos, end_pos, width=1, dash_length=20):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if x1 == x2:
        y_coords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        for i in range(0, len(y_coords), 2):
            if i+1 < len(y_coords):
                pygame.draw.line(surface, color, (x1, y_coords[i]), (x1, y_coords[i+1]), width)
    elif y1 == y2:
        x_coords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        for i in range(0, len(x_coords), 2):
            if i+1 < len(x_coords):
                pygame.draw.line(surface, color, (x_coords[i], y1), (x_coords[i+1], y1), width)

def draw_road_layout(screen):
    screen.fill(GRASS_COLOR)
    
    # Draw Roads
    pygame.draw.rect(screen, ROAD_COLOR, (300, 0, 200, 800))   # A/B
    pygame.draw.rect(screen, ROAD_COLOR, (0, 300, 800, 200))   # C/D
    
    # Intersections Borders
    pygame.draw.line(screen, ROAD_BORDER, (300, 0), (300, 800), 2)
    pygame.draw.line(screen, ROAD_BORDER, (500, 0), (500, 800), 2)
    pygame.draw.line(screen, ROAD_BORDER, (0, 300), (800, 300), 2)
    pygame.draw.line(screen, ROAD_BORDER, (0, 500), (800, 500), 2)

    # Dashed Lane Dividers
    draw_dashed_line(screen, WHITE, (400, 0), (400, 800), 2)
    draw_dashed_line(screen, WHITE, (366, 0), (366, 300), 1)
    draw_dashed_line(screen, WHITE, (333, 0), (333, 300), 1)
    
    draw_dashed_line(screen, WHITE, (433, 500), (433, 800), 1)
    draw_dashed_line(screen, WHITE, (466, 500), (466, 800), 1)
    
    draw_dashed_line(screen, WHITE, (0, 400), (800, 400), 2)
    draw_dashed_line(screen, WHITE, (0, 366), (300, 366), 1)
    draw_dashed_line(screen, WHITE, (0, 333), (300, 333), 1)
    
    draw_dashed_line(screen, WHITE, (500, 433), (800, 433), 1)
    draw_dashed_line(screen, WHITE, (500, 466), (800, 466), 1)

    # Stop Lines (Thick White)
    pygame.draw.line(screen, WHITE, (300, 300), (500, 300), 4) # Top
    pygame.draw.line(screen, WHITE, (300, 500), (500, 500), 4) # Bottom
    pygame.draw.line(screen, WHITE, (300, 300), (300, 500), 4) # Left
    pygame.draw.line(screen, WHITE, (500, 300), (500, 500), 4) # Right

    font = pygame.font.SysFont("Verdana", 24, bold=True)
    
    def draw_label(text, pos):
        surf = font.render(text, True, (200, 200, 200))
        screen.blit(surf, pos)

    draw_label("A (North)", (340, 20))
    draw_label("B (South)", (340, 750))
    draw_label("C (East)", (650, 340))
    draw_label("D (West)", (50, 340))
