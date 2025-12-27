import pygame
from config import *
import drawings

class Map(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        
        # image
        self.image = drawings.map_img.copy()

        # pos
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
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
