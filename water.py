import pygame
import tile
import drawings

class Water(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_water_img(), (0, 0))
    
    def type(self):
        return "water"

tile.tile_factories["water"] = lambda: Water()
tile.tile_types.append("water")
