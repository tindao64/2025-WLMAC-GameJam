import pygame
import tile
import drawings

class Grass(tile.Tile):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image.blit(drawings.make_grass_img(), (0, 0))
    
    def type(self):
        return "grass"

tile.tile_factories["grass"] = lambda: Grass()
tile.tile_types.append("grass")
