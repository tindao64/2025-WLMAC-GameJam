import pygame
import tile
import drawings

class Snow(tile.Tile):
    def __init__(self, thickness = 0, *groups):
        super().__init__(*groups)
        self.set_thickness(thickness)
    
    def set_thickness(self, thickness):
        self.thickness = thickness
        self.image.blit(drawings.make_snow_img(self.thickness), (0, 0))
    
    def type(self):
        return "snow"

tile.tile_factories["snow"] = lambda: Snow()
tile.tile_types.append("snow")