import pygame
from config import *

# Initialize pygame and screen before importing other stuff
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import snow

from player import Player
from map import Map

clock = pygame.time.Clock()
dt = 0.0

# Group containing all sprites
all_sprites = pygame.sprite.LayeredUpdates()

# the background (map)
map = Map(all_sprites)

# the player
player = Player(all_sprites)

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    screen.fill("black")

    all_sprites.update(dt, keys)
    all_sprites.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
