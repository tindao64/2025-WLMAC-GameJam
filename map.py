import pygame
from config import *
import tile
import random
from ordered_group import OrderedGroup
from typing import Callable

class Map(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = pygame.Surface((MAP_WIDTH * TILE_DIMENSION, MAP_HEIGHT * TILE_DIMENSION)).convert()

        # pos
        self.rect = self.image.get_rect()

        self.all_sprites = OrderedGroup()

        self._layer = MAP_LAYER

    # Fills in the map with stuff
    # Weights are relative to each other
    # len(weights) should equal len(tile.tile_types)
    def make_map(self, generator: Callable[[tuple[int, int]], tile.Tile]):
        # clear the existing tiles
        self.all_sprites.empty()
        
        # generate tiles
        for position in range(MAP_WIDTH * MAP_HEIGHT):
            x, y = position % MAP_WIDTH, position // MAP_WIDTH

            t = generator((x, y))

            # add to sprites
            self.all_sprites.add(t)

            # Set its position
            t.position = (x, y)
            t.update_rect()
            position += 1

        self.redraw()
    
    def set_tile(self, position, new_tile: tile.Tile):
        x, y = position
        # Position in all_sprites
        position = y * MAP_WIDTH + x

        # Add new tile
        self.all_sprites[position] = new_tile

        # Set position
        new_tile.position = (x, y)
        new_tile.update_rect()

    def get_all_tiles(self):
        return self.all_sprites
    
    def redraw(self):
        self.image.fill("black")
        self.all_sprites.draw(self.image)
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, *_):
        ...
