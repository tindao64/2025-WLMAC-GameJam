import pygame
from config import *
import tile
import random
from ordered_group import OrderedGroup

class Map(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = pygame.Surface((MAP_WIDTH * TILE_DIMENSION, MAP_HEIGHT * TILE_DIMENSION)).convert()

        # pos
        self.rect = self.image.get_rect()

        self.tile_groups: dict[str, pygame.sprite.Group] = {}
        self.all_sprites = OrderedGroup()

        # TODO: random choice of tiles
        # fill in map completely randomly for now
        weights = [1] * len(tile.tile_types)
        self.make_map(weights)

        self._layer = MAP_LAYER

    # Fills in the map with stuff
    # Weights are relative to each other
    # len(weights) should equal len(tile.tile_types)
    def make_map(self, weights):
        # generate the tiles
        tiletypes = random.choices(tile.tile_types, weights=weights, k=(MAP_WIDTH * MAP_HEIGHT))
        self.tile_groups.clear()
        self.all_sprites.empty()

        position = 0



        top_rows_count = 3 * MAP_WIDTH
        top_tile_type = "wood"
        for i in range(top_rows_count):
            tiletypes[i] = top_tile_type
            
            
        for type in tiletypes:
            t = tile.make_tile(type)

            # Add to typed and all groups
            group = self.tile_groups.setdefault(type, pygame.sprite.Group())
            group.add(t)
            self.all_sprites.add(t)

            # Set its position
            t.position = (position % MAP_WIDTH, position // MAP_WIDTH)
            t.update_rect()
            position += 1

        self.redraw()
    
    def set_tile(self, position, new_tile: tile.Tile):
        x, y = position
        # Position in all_sprites
        position = y * MAP_WIDTH + x

        # Remove the old tile from type group
        old_tile: tile.Tile = self.all_sprites[position]
        old_tile_type = old_tile.type()
        self.tile_groups[old_tile_type].remove(old_tile)
        
        # Remove the old group if empty
        if (len(self.tile_groups[old_tile_type]) == 0):
            self.tile_groups.pop(old_tile_type)

        # Add new tile
        self.all_sprites[position] = new_tile

        # Add to typed group
        self.tile_groups.setdefault(new_tile.type(), pygame.sprite.Group()).add(new_tile)

        # Set position
        new_tile.position = (x, y)
        new_tile.update_rect()

    # Get a group of tiles by type
    def get_group(self, group: str):
        return self.tile_groups[group]
    
    def has_group(self, group: str):
        return group in self.tile_groups
    
    def redraw(self):
        self.image.fill("black")
        self.all_sprites.draw(self.image)
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, *_):
        ...
