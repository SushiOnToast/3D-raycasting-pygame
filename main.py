import pygame
from settings import *
from map import Map
from player import Player

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

map = Map()
player = Player()

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player.update()


    screen.fill((0, 0, 0))

    map.render(screen)
    player.render(screen)
    pygame.display.update()