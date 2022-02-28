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
    images_names = ['tree_stage_0.png', 'tree_stage_1.png', 'tree_stage_2.png',
                    'tree.png']

    def __init__(self, *groups, age=100):
        super().__init__(*groups)

        self.age = age
        self.growing_velocity = random.randrange(1, 5)
        # Начальная стадия развития - семечко
        self.growing_up_stage = 0
        # Если это уже взрослое дерево, то присваиваем ему 2ую стадию
        if self.age >= 100:
            self.growing_up_stage = 3

        self.update_image()

        self.left_to_chop = 100
        self.chopping_velocity = 100
        self.is_being_chop = False

    def near_to_the_hero(self, hero_coords):
        accessible_radius = 150
        tree_center = self.rect.center
        hero_center = hero_coords.center
        x_distance = (tree_center[0] - hero_center[0]) ** 2
        y_distance = (tree_center[1] - hero_center[1]) ** 2
        distance = (x_distance + y_distance) ** 0.5

        return distance < accessible_radius

    def start_chopping(self):
        if self.growing_up_stage == 3:
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
                self.field.create_wood(self.draw_rect)
                self.field.create_seed(self.draw_rect)
                self.kill()

        # Увеличиваем возраст растения, если оно ещё растёт
        if self.age < 100:
            self.age += time * self.growing_velocity / 1000

        # Растение переходит в этап ростка
        if self.age > 30 and self.growing_up_stage < 1:
            self.growing_up_stage = 1
            self.update_image(same_coords=True)

        # Растение становится молодым
        if self.age > 70 and self.growing_up_stage < 2:
            self.growing_up_stage = 2
            self.update_image(same_coords=True)

        # Растение становится взрослым
        if self.age > 100 and self.growing_up_stage < 3:
            self.growing_up_stage = 3
            self.update_image(same_coords=True)

    def update_image(self, same_coords=False):
        cur_image_name = Tree.images_names[self.growing_up_stage]
        self.image = self.set_image(cur_image_name, -1)

        if not same_coords:
            self.draw_rect = self.image.get_rect()
            self.draw_rect.x = random.randrange(0, 700, 4)
            self.draw_rect.y = random.randrange(0, 500, 4)
            self.rect = pygame.rect.Rect(
                (self.draw_rect.x + 32, self.draw_rect.y + 116), (68, 16))


class Grass(Plant):
    image_name = 'grass_piece_large.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Grass.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(900)
        self.draw_rect.y = random.randrange(700)
