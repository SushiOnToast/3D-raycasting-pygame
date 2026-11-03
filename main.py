import pygame
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster

# Larger display window
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Original internal rendering surface
game_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map()
player = Player(map)
raycaster = Raycaster(player, map)

clock = pygame.time.Clock()

view_mode = 0
# 0 = Top-down
# 1 = Pseudo-3D
# 2 = Split-screen

topdown_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
raycast_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                view_mode = (view_mode + 1) % 3

    player.update()
    raycaster.castAllRays()

    game_surface.fill((0, 0, 0))

    if view_mode == 0:
        map.render(game_surface)
        player.render(game_surface)
        raycaster.render(game_surface, True)

    elif view_mode == 1:
        raycaster.render(game_surface, False)

    elif view_mode == 2:
        topdown_surface.fill((0, 0, 0))
        map.render(topdown_surface)
        player.render(topdown_surface)

        raycast_surface.fill((0, 0, 0))
        raycaster.render(raycast_surface, False)

        left_view = pygame.transform.scale(
            topdown_surface,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        )

        right_view = pygame.transform.scale(
            raycast_surface,
            (WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        )

        game_surface.blit(left_view, (0, 0))
        game_surface.blit(right_view, (WINDOW_WIDTH // 2, 0))

    # Scale the finished game frame onto the larger display
    scaled_surface = pygame.transform.scale(
        game_surface,
        (DISPLAY_WIDTH, DISPLAY_HEIGHT)
    )

    screen.blit(scaled_surface, (0, 0))

    pygame.display.update()