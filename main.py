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
import wood

from player import Player
from santa import Santa
from evil_santa import EvilSanta
from map import Map
import drawings
import time
import tile
import random
import sys

clock = pygame.time.Clock()
dt = 0.0

# Group containing all sprites
all_sprites = pygame.sprite.LayeredUpdates()

tile_weights = {
    "snow": 50,
    "fire": 10,
    "deep_snow": 0,
    "grass": 10,
    "water": 10,
    "ice": 10,
    "wood": 0
}

tile_weight_list = [tile_weights[x] for x in tile.tile_types]
deep_snow_index = tile.tile_types.index("deep_snow")

def tile_generator(pos):
    x, y = pos
    tile_weight_copy = tile_weight_list.copy()
    tile_weight_copy[deep_snow_index] += y * 50 // MAP_HEIGHT
    choice = random.choices(tile.tile_types, weights=tile_weight_copy)
    return choice[0]


# the background (map)
map = Map(all_sprites)
map.make_map(tile_generator)

for y in range(3):
    for x in range(MAP_WIDTH):
        map.set_tile((x, y), wood.Wood())
# the player
player = Player(all_sprites)

santa = Santa(all_sprites)
evil_santa = EvilSanta(all_sprites)

ice_time_left = 0.0
play_time_left = PLAY_TIME

screen.blit(drawings.make_how_to_play(), (0, 0))
pygame.display.flip()

wait = True
while wait:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            wait = False

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if player.health <= 0:
        draw_text(screen, "YOU LOSE!", (0, 0), "white", SCREEN_HEIGHT // 4, "red")
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        exit()

    keys = pygame.key.get_pressed()

    play_time_left -= dt
    if play_time_left <= 0:
        draw_text(screen, f"Game Over! Score: {santa.total_score}", (0, 0), "white", SCREEN_HEIGHT // 5, "blue")
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        exit()

    screen.fill("black")

    if ice_time_left > 0:
        ice_time_left -= dt
    if ice_time_left <= 0:
        ice_time_left = 0
        player.speed = PLAYER_SPEED

    all_sprites.update(dt, keys, player.rect)

    # Draw all sprites offset so the player is always in the middle of the screen
    offset_x = SCREEN_WIDTH // 2 - player.rect.centerx
    offset_y = SCREEN_HEIGHT // 2 - player.rect.centery
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    
    if map.has_group("snow"):
        for s in pygame.sprite.spritecollide(player, map.get_group("snow"), False):
            if (player.score < PLAYER_SNOWBALL_CAP):
                map.set_tile(s.position, grass.Grass())
                player.score += 1
    if map.has_group("fire"):
        for f in pygame.sprite.spritecollide(player, map.get_group("fire"), False):
            map.set_tile(f.position, grass.Grass())
            player.score = 0
            player.health -= 1
    if map.has_group("water"):
        for w in pygame.sprite.spritecollide(player, map.get_group("water"), False):
            map.set_tile(w.position, grass.Grass())
            player.score //= 2
    if map.has_group("deep_snow"):
        for d in pygame.sprite.spritecollide(player, map.get_group("deep_snow"), False):
            if player.score < PLAYER_SNOWBALL_CAP:
                map.set_tile(d.position, grass.Grass())
                player.score += 4
    if map.has_group("ice"):
        for i in pygame.sprite.spritecollide(player, map.get_group("ice"), False):
            player.speed = PLAYER_SPEED * ICE_SPEED_MULT
            ice_time_left = ICE_SPEED_TIME
    
    if player.rect.colliderect(santa.rect) and player.score > 0:
        santa.total_score += player.score
        player.score = 0
    
    if player.rect.colliderect(evil_santa.rect):
        player.score = 0
        player.health -= 1
        evil_santa.go_to_random()
    
    map.redraw()
    
    
    draw_text(screen, f'Score: {santa.total_score}', (0, 0), "white", SCREEN_HEIGHT // 8, "black")
    draw_text(screen, f'Time: {int(play_time_left)}s', (0, SCREEN_HEIGHT // 8), "white", SCREEN_HEIGHT // 8, "black")
    draw_text(screen, f'Snowball: {player.score}', (0, SCREEN_HEIGHT // 4), "white", SCREEN_HEIGHT // 8, "black")
    hearts = drawings.make_hearts(player.health)
    screen.blit(hearts, (0, SCREEN_HEIGHT * 3//8))
    if player.score >= PLAYER_SNOWBALL_CAP:
        draw_text(screen, 'Snowball Too Big!', (0, SCREEN_HEIGHT // 2), "white", SCREEN_HEIGHT // 8, "red")

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
