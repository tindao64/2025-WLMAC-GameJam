import pygame
import tile
import drawings

class Snow(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_snow_img(), (0, 0))
    
    def type(self):
        return "snow"

tile.tile_factories["snow"] = lambda: Snow()
tile.tile_types.append("snow")
