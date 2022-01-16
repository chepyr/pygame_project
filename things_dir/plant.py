import random

import pygame.mask
import pygame
from things_dir.thing import Thing


class Plant(Thing):
    image_name = 'default.png'

    def __init__(self, field=None, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Plant.image_name, -1)
        self.rect.x = 0
        self.rect.y = 0
        self.field = field


class Tree(Plant):
    image_name = 'tree.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Tree.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(0, 800, 4)
        self.draw_rect.y = random.randrange(0, 600, 4)
        self.rect = pygame.rect.Rect(
            (self.draw_rect.x + 32, self.draw_rect.y + 116), (68, 16))

        self.left_to_chop = 100
        self.chopping_velocity = 50
        self.is_being_chop = False

    def near_to_the_hero(self, hero_coords):
        accessible_radius = 80
        tree_center = self.rect.center
        hero_center = hero_coords.center
        x_distance = (tree_center[0] - hero_center[0]) ** 2
        y_distance = (tree_center[1] - hero_center[1]) ** 2
        distance = (x_distance + y_distance) ** 0.5

        return distance < accessible_radius

    def start_chopping(self):
        self.is_being_chop = True

    def stop_chopping(self):
        self.is_being_chop = False

    def pressed_on(self, *args):
        return args and args[0].type == pygame.MOUSEBUTTONDOWN and \
               self.draw_rect.collidepoint(args[0].pos)

    def update(self, time):
        if self.is_being_chop:
            self.left_to_chop -= time * self.chopping_velocity / 1000
            if self.left_to_chop <= 0:
                print('Дерево срублено')
                self.kill()
                self.field.create_wood(self.draw_rect)


class Grass(Plant):
    image_name = 'grass_piece_large.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Grass.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(900)
        self.draw_rect.y = random.randrange(700)
