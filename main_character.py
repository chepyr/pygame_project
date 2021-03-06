import random

import pygame
from things_dir.thing import Thing
from load_image_function import load_image

BORDERS = [870, 740]


class MainCharacter(Thing):
    def __init__(self, *group):
        super().__init__(*group)
        self.default_image = load_image('girl_skin.png', -1)
        self.image = self.default_image
        self.moving_to_right_images = []
        for i in range(8):
            current_image = load_image(f'girl_skin_move_right_{i}.png', -1)
            self.moving_to_right_images.append(current_image)
        self.image_blink = load_image('girl_skin_blink.png', -1)

        self.image_left_times = {'moving': 100, 'default': 3000, 'blink': 100}
        self.current_image_left_time = self.image_left_times['default']
        self.current_image_num = 0

        self.draw_rect = self.image.get_rect()

        self.draw_rect.x = random.randrange(0, 800, 4)
        self.draw_rect.y = random.randrange(0, 700, 4)
        self.velocity = 200

        self.moving = False
        self.direction = None
        self.independent_moving = False

        self.rect = pygame.rect.Rect(
            (self.draw_rect.x, self.draw_rect.y + 68), (66, 14))
        self.float_x = self.rect.x
        self.float_y = self.rect.y

        self.is_choping_wood = False

    def update_rects(self, x=0, y=0):
        self.rect.x = x
        self.rect.y = y
        self.draw_rect = pygame.rect.Rect(
            (self.rect.x, self.rect.y - 68), (66, 14))

    def update_image(self):
        if self.moving:
            self.current_image_num = (1 + self.current_image_num) % len(
                self.moving_to_right_images)
            self.image = self.moving_to_right_images[self.current_image_num]
            if self.direction == 'left' or self.direction == 'up':
                self.image = pygame.transform.flip(self.image, True, False)

            self.current_image_left_time = self.image_left_times['moving']
        else:
            if self.image == self.default_image:
                self.image = self.image_blink
                self.current_image_left_time = self.image_left_times['blink']
            else:
                self.image = self.default_image
                self.current_image_left_time = self.image_left_times['default']

    def update(self, time, groups=None):
        if self.moving:
            # ???????????? ????????????????
            self.current_image_left_time -= time * 1.2
            if self.current_image_left_time < 0:
                self.update_image()

            displacement = self.velocity * time / 1000
            self.move(displacement)

            # ???????????????? ???? ?????????????????????? ?? ??????????????????
            there_is_any_intersections = False
            if groups is not None:
                for group in groups:
                    if pygame.sprite.collide_rect(self, group):
                        there_is_any_intersections = True
                        break
                    if self.draw_rect.x < 0 or self.draw_rect.x > BORDERS[0]:
                        there_is_any_intersections = True
                        break
                    if self.draw_rect.y < 0 or self.draw_rect.y > BORDERS[1]:
                        there_is_any_intersections = True
                        break
            if there_is_any_intersections:
                self.move(displacement, reverse=True)

        else:
            self.current_image_left_time -= time
            if self.current_image_left_time < 0:
                self.update_image()

    def start_moving(self, pressed_button):
        self.moving = True
        self.current_image_left_time = self.image_left_times['moving']
        self.update_image()
        self.set_moving_direction(pressed_button)

    def stop_moving(self):
        self.moving = False
        self.current_image_num = 0
        self.image = self.default_image

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

    # def independent_move(self, time):
    #     self.
    #     pass

    def set_moving_direction(self, button):
        directions = {pygame.K_RIGHT: 'right', pygame.K_LEFT: 'left',
                      pygame.K_DOWN: 'down', pygame.K_UP: 'up'}
        self.direction = directions[button]

    def start_independent_moving(self):
        self.independent_moving = True

    def stop_independent_moving(self):
        self.independent_moving = False
