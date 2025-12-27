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

snow_img = pygame.surface.Surface((TILE_DIMENSION, TILE_DIMENSION)).convert()
snow_img.fill("snow")
pygame.draw.rect(
    snow_img,
    "snow4",
    (0, 0, TILE_DIMENSION, TILE_DIMENSION),
    width=(TILE_DIMENSION // 10)
)
