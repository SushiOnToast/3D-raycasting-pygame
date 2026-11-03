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

    def render(self, screen, topdown, viewport_width=None):
        if viewport_width is None:
            viewport_width = WINDOW_WIDTH

        dist_to_projection_plane = viewport_width / (2 * math.tan(FOV / 2))

        i = 0

        for ray in self.rays:

            if topdown:
                ray.render(screen)

            else:
                line_height = (TILESIZE / ray.distance) * dist_to_projection_plane

                draw_begin = (WINDOW_HEIGHT / 2) - (line_height / 2)
                draw_end = draw_begin + line_height

                pygame.draw.rect(
                    screen,
                    (ray.colour, ray.colour, ray.colour),
                    (i * (viewport_width / NUM_RAYS), draw_begin,
                    viewport_width / NUM_RAYS, line_height)
                )

            i += 1