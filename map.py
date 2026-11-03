import pygame
from settings import *

class Map:
    def __init__(self):
        # Number 1 is a wall, 0 is an empty space
        self.grid = MAP

    def has_wall_at(self, x, y):
        map_x = int(x // TILESIZE)
        map_y = int(y // TILESIZE)

        if map_x < 0 or map_x >= len(self.grid[0]) or map_y < 0 or map_y >= len(self.grid):
            return True

        return self.grid[map_y][map_x] == 1

    def render(self, screen):
        # method to render the map
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                # determine the pixel coordinates on the screen
                tile_x = j * TILESIZE
                tile_y = i * TILESIZE

                colour = (255, 255, 255)
                if self.grid[i][j] == 0:
                    colour = (0, 0, 0)
                pygame.draw.rect(screen, colour, (tile_x, tile_y, TILESIZE, TILESIZE))