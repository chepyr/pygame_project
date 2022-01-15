import random

import pygame
from things_dir.thing import Thing
from load_image_function import load_image


class MainCharacter(Thing):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image('girl_skin.png', -1)
        self.draw_rect = self.image.get_rect()

        self.draw_rect.x = random.randrange(0, 800, 4)
        self.draw_rect.y = random.randrange(0, 700, 4)
        self.velocity = 300
        self.moving = False

        self.rect = pygame.rect.Rect((self.draw_rect.x, self.draw_rect.y + 68), (66, 14))
        self.float_x = self.rect.x
        self.float_y = self.rect.y

    def update_rects(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y
        self.draw_rect = pygame.rect.Rect((self.rect.x, self.rect.y - 68), (66, 14))

    def update(self, time, move=False, groups=None):
        if move:
            displacement = self.velocity * time / 1000
            self.move(displacement)

            there_is_any_intersections = False
            if groups is not None:
                for group in groups:
                    if pygame.sprite.collide_rect(self, group):
                        there_is_any_intersections = True
                        break
            if there_is_any_intersections:
                self.move(displacement, reverse=True)

    def move(self, displacement, reverse=False):
        if reverse:
            displacement *= -1

        if self.direction == 'right':
            self.float_x += displacement
        elif self.direction == 'left':
            self.float_x -= displacement
        elif self.direction == 'down':
            self.float_y += displacement
        elif self.direction == 'up':
            self.float_y -= displacement
        self.update_rects(x=int(self.float_x), y=int(self.float_y))

    def set_moving_direction(self, button):
        directions = {79: 'right', 80: 'left', 81: 'down', 82: 'up'}
        self.direction = directions[button]
