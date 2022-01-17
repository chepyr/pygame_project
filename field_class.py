from gameplay import inventory_class
import modified_group


class Field:
    def __init__(self, *groups):
        self.groups = groups
        self.dropped_things = modified_group.ModifiedGroup()
        self.shades = []
        self.collected = []

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
        new_wood = inventory_class.Wood()
        new_wood.rect.center = tree_rect.center
        self.dropped_things.add(new_wood)

