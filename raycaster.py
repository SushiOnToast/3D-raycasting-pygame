import pygame
from settings import *
from ray import Ray, normalize_angle

class Raycaster:
    def __init__(self, player, map):
        self.rays = []
        self.player = player
        self.map = map
    
    def castAllRays(self):
        self.rays = []
        ray_angle = normalize_angle(self.player.rotation_angle - FOV/2)
        ray_increment = FOV/NUM_RAYS

        for i in range(NUM_RAYS):
            ray = Ray(ray_angle, self.player, self.map)
            ray.cast()
            self.rays.append(ray)

            ray_angle = normalize_angle(ray_angle + ray_increment)

    def render(self, screen):
        for ray in self.rays:
            ray.render(screen)