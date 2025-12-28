# Configuration

from enum import Enum
import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Adjust divisor to adjust player size
PLAYER_DIMENSION = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 8

KEY_UP = pygame.K_w
KEY_LEFT = pygame.K_a
KEY_DOWN = pygame.K_s
KEY_RIGHT = pygame.K_d

TILE_DIMENSION = PLAYER_DIMENSION * 3 // 2

MAP_WIDTH = 6 # tiles
MAP_HEIGHT = 30

PLAYER_SPEED = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 4 # pixels per second
ICE_SPEED_MULT = 25
ICE_SPEED_TIME = 0.5

PLAYER_SMALL_BALL_THRESHOLD = 1
PLAYER_MEDIUM_BALL_THRESHOLD = 20
PLAYER_BIG_BALL_THRESHOLD = 40

PLAYER_HEALTH = 3
PLAY_TIME = 120 # seconds

# Common things
# Don't change these; these aren't config!

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# Drawing order: bigger number goes above smaller number
# Draws player on top of map, not other way around
MAP_LAYER = 0
PLAYER_LAYER = 1

def draw_text(surf: pygame.Surface, text: str, dest, color, size, bg = None):
    font = pygame.font.SysFont(None, size)
    text_surf = font.render(text, True, color, bg)
    surf.blit(text_surf, dest)
