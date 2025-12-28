import pygame
from config import *
import drawings

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = drawings.make_player_img(Direction.UP, 0)

        # pos
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # dir
        self.direction = Direction.UP

        self.score = 0

        self.health = PLAYER_HEALTH

        self._layer = PLAYER_LAYER
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        # Update direction we "look"

        old_direction = self.direction
        if keys[KEY_UP]:
            self.direction = Direction.UP
        if keys[KEY_DOWN]:
            self.direction = Direction.DOWN
        if keys[KEY_LEFT]:
            self.direction = Direction.LEFT
        if keys[KEY_RIGHT]:
            self.direction = Direction.RIGHT

        # Skip updating if direction didn't change
        if self.direction == old_direction:
            return
        self.image.fill((0,0,0,0))
        self.image.blit(drawings.make_player_img(self.direction, self.score), (0, 0))
