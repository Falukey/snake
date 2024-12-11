import pygame
import os

os.environ['SDL_AUDIODRIVER'] = 'alsa'  # Make sure 'dsp' is appropriate for your system

try:
    pygame.mixer.init()
    bite_sound = pygame.mixer.Sound('apple_bite.wav')
except pygame.error as e:
    print(f"Error with audio setup: {e}")
    bite_sound = None  # Proceed without sound


def apple_eaten():
    if bite_sound is not None:
        bite_sound.play()

