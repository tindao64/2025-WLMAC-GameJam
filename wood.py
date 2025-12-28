import pygame
import tile
import drawings

class Wood(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_wood_img(), (0, 0))
    
    def type(self):
        return "wood"

tile.tile_factories["wood"] = lambda: Wood()
tile.tile_types.append("wood")