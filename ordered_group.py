# Pygame `Group`, but deterministically ordered and random-accessable
from typing import Iterator
import pygame

class OrderedGroup(pygame.sprite.AbstractGroup):
    def __init__(self, *sprites) -> None:
        self.spritelist: list = []
        self.spritedict: dict = {}

        self.add(*sprites)
    
    def add_internal(self, sprite, layer=None) -> None:
        if not self.has_internal(sprite):
            self.spritedict[sprite] = len(self.spritelist)
            self.spritelist.append(sprite)
    
    def remove_internal(self, sprite) -> None:
        if self.has_internal(sprite):
            index = self.spritedict.pop(sprite)
            del self.spritelist[index]
    
    def __getitem__(self, key: int):
        return self.spritelist[key]

    def __setitem__(self, index: int, sprite) -> None:
        # Remove the old sprite
        old_sprite = self.spritelist[index]
        self.spritedict.pop(old_sprite)

        # Add the new sprite
        self.spritelist[index] = sprite
        self.spritedict[sprite] = index
    
    # Override for efficiency
    def empty(self) -> None:
        self.spritedict.clear()
        self.spritelist.clear()

    def sprites(self):
        return self.spritelist.copy()
