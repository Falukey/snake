import pygame
import time
from constants import *
import random
from portals import PortalPair

class Square():
    def __init__(self, grid_x, grid_y, grid_size, radius = GRID_SIZE / 2):
        self.grid_x = grid_x      
        self.grid_y = grid_y      
        self.grid_size = grid_size
        self.radius = radius
        self.player_positions = []  
        self.poison_objects = []
        
        
        self.screen_x = self.grid_x * self.grid_size
        self.screen_y = self.grid_y * self.grid_size
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0),
                        (self.screen_x, self.screen_y),
                        self.radius)
        pygame.draw.rect(screen, (139, 69, 19),
                 (self.grid_x * self.grid_size, self.grid_y * self.grid_size, 
                  self.grid_size, self.grid_size), width=1)
        tip = (self.grid_x * self.grid_size + self.grid_size // 2, self.grid_y * self.grid_size)

        right_curve = (self.grid_x * self.grid_size + self.grid_size, self.grid_y * self.grid_size + self.grid_size // 2)

        bottom = (self.grid_x * self.grid_size + self.grid_size // 2, self.grid_y * self.grid_size + self.grid_size)

        left_curve = (self.grid_x * self.grid_size, self.grid_y * self.grid_size + self.grid_size // 2)

        leaf_points = [tip, right_curve, bottom, left_curve]

        pygame.draw.polygon(screen, (0, 255, 0), leaf_points)



    def update(self):
        self.screen_x = self.grid_x * self.grid_size
        self.screen_y = self.grid_y * self.grid_size

    def pixel_based_collision(self, other_square):
        square_rect = pygame.Rect(self.screen_x, self.screen_y, self.grid_size, self.grid_size)
        other_rect = pygame.Rect(other_square.screen_x, other_square.screen_y, other_square.grid_size, other_square.grid_size)
        return square_rect.colliderect(other_rect)
    def get_random_position(self):
        x = random.randint(0, (SCREEN_WIDTH  // GRID_SIZE) - 1)
        y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
        return x, y
    def place_food(self):
        while True:
            x, y = self.get_random_position()
            if (x, y) not in self.get_occupied_positions():
                self.grid_x = x
                self.grid_y = y
                break

    def get_occupied_positions(self):
    # Make sure these are lists of tuples like [(x1, y1), (x2, y2), ...]
        if self.poison_objects is None:
            self.poison_objects = []
        if self.player_positions is None:
            self.player_positions = []
    
        return set(self.poison_objects) | set(self.player_positions)














class Player(Square):
    def __init__(self, grid_x, grid_y, grid_size):
        super().__init__(grid_x, grid_y, grid_size, radius=0)
        self.grid_size = grid_size
        self.segments = [(STARTING_X, STARTING_Y,)]
        self.direction = (1, 0)
        self.directions = [(1,0), (0,1), (-1,0), (0,-1)]
        self.move_timer = 0
        initial_delay = 0.35
        self.move_delay = initial_delay
        self.min_move_delay = 0.1
        self.has_moved_since_turn = False
        self.input_timer = 0
        self.input_delay = 0.3
        self.turn_count = 0
        self.max_turns = 1 
        self.last_key_state = {}
        self.is_dead = False
        self.score = 0


    def draw(self, screen):
        # Draw each segment of the snake
        for segment in self.segments:
            screen_x = segment[0] * self.grid_size
            screen_y = segment[1] * self.grid_size
            pygame.draw.rect(screen, (0, 0, 255), 
                             (screen_x, screen_y, self.grid_size, self.grid_size))
    def increase_delay(self):
        self.move_delay += 0.1


    def grow(self): 
        tail_direction = (-self.direction[0], -self.direction[1])
        last_segment = self.segments[-1]
        new_segment = (last_segment[0] + tail_direction[0], last_segment[1] + tail_direction[1])
        self.segments.append(new_segment)
        decrease_amount = 0.05
        self.move_delay = max(self.min_move_delay, self.move_delay - decrease_amount)



    def check_collision(self,):
        head = self.segments[0]
        head_x, head_y = self.segments[0]
        head_x *= GRID_SIZE
        head_y *= GRID_SIZE

    # Check collision with the boundary
        if head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0 or head_y >= SCREEN_HEIGHT:
            return True
        for segment in self.segments[1:]:
            if head == segment:
                return True
        return False

    def update(self, dt,):
        self.move_timer += dt
        self.input_timer += dt
        current_index = self.directions.index(self.direction)
        if self.check_collision():
            self.is_dead = True
        keys = pygame.key.get_pressed()
        if self.turn_count < self.max_turns and self.has_moved_since_turn:
            if keys[pygame.K_d] and not self.last_key_state.get(pygame.K_d, False):  # clockwise rotation
                new_index = (current_index + 1) % 4
                self.direction = self.directions[new_index]
                self.has_moved_since_turn = False
                self.input_timer = 0
                self.turn_count += 1
            elif keys[pygame.K_a] and not self.last_key_state.get(pygame.K_a, False):  # counter-clockwise rotation
                new_index = (current_index - 1) % 4
                self.direction = self.directions[new_index]
                self.has_moved_since_turn = False
                self.input_timer = 0
                self.turn_count += 1
        self.last_key_state[pygame.K_d] = keys[pygame.K_d]
        self.last_key_state[pygame.K_a] = keys[pygame.K_a]
        
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.has_moved_since_turn = True
            self.turn_count = 0
            for i in range(len(self.segments) - 1, 0, -1):
                self.segments[i] = self.segments[i - 1]
        
    
            head_segment = self.segments[0]


            new_x = head_segment[0] + self.direction[0]
            new_y = head_segment[1] + self.direction[1]
            self.segments[0] = (new_x, new_y)
            
             # Use the instance
            
            
    
    # Update the player's position with new_x, new_y
            self.x = new_x
            self.y = new_y







            self.grid_x, self.grid_y = self.segments[0]
            super().update()  # Update screen coordinates


class Poison(Square):
    def __init__(self, grid_x, grid_y, grid_size):
        super().__init__(grid_x, grid_y, grid_size, radius=0)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_size = grid_size
        
        occupied_positions = set()
        
        # Initialize 10 unique positions
        self.positions = []
        while len(self.positions) < 20:
            pos = self.get_random_position()
            if pos not in occupied_positions:
                occupied_positions.add(pos)
                self.positions.append(pos)
    
    def get_random_position(self):
        max_x = (SCREEN_WIDTH // self.grid_size) - 1
        max_y = (SCREEN_HEIGHT // self.grid_size) - 1
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        return (x, y)

    def draw(self, screen):
        color = (128, 0, 128)
        for pos in self.positions:
            x, y = pos
            pygame.draw.rect(screen, color, pygame.Rect(
                x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size
            ))