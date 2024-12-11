import pygame
import time
from constants import *
import os
import random
from playerandfood import Square, Player, Poison
from sound import *
from scorebord import ScoreBoard
from portals import PortalPair


def main():
    (3840 - 1680) / 2
    (1600 - 1420) / 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = "1080,90"
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH , 1420))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
     
    player = Player(STARTING_X, STARTING_Y, GRID_SIZE)
    
    square_x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
    square_y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
    poison = Poison(square_x, square_y, GRID_SIZE)
    food = Square(square_x, square_y, GRID_SIZE)
    font = pygame.font.Font(None, 36) 
    game_state = 'menu'
    
    while game_state != 'exit':
        if game_state == 'menu':
            display_menu(screen, font)
            game_state = handle_menu_events()
        elif game_state == 'playing':
            game_state = run_game_loop(screen, clock, player, food, font, poison)

def display_menu(screen, font):
    # Fill the screen with a color (e.g., black for background)
    sky_blue = (135, 206, 235)
    grass_green = (34, 139, 34)
    sun_yellow = (255, 223, 0)
    screen.fill(sky_blue)
    pygame.draw.rect(screen, grass_green, pygame.Rect(0, 1000, 1690, 420))
    pygame.draw.circle(screen, sun_yellow, (1580, 100), 100)
    
    # Render the game title
    title_text = font.render("SNAKE", True, (255, 0, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)
    
    # Render Menu Options (e.g., "Start" and "Exit")
    start_text = font.render("Press Enter to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_text, start_rect)
    
    exit_text = font.render("Press Esc to Quit", True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(exit_text, exit_rect)
    
    # Update Display
    pygame.display.flip()

def handle_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Proper handle to allow window close
            return 'exit'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'playing'
            elif event.key == pygame.K_ESCAPE:
                return 'exit'
    return 'menu'
    

def run_game_loop(screen, clock, player, food, font, poison):
    import sys
    start_time = time.time()
    is_paused = False
    next_milestone = 10
    scoreboard = ScoreBoard("scores.json")
    score = 0
    running = True
    occupied_positions = set()
    poison_objects = []
# Create and add a Poison instance
    poison_instance = Poison(poison.grid_x, poison.grid_y, GRID_SIZE)
    poison_objects.append(poison_instance)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_paused = not is_paused
                elif player.is_dead:
                    if len(scoreboard.player_initials) <3:  # Only accept input if name isn't complete
                        if event.key >= pygame.K_a and event.key <= pygame.K_z:
                            scoreboard.player_initials += event.unicode.upper()
                    elif len(scoreboard.player_initials) == 3:  # Only exit after name is complete
                        restart, new_game = show_high_scores(screen, font)
                        if restart:
                            player = new_game
                            score = 0
                            player.score = 0
                            start_time = time.time()
                            food.reset()
                            player.score = 0
                        else:
                            running = False
        if not is_paused:

            if score >= next_milestone:
                player.increase_delay()
                next_milestone += 10 
            if player.grid_x == food.grid_x and player.grid_y == food.grid_y:
                food.grid_x = random.randint(0, (SCREEN_WIDTH  // GRID_SIZE) - 1)
                food.grid_y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
                food.place_food()
                player.grow()
                score += 1
                player.score += 1
            for poison_instance in poison_objects:  # Iterate through each Poison instance
                for (poison_x, poison_y) in poison_instance.positions:  # Check each position in the Poison instance
                    if player.grid_x == poison_x and player.grid_y == poison_y:
                        player.is_dead = True
            elapsed_time = time.time() - start_time
            dt = clock.tick(60) / 1000
            screen.fill((0, 100, 0))
            player.update(dt)
            food.update()
            player.draw(screen)
            food.draw(screen)
            poison.draw(screen)
        
            text_surface = font.render("Score: " + str(score), True, (0, 0, 0))
            screen.blit(text_surface, (10, 10))
            elapsed_time_text = font.render(f"Time: {int(elapsed_time)}s", True, (0, 0, 0))
            screen.blit(elapsed_time_text, (10, 60))
        
        pygame.display.flip()
        
        font = pygame.font.Font(None, 36) 
        if player.is_dead:
            if not scoreboard.score_processed:
                player_name = show_high_scores(screen, font, score)
                if player_name:
                    scoreboard.add_score(player_name, score)
                    scoreboard.score_processed = True
                    running = False
    pygame.quit()
    sys.exit()
def run_game(screen):
    running = True
    screen = pygame.display.set_mode((SCREEN_WIDTH , 1420))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
     
    
    player = Player(STARTING_X, STARTING_Y, GRID_SIZE)
    
    square_x = random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1)
    square_y = random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1)
    food = Square(square_x, square_y, GRID_SIZE)
    poison = Poison(square_x, square_y, GRID_SIZE)
    font = pygame.font.Font(None, 36) 
    while running:
        running = run_game_loop(screen, clock, player, food, font, poison)
        # Consider re-initializing game state here if needed

def show_high_scores(screen, font, score):
    running = True
    scoreboard = ScoreBoard("scores.json")
    initials = scoreboard.get_player_initials()
    scoreboard.add_score(score, initials)
    while running:
        screen.fill((0, 0, 0))  # Black background
        
        # Draw high scores title
        title_text = font.render("HIGH SCORES", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        # Draw the scores
        scoreboard.draw(screen, font)
        
        # Draw the prompts at bottom
        retry_text = font.render("Press ENTER to Try Again", True, (255, 255, 255))
        quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))
        screen.blit(retry_text, (SCREEN_WIDTH//2 - retry_text.get_width()//2, SCREEN_HEIGHT - 120))
        screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, SCREEN_HEIGHT - 80))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                    run_game(screen)
                    
                    return True
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.flip()
    
            

if __name__ == "__main__":
    main()