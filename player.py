import pygame
from config import *
import drawings

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = drawings.make_player_img(Direction.UP, 0)

        # pos
        self.rect = self.image.get_rect(center = (0, 0))

        # dir
        self.direction = Direction.UP

        self.score = 0
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self._layer = PLAYER_LAYER
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        # Update direction we "look"

        if keys[KEY_UP]:
            self.direction = Direction.UP
            self.rect.move_ip(0, -self.speed * dt)
        if keys[KEY_DOWN]:
            self.direction = Direction.DOWN
            self.rect.move_ip(0, self.speed * dt)
        if keys[KEY_LEFT]:
            self.direction = Direction.LEFT
            self.rect.move_ip(-self.speed * dt, 0)
        if keys[KEY_RIGHT]:
            self.direction = Direction.RIGHT
            self.rect.move_ip(self.speed * dt, 0)

        self.rect.clamp_ip((0, 0, MAP_WIDTH * TILE_DIMENSION, MAP_HEIGHT * TILE_DIMENSION))

        self.image = drawings.make_player_img(self.direction, self.score)
