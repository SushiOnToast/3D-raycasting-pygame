import pygame
from settings import *
import math

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2

        self.radius = 3

        self.turn_direction = 0
        self.walk_direction = 0
        self.rotation_angle = 45 * (math.pi/180)
        self.move_speed = 2
        self.rotation_speed = 2 * (math.pi/180)
    
    def update(self):
        keys = pygame.key.get_pressed()

        self.turn_direction = 0
        self.walk_direction = 0

        if keys[pygame.K_LEFT]:
            self.turn_direction = -1
        if keys[pygame.K_RIGHT]:
            self.turn_direction = 1

        if keys[pygame.K_UP]:
            self.walk_direction = 1
        if keys[pygame.K_DOWN]:
            self.walk_direction = -1
        
        move_step = self.walk_direction * self.move_speed
        self.rotation_angle += self.turn_direction * self.rotation_speed
        self.x += math.cos(self.rotation_angle) * move_step
        self.y += math.sin(self.rotation_angle) * move_step
        

    def render(self, screen):
        pygame.draw.circle(screen, "red", (self.x, self.y), self.radius)
