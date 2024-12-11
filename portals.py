import pygame
import time
from constants import *
import random

class PortalPair:
    def __init__(self, grid_size, screen):
        self.grid_size = grid_size
        pos1 = self.get_random_position()
        pos2 = self.get_random_position()
        while pos2 == pos1:
            pos2 = self.get_random_position()
        
        
        self.portal1 = Portal(pos1[0], pos1[1], grid_size)
        self.portal2 = Portal(pos2[0], pos2[1], grid_size)
    def draw(self, screen):
        self.portal1.draw(screen)    
        self.portal2.draw(screen)
    
    def get_random_position(self):
        max_x = (SCREEN_WIDTH // self.grid_size) - 1  # 41
        max_y = (SCREEN_HEIGHT // self.grid_size) - 1  # 34
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        return (x, y)
    def check_portal_collision(self, player_x, player_y):
    # Check if player position matches portal1's position
        if (player_x == self.portal1.grid_x and player_y == self.portal1.grid_y):
            return (self.portal2.grid_x, self.portal2.grid_y)
        elif (player_x == self.portal2.grid_x and player_y == self.portal2.grid_y):
            return (self.portal1.grid_x, self.portal1.grid_y)
        
class Portal:
    def __init__(self, grid_x, grid_y, grid_size):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_size = grid_size
        
    def draw(self, screen):
        # Draw a single portal
        portal_rect = pygame.Rect(
            self.grid_x * self.grid_size,
            self.grid_y * self.grid_size,
            self.grid_size,
            self.grid_size
        )
        pygame.draw.rect(screen, (128, 0, 128), portal_rect)