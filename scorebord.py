import pygame
from constants import *
import json
class ScoreEntry():
    def __init__(self, score, initials):
        self.score = score
        self.initials = str(initials)


class ScoreBoard():
    def __init__(self, scorefile):
        self.scorefile = scorefile
        self.scores = self.load_scores()
        self.is_dead = False
        self.player_initials = ""
        self.score_processed = False
    def get_player_initials(self):
    # Initialize empty initials
        initials = ""
        input_active = True
    
        while input_active and len(initials) < 3:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif len(initials) < 3:
                        # Only accept letters
                        if event.unicode.isalpha():
                            initials += event.unicode.upper()
    
    # Pad with spaces if needed
        while len(initials) < 3:
            initials += " "
    
        return initials
    
    def add_score(self, score, initials):
        new_entry = ScoreEntry(score, str(initials))
        self.scores.append(new_entry)
        self.scores.sort(key=lambda x: x.score, reverse=True)
        if len(self.scores) > 10:
            self.scores = self.scores[:10]
        self.save_scores()
    def load_scores(self):
        try:
            with open(self.scorefile, "r") as file:
                return [ScoreEntry(**entry) for entry in json.load(file)]
        except FileNotFoundError:
            return []
    
    def save_scores(self):
        with open(self.scorefile, "w") as file:
            json.dump(
                [{'score': entry.score, 'initials': entry.initials} for entry in self.scores],
                file
            )
    def display_scores(self):
        score_display = []
        for position, entry in enumerate(self.scores, start=1):
            score_line = f"{position}. {entry.initials} - {entry.score}"
            score_display.append(score_line)
        return score_display


    def draw(self, screen, font):
    # Vertical starting position
        base_y_position = 100
    # Vertical space between each score entry
        line_spacing = 40

        for index, score_entry in enumerate(self.scores):
        # Render the text for each score
            score_text = font.render(f"#{index + 1}: {score_entry.initials} - {score_entry.score}", True, (255, 255, 255))

        # Get the width of the rendered text for center alignment
            text_width = score_text.get_width()

        # Calculate position and draw text
            screen.blit(score_text, (SCREEN_WIDTH // 2 - text_width // 2, base_y_position + index * line_spacing))

    # For initial input prompt and display
        if self.is_dead and not self.score_processed:
        # Render and draw the "Enter your initials:" prompt
            prompt = font.render("Enter your initials:", True, (255, 255, 255))
            screen.blit(prompt, (100, 20))

        # Render and draw the current input for initials
            current_input = font.render(self.player_initials, True, (255, 255, 255))
            screen.blit(current_input, (100, 50))



    def set_game_over(self, is_dead, score):
        if is_dead and not self.score_processed:
            self.score_processed = True
            self.player_initials = self.get_player_initials()
            self.add_score(score, self.player_initials)