import pygame
import drawings
from config import *
import random

class Santa(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)

        self.image = drawings.make_santa()
        # FIX: Add parentheses to EXECUTE the method
        self.go_to_spawn() # <--- Corrected!
        self.total_score = 0
    
    def go_to_spawn(self):
        new_pos = (TILE_DIMENSION // 2, TILE_DIMENSION // 2) 
        
        self.rect = self.image.get_rect(center=new_pos)

    def go_to_random(self):
        random_x_min = PLAYER_DIMENSION // 2
        random_x_max = MAP_WIDTH * TILE_DIMENSION - PLAYER_DIMENSION // 2
        random_y_min = PLAYER_DIMENSION // 2
        random_y_max = MAP_HEIGHT * TILE_DIMENSION - PLAYER_DIMENSION // 2

        new_pos = (
            random.randint(random_x_min, random_x_max),
            random.randint(random_y_min, random_y_max)
        )

        self.rect = self.image.get_rect(center=new_pos)
    
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, *_):
        ...
