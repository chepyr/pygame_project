import pygame.transform
from things_dir.thing import Thing


class Wood(Thing):
    image_name = 'wood.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(Wood.image_name, -1)
        self.image = pygame.transform.scale(self.image, (100, 50))
