import pygame
import tile
import drawings

class Ice(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_ice_img(), (0, 0))
    
    def type(self):
        return "ice"

tile.tile_factories["ice"] = lambda: Ice()
tile.tile_types.append("ice")
