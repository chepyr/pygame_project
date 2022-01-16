from gameplay import inventory_class
import modified_group


class Field:
    def __init__(self, *groups):
        self.groups = groups
        self.dropped_things = modified_group.ModifiedGroup()

    def update(self):
        self.dropped_things.update()

    def draw(self, screen):
        self.dropped_things.draw(screen)

    def create_wood(self, tree_rect):
        new_wood = inventory_class.Wood()
        new_wood.rect.center = tree_rect.center
        self.dropped_things.add(new_wood)
