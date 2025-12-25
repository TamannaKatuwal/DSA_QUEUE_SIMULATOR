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

def draw_traffic_lights(screen):
    def draw_light_box(x, y, is_green, orientation='v'):
        # Traffic light box background
        box_w, box_h = (16, 40) if orientation == 'v' else (40, 16)
        pygame.draw.rect(screen, BLACK, (x - box_w//2, y - box_h//2, box_w, box_h), border_radius=4)
        
        # Colors
        r_color = RED if not is_green else (50, 0, 0)
        g_color = GREEN if is_green else (0, 50, 0)
        
        radius = 5
        if orientation == 'v':
            pygame.draw.circle(screen, r_color, (x, y - 8), radius)
            pygame.draw.circle(screen, g_color, (x, y + 8), radius)
        else:
            pygame.draw.circle(screen, r_color, (x - 8, y), radius)
            pygame.draw.circle(screen, g_color, (x + 8, y), radius)

    # Positions
    lights = traffic_logic.traffic_lights
    draw_light_box(290, 280, lights['A'] == 1, 'v')
    draw_light_box(530, 520, lights['B'] == 1, 'v')
    draw_light_box(520, 290, lights['C'] == 1, 'h')
    draw_light_box(280, 510, lights['D'] == 1, 'h')

    if traffic_logic.PRIORITY_MODE:
        # Pulsing Red Glow when in Priority Mode
        pulse = (math.sin(time.time() * 8.0) + 1.0) / 2.0
        alpha = int(pulse * 100)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (255, 69, 0, alpha), (0, 0, WIDTH, HEIGHT), 10)
        screen.blit(overlay, (0, 0))

def draw_vehicles(screen):
    queues = traffic_logic.vehicle_queues
    moving = traffic_logic.moving_vehicles
    
    # Draw Queued Vehicles
    # Lane A (Top)
    for i, v in enumerate(queues['A']):
        y = 260 - (i * 30)
        if y > -40:
            pygame.draw.rect(screen, v['color'], (370, y, 20, 28), border_radius=3)

    # Lane B (Bottom)
    for i, v in enumerate(queues['B']):
        y = 540 + (i * 30)
        if y < HEIGHT + 40:
            pygame.draw.rect(screen, v['color'], (410, y, 20, 28), border_radius=3)
            
    # Lane C (Right)
    for i, v in enumerate(queues['C']):
        x = 540 + (i * 30)
        if x < WIDTH + 40:
            pygame.draw.rect(screen, v['color'], (x, 370, 28, 20), border_radius=3)

    # Lane D (Left)
    for i, v in enumerate(queues['D']):
        x = 260 - (i * 30)
        if x > -40:
            pygame.draw.rect(screen, v['color'], (x, 410, 28, 20), border_radius=3)

    # Moving
    for mv in moving:
        pygame.draw.rect(screen, YELLOW, (mv['x'], mv['y'], mv['w'], mv['h']), border_radius=4)
        pygame.draw.rect(screen, (200, 150, 0), (mv['x']+2, mv['y']+2, mv['w']-4, mv['h']-4), border_radius=2)

def draw_stats_panel(screen):
    # HUD Configuration
    # Reduced width to 270 to fit in the top-right quadrant (500-800) without overlapping the road.
    panel_w, panel_h = 270, 150
    panel_x, panel_y = WIDTH - panel_w - 10, 20
    
    # HUD Background (Dark Blue/Gray with heavy alpha)
    hud_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(hud_surface, (10, 14, 28, 240), (0, 0, panel_w, panel_h), border_radius=10)
    # HUD Border (Cyan/Blue accent)
    pygame.draw.rect(hud_surface, (0, 191, 255), (0, 0, panel_w, panel_h), 2, border_radius=10)
    screen.blit(hud_surface, (panel_x, panel_y))
    
    # Typography
    header_font = pygame.font.SysFont("Verdana", 18, bold=True)
    mono_font = pygame.font.SysFont("Consolas", 16, bold=True)
    mini_font = pygame.font.SysFont("Verdana", 12)
    
    # 1. Header
    header_col = (0, 191, 255) # Deep Sky Blue
    t1 = header_font.render("SYSTEM STATUS", True, header_col)
    screen.blit(t1, (panel_x + 20, panel_y + 15))
    
    # 2. Priority Indicator
    is_priority = traffic_logic.PRIORITY_MODE
    status_text = "PRIORITY - LANE A" if is_priority else "NORMAL CONDITION"
    status_col = (255, 69, 0) if is_priority else (50, 205, 50) # Red-Orange vs Lime Green
    
    # Draw a "pill" background for status
    pill_rect = pygame.Rect(panel_x + 20, panel_y + 45, panel_w - 40, 28)
    pygame.draw.rect(screen, (status_col[0]//4, status_col[1]//4, status_col[2]//4), pill_rect, border_radius=6)
    pygame.draw.rect(screen, status_col, pill_rect, 1, border_radius=6)
    
    ts = mono_font.render(status_text, True, status_col)
    # Center text in pill
    screen.blit(ts, (pill_rect.centerx - ts.get_width()//2, pill_rect.centery - ts.get_height()//2))
    
    # 3. Lane Counters (Grid)
    # A B
    # C D 
    grid_y = panel_y + 85
    col_1_x = panel_x + 30
    col_2_x = panel_x + 160
    
    def draw_cell(lane, x, y):
        count = len(traffic_logic.vehicle_queues[lane])
        col = WHITE
        if count > 5: col = (255, 165, 0) # Orange warn
        if count > 10: col = (255, 50, 50) # Red critical
        
        lbl = mini_font.render(f"LANE {lane}", True, (150, 160, 180))
        val = mono_font.render(f"{count:02d}", True, col)
        
        screen.blit(lbl, (x, y))
        screen.blit(val, (x + 60, y - 2))

    draw_cell('A', col_1_x, grid_y)
    draw_cell('C', col_2_x, grid_y)
    draw_cell('B', col_1_x, grid_y + 25)
    draw_cell('D', col_2_x, grid_y + 25)
