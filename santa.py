import pygame
import drawings
from config import *
import random

class Santa(pygame.sprite.Sprite):
    def __init__(self, *groups) -> None:
        super().__init__()

        self.image = drawings.make_santa()
        self.rect = self.image.get_rect(midtop=(MAP_WIDTH * TILE_DIMENSION // 2, 0))
        self.total_score = 0
        self.layer = SANTA_LAYER

        self.add(*groups)

    def update(self, dt: float, keys: pygame.key.ScancodeWrapper, *_):
        ...
