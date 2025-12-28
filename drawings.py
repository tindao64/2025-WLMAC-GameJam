# All drawings and stuff

import pygame
from config import *
import random

player_up = pygame.image.load("player/up.png").convert_alpha()
player_down = pygame.image.load("player/down.png").convert_alpha()
player_left = pygame.image.load("player/left.png").convert_alpha()
player_right = pygame.image.load("player/right.png").convert_alpha()

ball_small = pygame.image.load("player/small_ball.png").convert_alpha()
ball_med = pygame.image.load("player/med_ball.png").convert_alpha()
ball_big = pygame.image.load("player/big_ball.png").convert_alpha()

fire1 = pygame.image.load("tiles/fire1.png").convert_alpha()
fire2 = pygame.image.load("tiles/fire2.png").convert_alpha()

water1 = pygame.image.load("tiles/water1.png").convert_alpha()
water2 = pygame.image.load("tiles/water2.png").convert_alpha()

snow_thin1 = pygame.image.load("tiles/snow_thin1.png").convert_alpha()
snow_thin2 = pygame.image.load("tiles/snow_thin2.png").convert_alpha()
snow_thick1 = pygame.image.load("tiles/snow_thick1.png").convert_alpha()
snow_thick2 = pygame.image.load("tiles/snow_thick2.png").convert_alpha()

grass = pygame.image.load("tiles/grass.png").convert_alpha()

ice = pygame.image.load("tiles/ice.png").convert_alpha()

heart = pygame.image.load("misc/heart.png").convert_alpha()

def make_player_img(dir: Direction, score: int) -> pygame.Surface:
    snow = None
    if score >= PLAYER_SMALL_BALL_THRESHOLD:
        snow = pygame.transform.scale(ball_small.copy(), (PLAYER_DIMENSION * 2//3, PLAYER_DIMENSION * 2//3))
    if score >= PLAYER_MEDIUM_BALL_THRESHOLD:
        snow = pygame.transform.scale(ball_med.copy(), (PLAYER_DIMENSION * 2//3, PLAYER_DIMENSION * 2//3))
    if score >= PLAYER_BIG_BALL_THRESHOLD:
        snow = pygame.transform.scale(ball_big.copy(), (PLAYER_DIMENSION * 2//3, PLAYER_DIMENSION * 2//3))

    match dir:
        case Direction.UP:
            player = pygame.transform.scale(player_up.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))
            if snow is not None:
                surf = pygame.Surface((PLAYER_DIMENSION, PLAYER_DIMENSION)).convert_alpha()
                surf.fill((0, 0, 0, 0))
                surf.blit(snow, (PLAYER_DIMENSION // 6, 0))
                surf.blit(player, (0, 0))
        case Direction.DOWN: 
            player = pygame.transform.scale(player_down.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))
            if snow is not None: player.blit(snow, (PLAYER_DIMENSION // 6, PLAYER_DIMENSION // 3))
        case Direction.LEFT: 
            player = pygame.transform.scale(player_left.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))
            if snow is not None: player.blit(snow, (0, PLAYER_DIMENSION // 6))
        case Direction.RIGHT: 
            player = pygame.transform.scale(player_right.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))
            if snow is not None: player.blit(snow, (PLAYER_DIMENSION // 3, PLAYER_DIMENSION // 6))
    
    return player

def make_snow_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([snow_thin1, snow_thin2]).copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_deep_snow_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([snow_thick1, snow_thick2]).copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_fire_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([fire1, fire2]).copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_water_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([water1, water2]).copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_ice_img() -> pygame.Surface:
    return pygame.transform.scale(ice.copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_grass_img() -> pygame.Surface:
    return pygame.transform.scale(grass.copy(), (TILE_DIMENSION, TILE_DIMENSION))

def make_hearts(count: int) -> pygame.Surface:
    surf = pygame.Surface((TILE_DIMENSION * (2 * count) // 2 + 1, TILE_DIMENSION // 2)).convert_alpha()
    surf.fill((0, 0, 0, 0))
    scaled_heart = pygame.transform.scale(heart, (TILE_DIMENSION // 2, TILE_DIMENSION // 2))
    for i in range(count):
        surf.blit(scaled_heart, (i * TILE_DIMENSION, 0))
    return surf

