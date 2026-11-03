import pygame
from settings import *

class Map:
    def __init__(self):
        # Number 1 is a wall, 0 is an empty space
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

    def has_wall_at(self, x, y):
        # this method checks whether there is wall where the players is or not
        return self.grid[int(y // TILESIZE)][int(x // TILESIZE)]

    def render(self, screen):
        # method to render the map
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                # determine the pixel coordinates on the screen
                tile_x = j * TILESIZE
                tile_y = i * TILESIZE

                colour = (255, 255, 255)
                if self.grid[i][j] == 1:
                    colour = (0, 0, 0)
                pygame.draw.rect(screen, colour, (tile_x, tile_y, TILESIZE-1, TILESIZE-1))