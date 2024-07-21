import colorsys
import random

import pygame
from pygame.math import Vector2


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)


# Constants

SCREEN_SIZE = Vector2(1280, 720)
FPS = 60

SIZE = 10
ROWS = SCREEN_SIZE.y // SIZE
COLS = SCREEN_SIZE.x // SIZE


class Grain:
    def __init__(self, grid_pos, color):
        self.grid_pos = grid_pos
        self.pixel_pos = Vector2(self.grid_pos.x * SIZE, self.grid_pos.y * SIZE)
        self.at_rest = False
        self.vel = 0
        self.acc = 0.1
        self.color = color

    def check_collision(self, grains):
        if not self.at_rest:
            if self.grid_pos.y >= ROWS:
                self.at_rest = True
                self.grid_pos.y = ROWS
                self.pixel_pos = Vector2(self.grid_pos.x * SIZE, self.grid_pos.y * SIZE)

            for grain in grains:
                exp = (
                    grain.grid_pos.y == self.grid_pos.y + 1
                    and grain.grid_pos.x == self.grid_pos.x
                    and grain.at_rest
                )
                if exp:
                    self.at_rest = True
                    self.grid_pos.y = grain.grid_pos.y - 1
                    self.pixel_pos = Vector2(
                        self.grid_pos.x * SIZE, self.grid_pos.y * SIZE
                    )

                    left = True
                    right = True
                    dirs = []

                    for grain in grains:
                        if (
                            Vector2(self.grid_pos.x + 1, self.grid_pos.y + 1)
                            == grain.grid_pos
                            and grain.at_rest
                        ):
                            right = False
                        if (
                            Vector2(self.grid_pos.x - 1, self.grid_pos.y + 1)
                            == grain.grid_pos
                            and grain.at_rest
                        ):
                            left = False

                    if left == True:
                        dirs.append("left")
                    if right == True:
                        dirs.append("right")

                    if dirs:

                        choice = random.choice(dirs)

                        if choice == "left":
                            self.grid_pos.x -= 1
                            self.grid_pos.y += 1
                            self.at_rest = False
                            self.pixel_pos = Vector2(
                                self.grid_pos.x * SIZE, self.grid_pos.y * SIZE
                            )
                        if choice == "right":
                            self.grid_pos.x += 1
                            self.grid_pos.y += 1
                            self.at_rest = False
                            self.pixel_pos = Vector2(
                                self.grid_pos.x * SIZE, self.grid_pos.y * SIZE
                            )

    def fall(self):
        if not self.at_rest:
            self.vel += self.acc
            self.pixel_pos.y += self.vel
            self.grid_pos = Vector2(self.pixel_pos.x // SIZE, self.pixel_pos.y // SIZE)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            ((self.pixel_pos.x - SIZE, self.pixel_pos.y - SIZE), (SIZE, SIZE)),
        )


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

    hue += 0.01  # Change this value to control the speed of the color change
    if hue > 1:
        hue = 0  # Reset hue when it goes past 1

    color = hsv_to_rgb(hue, 1, 1)  # Full saturation and value

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
