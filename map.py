import pygame
from config import *
import tile
import random

class Map(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = pygame.Surface((MAP_WIDTH * TILE_DIMENSION, MAP_HEIGHT * TILE_DIMENSION)).convert()

        # pos
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

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
        self.tiles = [tile.make_tile(t) for t in tiletypes]
        self.redraw()
    
    def set_tile(self, x, y, new_tile: tile.Tile):
        self.tiles[y * MAP_WIDTH + x] = new_tile
        self.redraw()
    
    def redraw(self):
        self.image.fill("black")
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                self.image.blit(
                    self.tiles[y * MAP_WIDTH + x].image, # tile image
                    (x * TILE_DIMENSION, y * TILE_DIMENSION) # tile coords on screen
                )
        # TODO: remove debug, also remove the redraw in update()
        center = self.get_center()
        pygame.draw.rect(
            self.image,
            "purple",
            (center[0] * TILE_DIMENSION, center[1] * TILE_DIMENSION, TILE_DIMENSION, TILE_DIMENSION),
            width=(TILE_DIMENSION//10)
        )
    
    # Returns the tile coordinate that is currently in the middle of the screen
    def get_center(self):
        x_px = SCREEN_WIDTH // 2 - self.rect.x
        y_px = SCREEN_HEIGHT // 2 - self.rect.y

        return (x_px // TILE_DIMENSION, y_px // TILE_DIMENSION)
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        # dt is time since last update
        # multiply with PLAYER_SPEED to ensure constant moving speed
        if keys[KEY_UP]:
            self.rect = self.rect.move(0, PLAYER_SPEED * dt)
        if keys[KEY_DOWN]:
            self.rect = self.rect.move(0, -PLAYER_SPEED * dt)
        if keys[KEY_LEFT]:
            self.rect = self.rect.move(PLAYER_SPEED * dt, 0)
        if keys[KEY_RIGHT]:
            self.rect = self.rect.move(-PLAYER_SPEED * dt, 0)

        # Ensure player can't go off the map
        PLAYER_LEFT = SCREEN_WIDTH // 2 - PLAYER_DIMENSION // 2
        PLAYER_RIGHT = SCREEN_WIDTH // 2 + PLAYER_DIMENSION // 2
        PLAYER_TOP = SCREEN_HEIGHT // 2 - PLAYER_DIMENSION // 2
        PLAYER_BOTTOM = SCREEN_HEIGHT // 2 + PLAYER_DIMENSION // 2

        if self.rect.left > PLAYER_LEFT: # reversed since the map moves and not the player
            self.rect = self.rect.move(PLAYER_LEFT - self.rect.left, 0)
        if self.rect.right < PLAYER_RIGHT:
            self.rect = self.rect.move(PLAYER_RIGHT - self.rect.right, 0)
        if self.rect.top > PLAYER_TOP:
            self.rect = self.rect.move(0, PLAYER_TOP - self.rect.top)
        if self.rect.bottom < PLAYER_BOTTOM:
            self.rect = self.rect.move(0, PLAYER_BOTTOM - self.rect.bottom)
        self.redraw()
