import pygame
pygame.init()
from config import *

# Initialize pygame and screen before importing other stuff
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import snow
import fire as _
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
    "grass": 10,
    "water": 10,
    "ice": 10,
    "wood": 0
}

tile_weight_list = [tile_weights[x] for x in tile.tile_types]

def tile_generator(pos) -> tile.Tile:
    choice = random.choices(tile.tile_types, weights=tile_weight_list)
    
    type = choice[0]
    if type == "snow":
        x, y = pos
        snow_weights = [
            50,
            y * 100 // MAP_HEIGHT,
            y * 100 // MAP_HEIGHT,
            y * 100 // MAP_HEIGHT
        ]
        snow_types = [0, 1, 2, 3]
        choice = random.choices(snow_types, weights=snow_weights)
        return snow.Snow(choice[0])
    return tile.make_tile(type)


# the background (map)
map = Map(all_sprites)
map.make_map(tile_generator)

for y in range(3):
    for x in range(MAP_WIDTH):
        map.set_tile((x, y), wood.Wood())
# the player
player = Player(all_sprites)

santa = Santa(all_sprites)
evil_santas = pygame.sprite.Group()
EvilSanta(all_sprites, evil_santas)

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
    clock.tick(60)

last_collisions: set[tile.Tile] = set()

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    if player.health <= 0:
        draw_text(screen, "YOU LOSE!", (0, 0), "white", SCREEN_HEIGHT // 4, "red")
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    keys = pygame.key.get_pressed()

    play_time_left -= dt
    if play_time_left <= 0:
        draw_text(screen, f"Game Over! Score: {santa.total_score}", (0, 0), "white", SCREEN_HEIGHT // 5, "blue")
        pygame.display.flip()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    screen.fill("black")

    if ice_time_left > 0:
        ice_time_left -= dt
        player.move(dt)
    else:
        ice_time_left = 0
        player.speed = PLAYER_SPEED

    all_sprites.update(dt, keys, player.rect)

    # Draw all sprites offset so the player is always in the middle of the screen
    offset_x = SCREEN_WIDTH // 2 - player.rect.centerx
    offset_y = SCREEN_HEIGHT // 2 - player.rect.centery
    for sprite in all_sprites:
        screen.blit(sprite.image, (sprite.rect.x + offset_x, sprite.rect.y + offset_y))

    # Do collision detection
    all_collisions = set(pygame.sprite.spritecollide(player, map.get_all_tiles(), False))
    all_new_collisions = all_collisions.copy()
    type_collisions: dict[str, set] = {x: set() for x in tile.tile_types}

    # Store only new collisions
    for old_collision in last_collisions:
        if old_collision in all_new_collisions:
            all_new_collisions.remove(old_collision)
    
    last_collisions = all_collisions
    
    # Filter collisions into types
    for collision in all_new_collisions:
        type_collisions[collision.type()].add(collision)
    
    for s in type_collisions["snow"]:
        s: snow.Snow
        player.score += 1
        s.set_thickness(s.thickness - 1)
        if s.thickness < 0:
            map.set_tile(s.position, grass.Grass())
    for f in type_collisions["fire"]:
        player.score = 0
        player.health -= 1
    for i in type_collisions["ice"]:
        player.speed = PLAYER_SPEED * ICE_SPEED_MULT
        ice_time_left = ICE_SPEED_TIME
    for w in type_collisions["water"]:
        player.score //= 2
    
    if player.rect.colliderect(santa.rect) and player.score > 0:
        santa.total_score += player.score
        player.score = 0
        if random.randint(1, 3) == 1:
            EvilSanta(all_sprites, evil_santas)
    
    for evil_santa in pygame.sprite.spritecollide(player, evil_santas, False):
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
