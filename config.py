# Configuration and common things

from enum import Enum
import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Adjust divisor to adjust player size
PLAYER_DIMENSION = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 8

class Direction(Enum):
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

KEY_UP = pygame.K_w
KEY_LEFT = pygame.K_a
KEY_DOWN = pygame.K_s
KEY_RIGHT = pygame.K_d

PLAYER_SPEED = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 4 # pixels per second
