import pygame.transform
from things_dir.thing import Thing


class DroppedDownThing(Thing):
    def __init__(self):
        super().__init__()
        self.image = self.set_image(Thing.image_name, -1)
        self.name = None

    def near_to_the_hero(self, hero_coordinates):
        hero_center = hero_coordinates.center
        if self.rect.x <= hero_center[0] <= self.rect.right and \
                self.rect.y <= hero_center[1] <= self.rect.bottom:
            return True
        return False


class Wood(DroppedDownThing):
    image_name = 'wood.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(Wood.image_name, -1)
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.name = 'wood'


class Seed(DroppedDownThing):
    image_name = 'seed.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(Seed.image_name, -1)
        self.name = 'seed'
