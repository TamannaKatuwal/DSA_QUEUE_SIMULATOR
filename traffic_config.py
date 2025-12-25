# traffic_config.py
import pygame

# Dimensions
WIDTH, HEIGHT = 800, 800

# Colors (Premium Palette)
WHITE = (240, 240, 245)
BLACK = (20, 20, 30)
GRAY = (50, 50, 50)
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (0, 123, 255)
YELLOW = (255, 193, 7)
ORANGE = (253, 126, 20)

# Environment Colors
GRASS_COLOR = (34, 139, 34)
ROAD_COLOR = (50, 50, 55)
ROAD_BORDER = (80, 80, 90)
GHOST_WHITE = (248, 248, 255, 200)

# Lane Configuration
LANE_FILES = {
    'A': 'lane_a.txt',
    'B': 'lane_b.txt',
    'C': 'lane_c.txt',
    'D': 'lane_d.txt'
}

# Logic Constants
AL2_PRIORITY_THRESHOLD = 10
AL2_NORMAL_THRESHOLD = 5

# Vehicle Movement
MOVE_SPEED = 250.0  
MIN_GAP = 0.8       # Faster throughput
