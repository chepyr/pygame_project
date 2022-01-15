import random

import pygame.mask

from things_dir.thing import Thing


class Plant(Thing):
    image_name = 'default.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Plant.image_name, -1)
        self.draw_rect.x = random.randrange(900)
        self.draw_rect.y = random.randrange(700)


class Tree(Plant):
    image_name = 'tree.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Tree.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(0, 800, 4)
        self.draw_rect.y = random.randrange(0, 600, 4)
        self.rect = pygame.rect.Rect((self.draw_rect.x + 32, self.draw_rect.y + 116), (68, 16))

class Grass(Plant):
    image_name = 'grass_piece_large.png'

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Grass.image_name, -1)
        self.draw_rect = self.image.get_rect()
        self.draw_rect.x = random.randrange(900)
        self.draw_rect.y = random.randrange(700)
