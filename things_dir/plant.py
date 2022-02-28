import random

import pygame.mask
import pygame
from things_dir.thing import Thing
from main import FIELD_SIZE


class Plant(Thing):
    image_name = 'default.png'

    def __init__(self, field=None, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Plant.image_name, -1)
        self.rect.x = 0
        self.rect.y = 0
        self.field = field
        self.center = [0, 0]


class Tree(Plant):
    image_name = 'tree.png'
    images_names = ['tree_stage_0.png', 'tree_stage_1.png', 'tree_stage_2.png',
                    'tree.png']

    def __init__(self, *groups, age=100, field=None):
        super().__init__(*groups)

        self.age = age
        self.growing_velocity = random.randrange(1, 8)
        # Начальная стадия развития - семечко
        self.growing_up_stage = 0
        # Если это уже взрослое дерево, то присваиваем ему 2ую стадию
        if self.age >= 100:
            self.growing_up_stage = 3

        self.update_image()

        self.left_to_chop = 100
        self.chopping_velocity = 100
        self.is_being_chop = False
        self.field = field

    def near_to_the_hero(self, hero_coords):
        """Возвращает True, если дерево находится в близком к герою радиусе"""
        accessible_radius = 150
        tree_center = self.rect.center
        hero_center = hero_coords.center
        x_distance = (tree_center[0] - hero_center[0]) ** 2
        y_distance = (tree_center[1] - hero_center[1]) ** 2
        distance = (x_distance + y_distance) ** 0.5

        return distance < accessible_radius

    def start_chopping(self):
        # Проверка на то, что дерево выросшее
        if self.growing_up_stage == 3:
            self.is_being_chop = True

    def stop_chopping(self):
        self.is_being_chop = False

    def pressed_on(self, *args):
        """Проверка на то, что пользователь нажимает кнопкой мышии на дерево"""
        return args and args[0].type == pygame.MOUSEBUTTONDOWN and \
               self.draw_rect.collidepoint(args[0].pos)

    def update(self, time):
        """Обновление состояния дерева: уменьшение количества оставшейся жизни,
            изменение спрайтов по мере роста"""
        if self.is_being_chop:
            # Если дерево находится в процессе рубки,
            # то уменьшаем оставшееся у него количество "жизни"
            self.left_to_chop -= time * self.chopping_velocity / 1000

            # Если у дерева закончилась "жизнь", то удаляем его,
            # а на его месте на поле выпадаюи семечко и кусок древесины
            if self.left_to_chop <= 0:
                # Вероятность выпадения второго элемента
                second_wood_drop_probability = 40
                second_seed_drop_probability = 30
                # Колмчество элементов
                count_wood = 1 + bool(
                    random.randrange(100) < second_wood_drop_probability)
                count_seed = 1 + bool(random.randrange(
                    100) < second_seed_drop_probability)

                for wood_i in range(count_wood):
                    # При итерации у каждого следующего объекта
                    # делаем смещение на 10 пикселей вправо и вниз
                    rect = pygame.rect.Rect(
                        (self.draw_rect.x + wood_i * 10,
                         self.draw_rect.y + wood_i * 10),
                        (self.draw_rect.w, self.draw_rect.h))
                    self.field.create_wood(rect)

                for seed_i in range(count_seed):
                    # При итерации у каждого следующего объекта
                    # делаем смещение на 10 пикселей вправо и вниз
                    rect = pygame.rect.Rect(
                        (self.draw_rect.x + seed_i * 10,
                         self.draw_rect.y + seed_i * 10),
                        (self.draw_rect.w, self.draw_rect.h))
                    self.field.create_seed(rect)

                self.kill()
                del self
                return

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
        """Обновляет спрайт дерева"""
        cur_image_name = Tree.images_names[self.growing_up_stage]
        self.image = self.set_image(cur_image_name, -1)

        # Если у дерева нужно генерировать новые координаты (это новый росток)
        if not same_coords:
            self.draw_rect = self.image.get_rect()
            self.draw_rect.x = random.randrange(0, FIELD_SIZE[0], 4)
            self.draw_rect.y = random.randrange(0, FIELD_SIZE[1] - 100, 4)
            self.rect = pygame.rect.Rect(
                (self.draw_rect.x + 32, self.draw_rect.y + 116), (68, 16))
            self.center = self.rect.center

        # Если это новый росток, то подгоняем rect'ы под размер картинки
        if self.growing_up_stage == 0:
            self.draw_rect = self.image.get_rect()
            self.draw_rect.center = self.center
            self.rect = pygame.rect.Rect(
                (self.draw_rect.x + 20, self.draw_rect.y + 30), (20, 10))

        if self.growing_up_stage == 3:
            self.draw_rect = self.image.get_rect()
            self.draw_rect.center = self.center
            self.rect = pygame.rect.Rect(
                (self.draw_rect.x + 32, self.draw_rect.y + 116), (68, 16))


class Grass(Plant):
    image_name = 'grass_piece_large.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Grass.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(FIELD_SIZE[0])
        self.draw_rect.y = random.randrange(FIELD_SIZE[1])
