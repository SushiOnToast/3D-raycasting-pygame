import pygame
from settings import *
from map import Map
from player import Player
from raycaster import Raycaster

screen = pygame.display.set_mode((WIDTH, HEIGHT))

map = Map()
player = Player()
raycaster = Raycaster(player, map)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("black")
    raycaster.castAllRays()

    map.render(screen)
    player.render(screen)
    player.update()

    raycaster.render(screen)

    pygame.display.update()
    clock.tick(60)