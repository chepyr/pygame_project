import pygame
from load_image_function import load_image

# Количество древесины, необходимое для разблокировки корабля
NEED_WOOD = 20


class Thing(pygame.sprite.Sprite):
    image_name = 'default.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image(Thing.image_name, -1)
        self.rect = self.image.get_rect()

    def set_image(self, image_name, *colorkey):
        self.image = load_image(image_name, *colorkey)
        return self.image


class Cursor(Thing):
    image_name = 'cursor.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = load_image(Cursor.image_name, -1)
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.rect.x, self.rect.y = pos


class Tool(Thing):
    def __init__(self):
        super().__init__()


class Axe(Tool):
    name = 'axe'

    def __init__(self):
        super().__init__()


class Ship(pygame.sprite.Sprite):
    images = ['ship_0.png', 'ship_1.png', 'ship.png']

    def __init__(self):
        super().__init__()
        self.image = load_image(Ship.images[0], -1)
        self.rect = self.image.get_rect()
        self.rect.x = 850
        self.rect.y = 50

        self.start_image_count = NEED_WOOD / 2
        self.middle_image_count = self.start_image_count + 1 + NEED_WOOD / 2

        self.construction_finished = False

    def update(self, wood_count):
        """Обновляет спрайты корабля по мере сбора древесины"""
        # переход во второй этап строительства
        if wood_count > self.start_image_count:
            self.image = load_image(Ship.images[1], -1)
        # Переход в последний этап строительства
        elif wood_count > self.middle_image_count:
            self.image = load_image(Ship[2], -1)

        # Строительство закончено
        elif wood_count >= NEED_WOOD:
            self.construction_finished = True
