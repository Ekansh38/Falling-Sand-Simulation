import colorsys

import pygame
from pygame.math import Vector2

from constants import FPS, RAINBOW_SPEED, SCREEN_SIZE, SIZE
from grain import Grain

# Functions


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


# Pygame Setup

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
running = True

grains = []
hue = 0


# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    hue += RAINBOW_SPEED
    if hue > 1:
        hue = 0

    color = hsv_to_rgb(hue, 1, 1)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = Vector2(mouse_pos[0], mouse_pos[1])
    mouse_pos.x = mouse_pos.x // SIZE
    mouse_pos.y = mouse_pos.y // SIZE

    if pygame.mouse.get_pressed()[0]:
        grain = Grain(mouse_pos, color)
        grains.append(grain)

    for grain in grains:
        grain.check_collision(grains)
        grain.fall()
        grain.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
