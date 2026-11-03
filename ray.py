import math, pygame
from settings import *

def normalise_angle(angle):
    angle = angle % (2 * math.pi)
    if (angle <= 0):
        angle = (2 * math.pi) + angle

    return angle

def distance_between(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))

class Ray:
    def __init__(self, angle, player, map):
        self.ray_angle = normalise_angle(angle)
        self.player = player
        self.map = map

        self.is_facing_down = self.ray_angle > 0 and self.ray_angle < math.pi
        self.is_facing_up = not self.is_facing_down
        self.is_facing_right = self.ray_angle < 0.5 * math.pi or self.ray_angle > 1.5 * math.pi
        self.is_facing_left = not self.is_facing_right

        self.wall_hit_x = 0
        self.wall_hit_y = 0

        self.distance = 0
        self.colour = 255

    def cast(self):
        ## horizontal checking
        found_horizontal_wall = False
        horizontal_hit_x = 0
        horizontal_hit_y = 0

        first_intersection_x = 0
        first_intersection_y = 0

        if self.is_facing_up:
            first_intersection_y = ((self.player.y) // TILESIZE) * TILESIZE - 0.01
        elif self.is_facing_down:
            first_intersection_y = ((self.player.y) // TILESIZE) * TILESIZE + TILESIZE

        first_intersection_x = self.player.x + (first_intersection_y - self.player.y) / math.tan(self.ray_angle)

        next_horizontal_x = first_intersection_x
        next_horizontal_y = first_intersection_y

        xa = 0
        ya = 0

        if self.is_facing_up:
            ya = -TILESIZE
        elif self.is_facing_down:
            ya = TILESIZE

        xa = ya / math.tan(self.ray_angle)

        while (next_horizontal_x <= WINDOW_WIDTH and next_horizontal_x >= 0 and next_horizontal_y <= WINDOW_HEIGHT and next_horizontal_y >= 0):
            if self.map.has_wall_at(next_horizontal_x, next_horizontal_y):
                found_horizontal_wall = True
                horizontal_hit_x = next_horizontal_x
                horizontal_hit_y = next_horizontal_y
                break
            else:
                next_horizontal_x += xa
                next_horizontal_y += ya

        ## vertical checking
        found_vertical_wall = False
        vertical_hit_x = 0
        vertical_hit_y = 0

        if self.is_facing_right:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) + TILESIZE
        elif self.is_facing_left:
            first_intersection_x = ((self.player.x // TILESIZE) * TILESIZE) - 0.01

        first_intersection_y = self.player.y + (first_intersection_x - self.player.x) * math.tan(self.ray_angle)

        next_vertical_x = first_intersection_x
        next_vertical_y = first_intersection_y

        if self.is_facing_right:
            xa = TILESIZE
        elif self.is_facing_left:
            xa = -TILESIZE

        ya = xa * math.tan(self.ray_angle)

        while (next_vertical_x <= WINDOW_WIDTH and next_vertical_x >= 0 and next_vertical_y <= WINDOW_HEIGHT and next_vertical_y >= 0):
            if self.map.has_wall_at(next_vertical_x, next_vertical_y):
                found_vertical_wall = True
                vertical_hit_x = next_vertical_x
                vertical_hit_y = next_vertical_y
                break
            else:
                next_vertical_x += xa
                next_vertical_y += ya

        # distance calculation (compare distances and figure out which wall hit is valid)
        horizontal_distance = 0
        vertical_distance = 0

        if found_horizontal_wall:
            horizontal_distance = distance_between(self.player.x, self.player.y, horizontal_hit_x, horizontal_hit_y)
        else:
            horizontal_distance = 9999
        if found_vertical_wall:
            vertical_distance = distance_between(self.player.x, self.player.y, vertical_hit_x, vertical_hit_y)
        else:
            vertical_distance = 9999

        if horizontal_distance < vertical_distance:
            self.wall_hit_x = horizontal_hit_x
            self.wall_hit_y = horizontal_hit_y
            self.distance = horizontal_distance
            self.colour = 160
        else:
            self.wall_hit_x = vertical_hit_x
            self.wall_hit_y = vertical_hit_y
            self.distance = vertical_distance
            self.colour = 255

        # here we get rid of fisheye effect by measuring the distance from the player's viewplane rather than the player itself
        self.distance *= math.cos(self.player.rotation_angle - self.ray_angle)

        # lighting effect
        self.colour *= (60 / self.distance)
        self.colour = min(self.colour, 255)

    def render(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.player.x, self.player.y), (self.wall_hit_x, self.wall_hit_y))