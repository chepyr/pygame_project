import pygame
import modified_group
import things_dir.plant
from main_character import MainCharacter
import field_class
from gameplay import gameplay_management, inventory_class

GRASS_COLOR = (131, 146, 76)
SCREEN_SIZE = (1000, 800)


def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    screen.fill(GRASS_COLOR)

    cursor_group = modified_group.ModifiedGroup()
    things_dir.thing.Cursor(cursor_group)

    # настройки игры
    field = field_class.Field()
    game = gameplay_management.Game()
    game.resize(screen.get_size())
    axe = things_dir.thing.Axe()
    game.inventory.add_item(axe)

    # Создание спрайтов
    sprites = modified_group.ModifiedGroup()
    trees_sprites = modified_group.ModifiedGroup()
    for _ in range(20):
        things_dir.plant.Grass(field, sprites)
    for _ in range(6):
        things_dir.plant.Tree(field, trees_sprites)
    hero_group = modified_group.ModifiedGroup()
    hero = MainCharacter(hero_group)

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(GRASS_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Изменение размеров окна
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
                game.resize(screen.get_size())

            if event.type == pygame.KEYDOWN:
                pressed_button = pygame.key.get_pressed().index(1)
                # Нажатие стрелок для передвижения персонажа
                if pressed_button in [79, 80, 81, 82]:
                    hero.start_moving(pressed_button)

                # Зажата кнопка 'i' для просмотра инвентаря
                elif pressed_button == 12:
                    game.inventory.enable_active_mode()

                else:
                    print(pressed_button)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN,
                                 pygame.K_UP]:
                    hero.stop_moving()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.update(event)
                # Проверка на то, что человек хочет рубить деревья
                for tree in trees_sprites:
                    # Проверка на то, что игрок стоит рядом с текущим деревом,
                    # у него есть топор в инвентаре и
                    # что игрок щёлкнул по текущему дереву
                    if tree.near_to_the_hero(hero.rect) and \
                            tree.pressed_on(event) and \
                            game.inventory.has(things_dir.thing.Axe.name):
                        tree.start_chopping()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Проверка на то, что игрок перестал рубить дерево
                for tree in trees_sprites:
                    if tree.is_being_chop:
                        tree.stop_chopping()

        cur_time = clock.tick()

        # Отрисовка всех спрайтов

        sprites.draw(screen)
        trees_sprites.update(cur_time)
        trees_sprites.draw(screen)

        field.update()
        field.draw(screen)

        # Отрсовка героя
        hero_group.update(cur_time, groups=trees_sprites)
        hero_group.draw(screen)

        # -------------------------------

        game.draw(screen)
        # Отрисовка курсора
        if pygame.mouse.get_focused():
            cursor_group.update(pygame.mouse.get_pos())
            cursor_group.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
