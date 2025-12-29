# All drawings and stuff

import pygame
from config import *
import random


import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath(".")
    return os.path.join(base_path, relative_path)

player = {}

for dir in ["up", "down", "left", "right"]:
    dir_enum = {"up": Direction.UP, "down": Direction.DOWN, "left": Direction.LEFT, "right": Direction.RIGHT}[dir]
    player[dir_enum] = {}
    for size in ["", "small", "med", "big"]:
        path = resource_path(f"player/{dir}{'_' if len(size) > 0 else ''}{size}.png")
        player[dir_enum][size] = pygame.image.load(path).convert_alpha()

fire1 = pygame.image.load(resource_path("tiles/fire1.png")).convert_alpha()
fire2 = pygame.image.load(resource_path("tiles/fire2.png")).convert_alpha()

water1 = pygame.image.load(resource_path("tiles/water1.png")).convert_alpha()
water2 = pygame.image.load(resource_path("tiles/water2.png")).convert_alpha()

snow1 = pygame.image.load(resource_path("tiles/snow1.png")).convert_alpha()
snow2 = pygame.image.load(resource_path("tiles/snow2.png")).convert_alpha()
snow3 = pygame.image.load(resource_path("tiles/snow3.png")).convert_alpha()
snow4 = pygame.image.load(resource_path("tiles/snow4.png")).convert_alpha()
snow = [snow1, snow2, snow3, snow4]

grass = pygame.image.load(resource_path("tiles/grass.png")).convert_alpha()

ice = pygame.image.load(resource_path("tiles/ice.png")).convert_alpha()

wood = pygame.image.load(resource_path("tiles/wood.png")).convert_alpha()

heart = pygame.image.load(resource_path("misc/heart.png")).convert_alpha()

how_to_play = pygame.image.load(resource_path("misc/how_to_play.png")).convert_alpha()

santa = pygame.image.load(resource_path("misc/santa.png")).convert_alpha()
evil_santa = pygame.image.load(resource_path("misc/evil_santa.png")).convert_alpha()

def make_player_img(dir: Direction, score: int) -> pygame.Surface:
    snow = ""
    if score >= PLAYER_SMALL_BALL_THRESHOLD:
        snow = "small"
    if score >= PLAYER_MEDIUM_BALL_THRESHOLD:
        snow = "med"
    if score >= PLAYER_BIG_BALL_THRESHOLD:
        snow = "big"
    return pygame.transform.scale(player[dir][snow], (PLAYER_DIMENSION, PLAYER_DIMENSION))

def make_snow_img(thickness: int) -> pygame.Surface:
    return pygame.transform.scale(snow[thickness], (TILE_DIMENSION, TILE_DIMENSION))

def make_wood_img() -> pygame.Surface:
    return pygame.transform.scale(wood, (TILE_DIMENSION, TILE_DIMENSION))

def make_fire_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([fire1, fire2]), (TILE_DIMENSION, TILE_DIMENSION))

def make_water_img() -> pygame.Surface:
    return pygame.transform.scale(random.choice([water1, water2]), (TILE_DIMENSION, TILE_DIMENSION))

def make_ice_img() -> pygame.Surface:
    return pygame.transform.scale(ice, (TILE_DIMENSION, TILE_DIMENSION))

def make_grass_img() -> pygame.Surface:
    return pygame.transform.scale(grass, (TILE_DIMENSION, TILE_DIMENSION))

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
    return pygame.transform.scale(santa, (PLAYER_DIMENSION, PLAYER_DIMENSION))

def make_evil_santa() -> pygame.Surface:
    return pygame.transform.scale(evil_santa, (PLAYER_DIMENSION, PLAYER_DIMENSION))