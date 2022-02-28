from gameplay import inventory_class
import modified_group
from things_dir.thing import Thing
import pygame


class Background(Thing):
    image_name = "background.png"

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.set_image(Background.image_name)
        self.rect = self.image.get_rect()


class Field:
    def __init__(self, *groups):
        self.trees_group = modified_group.ModifiedGroup()
        self.sprites = modified_group.ModifiedGroup()
        self.dropped_things = modified_group.ModifiedGroup()
        self.shades = []
        self.collected = []
        self.background = pygame.sprite.GroupSingle(Background())

    def update(self, hero_coordinates):
        self.collected = []
        self.dropped_things.update()
        for thing in self.dropped_things:
            if thing.near_to_the_hero(hero_coordinates):
                thing.kill()
                self.collected.append(thing.name)

    def draw(self, screen):
        self.dropped_things.draw(screen)

    def create_wood(self, tree_rect):
        """Метод вызывается из метода Plant.update, когда дерево срубилось"""
        new_wood = inventory_class.Wood()
        new_wood.rect.center = tree_rect.center
        self.dropped_things.add(new_wood)

    def create_seed(self, tree_rect):
        """Метод вызывается из метода Plant.update, когда дерево срубилось"""
        new_seed = inventory_class.Seed()
        new_seed.rect.x = tree_rect.x + 40
        new_seed.rect.y = tree_rect.y + 40
        self.dropped_things.add(new_seed)
