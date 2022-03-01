import gameplay
import things_dir
import modified_group
import pygame
import field_class
import main_character
from PIL import Image, ImageDraw, ImageFont

from things_dir.thing import NEED_WOOD

class Game:
    def __init__(self, screen_size):
        self.screen_size = screen_size

        self.inventory = Inventory()
        self.menu = Menu()
        self.resources = AllResources()
        self.taskbar = Taskbar(self.inventory, self.menu, self.resources)
        self.field = field_class.Field()
        self.hero = main_character.MainCharacter()
        self.ship = pygame.sprite.GroupSingle(things_dir.thing.Ship())

        self.game_over = None

    def update(self, *args):
        if args:
            self.taskbar.update(*args)

        self.field.update(self.hero.rect)
        self.add_collected_things(self.field.collected)
        self.resources.update()
        self.ship.update(self.resources.wood_resource.count)

        if self.ship.sprite.construction_finished:
            self.game_over = pygame.sprite.GroupSingle((GameOver(self.screen_size)))


    def draw(self, screen):
        self.ship.draw(screen)
        self.taskbar.draw(screen)
        self.field.draw(screen)

        if self.game_over is not None:
            self.game_over.draw(screen)

    def add_collected_things(self, collected_things):
        """Если игрок собрал какую-то вещь с поля,
            то увеличиваем значение соответстующего ресурса"""
        for item in collected_things:
            if item == 'wood':
                self.resources.wood_resource.increase(1)
            elif item == 'seed':
                self.resources.seed_resource.increase(1)

    def resize(self, new_size):
        self.taskbar.resize(new_size)

    def plant_tree(self):
        """Высаживает новое дерево (если у игрока есть семена)"""
        # Проверка на наличие семян у игрока
        if self.resources.seed_resource.count > 0:
            # Сажаем новое дерево
            new_plant = things_dir.plant.Tree(field=self.field, age=0)
            self.field.trees_group.add(new_plant)
            self.field.sprites.add(new_plant)

            # Уменьшаем количество семян у игрока
            self.resources.seed_resource.increase(-1)


class GameOver(things_dir.thing.Thing):
    image_name = 'game_over.png'

    def __init__(self, screen_size):
        super().__init__()
        self.image = self.set_image(GameOver.image_name, -1)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_size[0] / 2, screen_size[1] / 2)


class Taskbar(things_dir.thing.Thing):
    image_name = 'taskbar.png'

    def __init__(self, inventory, menu, resources):
        super().__init__()
        self.image = self.set_image(Taskbar.image_name)
        self.rect = self.image.get_rect()
        self.height = self.rect.height

        self.inventory = inventory
        self.menu = menu
        self.clickable_items = [self.inventory, self.menu]
        self.resources = resources

        self.emblems = modified_group.ModifiedGroup(
            (WoodEmblem(), SeedEmblem()))

        self.group = modified_group.ModifiedGroup()
        self.group.add(self, self.inventory, self.menu)

    def update(self, *args):
        for item in self.clickable_items:
            if item.pressed_on(*args):
                item.enable_active_mode()

    def draw(self, screen):
        self.group.draw(screen)
        self.resources.draw(screen)
        self.emblems.draw(screen)

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


class AllResources(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.wood_resource = WoodResource()
        self.seed_resource = SeedResource()
        self.resources = [self.wood_resource, self.seed_resource]
        self.add(*self.resources)


class Resource(things_dir.thing.Thing):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.group = pygame.sprite.GroupSingle()
        self.wood = False

    def update_image(self):
        text_color = (105, 76, 53)
        stroke_color = (58, 41, 46)
        font = ImageFont.truetype("arial.ttf", 30)
        image = Image.new('RGB', (100, 100), (0, 0, 0))
        draw = ImageDraw.Draw(image)

        if self.wood:
            draw.text((10, 10), text=f'{self.count} / {NEED_WOOD}',
                      fill=text_color,
                      align="center", font=font, stroke_width=2,
                      stroke_fill=stroke_color)
        else:
            draw.text((10, 10), text=f'{self.count}',
                      fill=text_color,
                      align="center", font=font, stroke_width=2,
                      stroke_fill=stroke_color)

        image_bytes = image.tobytes()
        self.image = pygame.image.fromstring(image_bytes, (100, 100), 'RGB')
        self.image = self.image.convert()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)

    def update(self):
        self.update_image()


class WoodResource(Resource):
    image_name = 'wood.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(WoodResource.image_name, -1)
        self.rect.x = 180
        self.rect.y = 810
        self.wood = True

    def increase(self, count):
        self.count += count


class SeedResource(Resource):
    image_name = 'seed.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(SeedResource.image_name, -1)
        self.rect.x = 500
        self.rect.y = 810

    def increase(self, count):
        self.count += count


class WoodEmblem(things_dir.thing.Thing):
    image_name = 'wood.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(WoodEmblem.image_name, -1)
        self.image = pygame.transform.scale(self.image, (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 810


class SeedEmblem(things_dir.thing.Thing):
    image_name = 'seed.png'

    def __init__(self):
        super().__init__()
        self.image = self.set_image(SeedEmblem.image_name, -1)
        self.rect = self.image.get_rect()
        self.rect.x = 550
        self.rect.y = 810
