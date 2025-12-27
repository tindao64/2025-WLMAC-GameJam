# All drawings and stuff

import pygame
from config import *

# Temporary drawing 
# TODO: put image in
player_img = pygame.surface.Surface((PLAYER_DIMENSION, PLAYER_DIMENSION)).convert_alpha()
player_img.fill("red")
pygame.draw.rect( # Draw blue in direction player is facing
    player_img, # surface
    "blue", # color
    (0, 0, PLAYER_DIMENSION, PLAYER_DIMENSION // 3) # (x, y, w, h)
)

map_img = pygame.surface.Surface((SCREEN_WIDTH * 3, SCREEN_HEIGHT * 3)).convert_alpha()
map_img.fill("green")
pygame.draw.rect( # draw yellow thing in middle
    map_img,
    "yellow",
    (SCREEN_WIDTH * 3//2, SCREEN_HEIGHT * 3//2, PLAYER_DIMENSION, PLAYER_DIMENSION)
)
