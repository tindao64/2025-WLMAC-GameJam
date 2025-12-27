import pygame
import tile
import drawings

class Fire(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.fire_img, (0, 0))
    
    def type(self):
        return "fire"

tile.tile_factories["fire"] = lambda: Fire()
tile.tile_types.append("fire")
