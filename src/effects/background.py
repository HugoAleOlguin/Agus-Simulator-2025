import pygame
import math

class SimpleBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.time = 0
        self.grid_size = 40
        self.base_color = (180, 180, 180)
        self.line_color = (190, 190, 190)
        
    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        # Color base del fondo
        surface.fill(self.base_color)
        
        # Dibujar grid suave
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(surface, self.line_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(surface, self.line_color, (0, y), (self.width, y))
