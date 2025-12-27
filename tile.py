# A tile on the map

import pygame
from config import *
from enum import Enum
from typing import Callable

type TileType = str

class Tile(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((TILE_DIMENSION, TILE_DIMENSION)).convert()
        self.position: list[int] = [-1, -1] # This is set by the Map
        self.rect: list[int] = [-1, -1, TILE_DIMENSION, TILE_DIMENSION] # Also set by the map
    
    # Please implement this in subclasses
    # Return a string containing the type
    def type(self) -> str:
        ...
    
    # Use Map.remove instead, which properly handles it
    def kill(self):
        raise TypeError("kill() is not supported on `Tile`s. Use Map.remove instead.")

# Tiles should fill in one entry into these upon importing

tile_factories: dict[TileType, Callable[[], Tile]] = {}
tile_types: list[TileType] = []

def make_tile(type: TileType) -> Tile:
    return tile_factories[type]()
