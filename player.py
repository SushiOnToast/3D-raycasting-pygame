import pygame
import math
from settings import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        self.radius = 5
        self.turn_dir = 0
        self.walk_dir = 0
        self.rotation_angle = 90 * (math.pi / 180)
        self.move_speed = 2.5
        self.rotation_speed = 2 * (math.pi / 180)

    def update(self):
        keys = pygame.key.get_pressed()

        self.turn_dir = 0
        self.walk_dir = 0

        if keys[pygame.K_RIGHT]:
            self.turn_dir = 1
        if keys[pygame.K_LEFT]:
            self.turn_dir = -1
        if keys[pygame.K_UP]:
            self.walk_dir = 1
        if keys[pygame.K_DOWN]:
            self.walk_dir = -1

        move_step = self.walk_dir * self.move_speed
        self.rotation_angle += self.turn_dir * self.rotation_speed
        self.x += math.cos(self.rotation_angle) * move_step
        self.y += math.sin(self.rotation_angle) * move_step

    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x + math.cos(self.rotation_angle) * 50, self.y + math.sin(self.rotation_angle) * 50))