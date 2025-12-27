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

        self.tile_groups: dict[str, pygame.sprite.Group] = {}
        self.tiles: list[tile.Tile | None] = []

        # TODO: random choice of tiles
        # fill in map completely randomly for now
        weights = [1] * len(tile.tile_types)
        self.make_map(weights)

        self._layer = MAP_LAYER

        self.speed = PLAYER_SPEED
    
    # Fills in the map with stuff
    # Weights are relative to each other
    # len(weights) should equal len(tile.tile_types)
    def make_map(self, weights):
        # generate the tiles
        tiletypes = random.choices(tile.tile_types, weights=weights, k=(MAP_WIDTH * MAP_HEIGHT))
        self.tiles.clear()
        self.tile_groups.clear()
        self.tile_groups["all"] = pygame.sprite.Group()

        position = 0

        for type in tiletypes:
            t = tile.make_tile(type)
            self.tiles.append(t)

            # Add to typed and all groups
            group = self.tile_groups.setdefault(type, pygame.sprite.Group())
            group.add(t)
            self.tile_groups["all"].add(t)

            # Set its position
            t.position = [position % MAP_WIDTH, position // MAP_WIDTH]
            t.rect = [t.position[0] * TILE_DIMENSION, t.position[1] * TILE_DIMENSION, TILE_DIMENSION, TILE_DIMENSION]
            position += 1

        self.redraw()
    
    def set_tile(self, x, y, new_tile: tile.Tile):
        old = self.tiles[y * MAP_WIDTH + x]
        if old is not None:
            self.remove_tile(old)
        self.tiles[y * MAP_WIDTH + x] = new_tile
        new_tile.position = [x, y]
        new_tile.rect = [new_tile.position[0] * TILE_DIMENSION, new_tile.position[1] * TILE_DIMENSION, TILE_DIMENSION, TILE_DIMENSION]

        self.tile_groups["all"].add(new_tile)
        self.tile_groups.setdefault(new_tile.type(), pygame.sprite.Group()).add(new_tile)

    
    def remove_tile(self, tile: tile.Tile):
        self.tile_groups["all"].remove(tile)

        tile_group = self.tile_groups[tile.type()]
        tile_group.remove(tile)
        if len(tile_group) == 0:
            self.tile_groups.pop(tile.type())
        
        self.tiles[tile.position[1] * MAP_WIDTH + tile.position[0]] = None
        
    def player_collide(self, group_name: str) -> list[tile.Tile]:
        if group_name not in self.tile_groups:
            return []
        group = self.tile_groups[group_name]

        # The player rect, as seen by us
        player_rect_relative = pygame.Rect(
            SCREEN_WIDTH // 2 - self.rect.x - PLAYER_DIMENSION // 2,
            SCREEN_HEIGHT // 2 - self.rect.y - PLAYER_DIMENSION // 2,
            PLAYER_DIMENSION,
            PLAYER_DIMENSION
        )

        sprites = group.sprites()

        collided = player_rect_relative.collideobjectsall(
            sprites,
            key=lambda s: s.rect
        )
        return collided
    
    # Get a group of tiles by type, or "all" which is all of them
    def get_group(self, group: str):
        return self.tile_groups[group]
    
    def redraw(self):
        self.image.fill("black")
        self.tile_groups["all"].draw(self.image)
    
    # Returns the tile coordinate that is currently in the middle of the screen
    def get_center(self):
        x_px = SCREEN_WIDTH // 2 - self.rect.x
        y_px = SCREEN_HEIGHT // 2 - self.rect.y

        return (x_px // TILE_DIMENSION, y_px // TILE_DIMENSION)
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        # dt is time since last update
        # multiply with PLAYER_SPEED to ensure constant moving speed
        if keys[KEY_UP]:
            self.rect = self.rect.move(0, self.speed * dt)
        if keys[KEY_DOWN]:
            self.rect = self.rect.move(0, -self.speed * dt)
        if keys[KEY_LEFT]:
            self.rect = self.rect.move(self.speed * dt, 0)
        if keys[KEY_RIGHT]:
            self.rect = self.rect.move(-self.speed * dt, 0)

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
