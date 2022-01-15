import pygame
from load_image_function import load_image


class Thing(pygame.sprite.Sprite):
    image_name = 'default.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image(Thing.image_name, -1)
        self.rect = self.image.get_rect()
        self.draw_rect = self.image.get_rect()

    def set_image(self, image_name, *colorkey):
        self.image = load_image(image_name, *colorkey)
        self.draw_rect = self.image.get_rect()
        return self.image


class Cursor(Thing):
    image_name = 'cursor.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image(Cursor.image_name, -1)
        self.rect = self.image.get_rect()
        self.draw_rect = self.rect

    def update(self, pos):
        self.rect.x, self.rect.y = pos
        self.draw_rect = self.rect
