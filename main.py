import pygame
from config import *

# Initialize pygame and screen before importing other stuff
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import snow as _
import fire as _
import deep_snow as _
import grass
import water as _
import ice as _

from player import Player
from map import Map

clock = pygame.time.Clock()
dt = 0.0

# Group containing all sprites
all_sprites = pygame.sprite.LayeredUpdates()

# the background (map)
map = Map(all_sprites)
map.make_map([50, 10, 10, 10, 10, 10])

# the player
player = Player(all_sprites)

ice_time_left = 0.0

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    screen.fill("black")

    if ice_time_left > 0:
        ice_time_left -= dt
    if ice_time_left <= 0:
        ice_time_left = 0
        map.speed = PLAYER_SPEED

    all_sprites.update(dt, keys)
    all_sprites.draw(screen)

    for s in map.player_collide("snow"):
        map.set_tile(s.position[0], s.position[1], grass.Grass())
        player.score += 1
    for f in map.player_collide("fire"):
        map.set_tile(f.position[0], f.position[1], grass.Grass())
        player.score = 0
    for w in map.player_collide("water"):
        map.set_tile(w.position[0], w.position[1], grass.Grass())
        player.score //= 2
    for d in map.player_collide("deep_snow"):
        map.set_tile(d.position[0], d.position[1], grass.Grass())
        player.score += 4
    for i in map.player_collide("ice"):
        map.speed = PLAYER_SPEED * 6
        ice_time_left = 4.0
    
    map.redraw()
    
    
    draw_text(screen, f'Score: {player.score}', (0, 0), (255, 255, 255), SCREEN_HEIGHT // 8)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
