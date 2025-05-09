import math
import pygame
from settings import *


def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if (angle < 0):
        angle = (2 * math.pi) + angle
    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Ray:
    def __init__(self, angle, player, map):
        self.ray_angle = normalize_angle(angle)
        self.player = player
        self.map = map

        # since y axis is inverted in pygame, in normal cartesian plane it would be considered up
        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.ray_angle < 0.5 * math.pi or self.ray_angle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

    
    def cast(self):
    # Handle vertical rays (90° and 270°)
        if abs(math.cos(self.ray_angle)) < 0.0001:
            # Vertical ray - only check vertical intersections, since the ray would be pointing straiht up
            next_x = math.floor(self.player.x / TILESIZE) * TILESIZE
            next_x += TILESIZE if self.is_facing_right else 0
            
            while 0 <= next_x <= WIDTH:
                if self.map.has_wall_at(next_x, self.player.y):
                    self.wall_hit_x = next_x
                    self.wall_hit_y = self.player.y
                    return
                next_x += TILESIZE if self.is_facing_right else -TILESIZE
            return

        # Handle horizontal rays (0° and 180°)
        if abs(math.sin(self.ray_angle)) < 0.0001:
            # Horizontal ray - only check horizontal intersections, since the ray would be pointing straight left or right
            next_y = math.floor(self.player.y / TILESIZE) * TILESIZE
            next_y += TILESIZE if self.is_facing_down else 0
            
            while 0 <= next_y <= HEIGHT:
                if self.map.has_wall_at(self.player.x, next_y):
                    self.wall_hit_x = self.player.x
                    self.wall_hit_y = next_y
                    return
                next_y += TILESIZE if self.is_facing_down else -TILESIZE
            return
        
        # for all other angles

        # Horizontal intersection checking
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        # Find first horizontal intersection
        first_y = math.floor(self.player.y / TILESIZE) * TILESIZE
        if self.is_facing_down:
            first_y += TILESIZE
        else:
            first_y -= 0.0001

        # Calculate horizontal steps
        ya = TILESIZE if self.is_facing_down else -TILESIZE
        xa = ya / math.tan(self.ray_angle)

        next_x = self.player.x + (first_y - self.player.y) / math.tan(self.ray_angle)
        next_y = first_y

        # Check horizontal intersections
        while 0 <= next_x <= WIDTH and 0 <= next_y <= HEIGHT:
            if self.map.has_wall_at(next_x, next_y - (0.0001 if self.is_facing_up else 0)):
                found_horizontal_wall = True
                horizontal_hit_x = next_x
                horizontal_hit_y = next_y
                break
            next_x += xa
            next_y += ya

        # Vertical intersection checking
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        # Find first vertical intersection
        first_x = math.floor(self.player.x / TILESIZE) * TILESIZE
        if self.is_facing_right:
            first_x += TILESIZE
        else:
            first_x -= 0.0001

        # Calculate vertical steps
        xa = TILESIZE if self.is_facing_right else -TILESIZE
        ya = xa * math.tan(self.ray_angle)

        next_x = first_x
        next_y = self.player.y + (first_x - self.player.x) * math.tan(self.ray_angle)

        # Check vertical intersections
        while 0 <= next_x <= WIDTH and 0 <= next_y <= HEIGHT:
            if self.map.has_wall_at(next_x - (0.0001 if self.is_facing_left else 0), next_y):
                found_vertical_wall = True
                vertical_hit_x = next_x
                vertical_hit_y = next_y
                break
            next_x += xa
            next_y += ya

        # Find closest wall hit
        horizontal_dist = float('inf')
        if found_horizontal_wall:
            horizontal_dist = distance_between(
                self.player.x, self.player.y,
                horizontal_hit_x, horizontal_hit_y
            )

        vertical_dist = float('inf')
        if found_vertical_wall:
            vertical_dist = distance_between(
                self.player.x, self.player.y,
                vertical_hit_x, vertical_hit_y
            )

        # Set wall hit point to closest intersection
        if horizontal_dist < vertical_dist:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y

    def render(self, screen):
        # pygame.draw.line(screen, "red", (self.player.x, self.player.y), (self.player.x + (
        #     math.cos(self.ray_angle)) * 50, self.player.y + (math.sin(self.ray_angle)) * 50))
        pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.wall_hit_x,self.wall_hit_y))