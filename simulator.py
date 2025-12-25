"""
simulator.py

The main entry point for the Traffic Junction Simulator.
This script initializes the Pygame window and runs the main game loop,
coordinating between logic updates and visual rendering.

Usage:
    Run this script to start the simulation.
    Ensure traffic_config.py and traffic_logic.py are in the same directory.
"""

import pygame
import sys
import traffic_logic
import traffic_visuals
from traffic_config import *

# Initialize Pygame engine
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Junction Simulator - Priority Queue Edition")

# --- Main Simulation Loop ---
running = True
clock = pygame.time.Clock()

print("--------------------------------------------------")
print("Traffic Simulator Started.")
print(f"Resolution: {WIDTH}x{HEIGHT}")
print("Press Close [X] to exit.")
print("--------------------------------------------------")

while running:
    # 1. Event Handling
    # Check for quit events (clicking the X button)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Logic Update Step
    # Read inputs, update traffic lights, move cars
    traffic_logic.read_lane_files()
    traffic_logic.update_lights_logic()
    traffic_logic.process_vehicles()
    
    # 3. Visualization Step
    # Clear screen (implicitly done by drawing over) and render new state
    traffic_visuals.draw_road_layout(screen)
    traffic_visuals.draw_traffic_lights(screen)
    traffic_visuals.draw_vehicles(screen)
    traffic_visuals.draw_stats_panel(screen)
    
    # 4. Physics/Time Step
    # Limit frame rate to 60 FPS and get delta time (dt) for smooth movement
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    traffic_logic.update_moving_vehicles(dt)
    
    # Update the display surface to show the new frame
    pygame.display.flip()

# Cleanup on exit
pygame.quit()
sys.exit()
