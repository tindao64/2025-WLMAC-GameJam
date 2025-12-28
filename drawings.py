# All drawings and stuff

import pygame
from config import *
import random


import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # For development environment (outside of .exe)
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

player_up = pygame.image.load(resource_path("player/up.png")).convert_alpha() ####
player_down = pygame.image.load(resource_path("player/down.png")).convert_alpha() ####
player_left = pygame.image.load(resource_path("player/left.png")).convert_alpha() ####
player_right = pygame.image.load(resource_path("player/right.png")).convert_alpha() ####

ball_small = pygame.image.load(resource_path("player/small_ball.png")).convert_alpha() ####
ball_med = pygame.image.load(resource_path("player/med_ball.png")).convert_alpha() ####
ball_big = pygame.image.load(resource_path("player/big_ball.png")).convert_alpha() ####

fire1 = pygame.image.load(resource_path("tiles/fire1.png")).convert_alpha() ####
fire2 = pygame.image.load(resource_path("tiles/fire2.png")).convert_alpha() ####

water1 = pygame.image.load(resource_path("tiles/water1.png")).convert_alpha() ####
water2 = pygame.image.load(resource_path("tiles/water2.png")).convert_alpha() ####

snow_thin1 = pygame.image.load(resource_path("tiles/snow_thin1.png")).convert_alpha() ####
snow_thin2 = pygame.image.load(resource_path("tiles/snow_thin2.png")).convert_alpha() ####
snow_thick1 = pygame.image.load(resource_path("tiles/snow_thick1.png")).convert_alpha() ####
snow_thick2 = pygame.image.load(resource_path("tiles/snow_thick2.png")).convert_alpha() ####

grass = pygame.image.load(resource_path("tiles/grass.png")).convert_alpha() ####

ice = pygame.image.load(resource_path("tiles/ice.png")).convert_alpha() ####

wood = pygame.image.load(resource_path("tiles/wood.png")).convert_alpha() ############################## ####

heart = pygame.image.load(resource_path("misc/heart.png")).convert_alpha() ####

how_to_play = pygame.image.load(resource_path("misc/how_to_play.png")).convert_alpha() ####

santa = pygame.image.load(resource_path("misc/santa.png")).convert_alpha() ####
evil_santa = pygame.image.load(resource_path("misc/evil_santa.png")).convert_alpha() ####

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

def make_wood_img() -> pygame.Surface:
    return pygame.transform.scale(wood.copy(), (TILE_DIMENSION, TILE_DIMENSION))

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

def make_how_to_play() -> pygame.Surface:
    scale_factor = SCREEN_HEIGHT / how_to_play.get_height()
    return pygame.transform.scale_by(how_to_play, scale_factor)

def make_santa() -> pygame.Surface:
    return pygame.transform.scale(santa.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))

def make_evil_santa() -> pygame.Surface:
    return pygame.transform.scale(evil_santa.copy(), (PLAYER_DIMENSION, PLAYER_DIMENSION))