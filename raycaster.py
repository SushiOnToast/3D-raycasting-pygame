import pygame
from settings import *
from ray import Ray

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map

    def castAllRays(self):
        self.rays = []
        ray_angle = self.player.rotation_angle - (FOV / 2)
        for i in range(NUM_RAYS):
            ray = Ray(ray_angle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)

            ray_angle += FOV / NUM_RAYS

    def render(self, screen):
        dist_to_projection_plane = (WINDOW_WIDTH / math.tan(FOV / 2))
        i = 0
        for ray in self.rays:
            # ray.render(screen)

            # height of the wall on our projection, the wall height is currently set to TILESIZE but can be changed if needed
            line_height = (TILESIZE / ray.distance) * dist_to_projection_plane

            draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (ray.colour, ray.colour, ray.colour), (i*RES, draw_begin, RES, draw_end))

            i += 1