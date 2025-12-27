import pygame
import tile
import drawings

class DeepSnow(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_deep_snow_img(), (0, 0))
    
    def type(self):
        return "deep_snow"

tile.tile_factories["deep_snow"] = lambda: DeepSnow()
tile.tile_types.append("deep_snow")
