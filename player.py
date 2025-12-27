import pygame
from config import *
import drawings

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = pygame.Surface((PLAYER_DIMENSION, PLAYER_DIMENSION)).convert_alpha()
        self.image.blit(drawings.player_img, (0, 0))

        # pos
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # dir
        self.direction = Direction.UP
    
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
        
        self.image.blit(drawings.player_img, (0, 0))

        match self.direction:
            case Direction.UP:
                self.image = pygame.transform.rotate(self.image, 0)
            case Direction.DOWN:
                self.image = pygame.transform.rotate(self.image, 180)
            case Direction.LEFT:
                self.image = pygame.transform.rotate(self.image, 90)
            case Direction.RIGHT:
                self.image = pygame.transform.rotate(self.image, 270)

