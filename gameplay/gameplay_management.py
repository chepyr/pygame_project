import gameplay
import things_dir
import modified_group
import pygame


class Game:
    def __init__(self):
        self.inventory = Inventory()
        self.menu = Menu()
        self.taskbar = Taskbar(self.inventory, self.menu)

    def update(self, *args):
        self.taskbar.update(*args)

    def draw(self, screen):
        self.taskbar.draw(screen)

    def resize(self, new_size):
        self.taskbar.resize(new_size)


class Taskbar(things_dir.thing.Thing):
    image_name = 'taskbar.png'

    def __init__(self, inventory, menu):
        super().__init__()
        self.image = self.set_image(Taskbar.image_name)
        self.rect = self.image.get_rect()
        self.height = self.rect.height

        self.inventory = inventory
        self.menu = menu
        self.clickable_items = [self.inventory, self.menu]

        self.group = modified_group.ModifiedGroup()
        self.group.add(self, self.inventory, self.menu)

    def update(self, *args):
        for item in self.clickable_items:
            if item.pressed_on(*args):
                item.enable_active_mode()

    def draw(self, screen):
        self.group.draw(screen)

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.image, (
            new_size[0], self.image.get_size()[1]))
        self.rect.y = new_size[1] - self.height

        self.inventory.update_coordinates(self.rect)
        self.menu.update_coordinates(self.rect, new_size)


class Menu(things_dir.thing.Thing):
    image_button = 'menu.png'

    def __init__(self):
        super().__init__()
        self.inventory_content = list()
        self.image = self.set_image(Menu.image_button, -1)
        self.rect = self.image.get_rect()

    def pressed_on(self, *args):
        return args and args[0].type == pygame.MOUSEBUTTONDOWN and \
               self.rect.collidepoint(args[0].pos)

    def update_coordinates(self, taskbar_rect):
        self.rect.x = taskbar_rect.x + 100
        self.rect.y = taskbar_rect.y + 32

    def enable_active_mode(self):
        print('Вы в меню')

    def update_coordinates(self, taskbar_rect, new_screen_size):
        self.rect.x = new_screen_size[0] - 100 - self.rect.width
        self.rect.y = taskbar_rect.y + 32


class Inventory(things_dir.thing.Thing):
    image_button = 'inventory.png'

    def __init__(self):
        super().__init__()
        self.inventory_content = list()
        self.image = self.set_image(Inventory.image_button, -1)
        self.rect = self.image.get_rect()

    def enable_active_mode(self):
        print('Содержимое инвентаря: ', end='')
        for item in self.inventory_content:
            print(item.name, end=' ')
        print()

    def add_item(self, new_item):
        self.inventory_content.append(new_item)

    def has(self, find_item):
        for item in self.inventory_content:
            if item.name == find_item:
                return True
        return False

    def pressed_on(self, *args):
        return args and args[0].type == pygame.MOUSEBUTTONDOWN and \
               self.rect.collidepoint(args[0].pos)

    def update_coordinates(self, taskbar_rect):
        self.rect.x = taskbar_rect.x + 100
        self.rect.y = taskbar_rect.y + 32
