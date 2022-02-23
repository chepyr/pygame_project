import pygame
import modified_group
import things_dir.plant
from main_character import MainCharacter
import field_class
from gameplay import gameplay_management, inventory_class

GRASS_COLOR = (131, 146, 76)
SCREEN_SIZE = (1000, 800)

# is it ok

def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
    pygame.mouse.set_visible(False)
    screen.fill(GRASS_COLOR)

    cursor_group = modified_group.ModifiedGroup()
    things_dir.thing.Cursor(cursor_group)

    # настройки игры
    game = gameplay_management.Game()
    game.resize(screen.get_size())
    axe = things_dir.thing.Axe()
    game.inventory.add_item(axe)

    # Создание спрайтов
    sprites = modified_group.ModifiedGroup()
    for _ in range(20):
        things_dir.plant.Grass(game.field, sprites)
    for _ in range(6):
        new_plant = things_dir.plant.Tree(game.field)
        game.field.trees_group.add(new_plant)

    hero_group = modified_group.ModifiedGroup()
    hero_group.add(game.hero)

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

            # ----------- Обработка событий нажатия кнопок -----------

            if event.type == pygame.KEYDOWN:
                # Нажатие стрелок для передвижения персонажа
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN,
                                 pygame.K_UP]:
                    game.hero.start_moving(event.key)

                # Зажата кнопка 'i' для просмотра инвентаря
                elif event.key == pygame.K_i:
                    game.inventory.enable_active_mode()

                # Зажата кнопка "x" для рубки дерева
                elif event.key == pygame.K_x:
                    for tree in game.field.trees_group:
                        if tree.near_to_the_hero(game.hero.rect) and \
                                game.inventory.has(things_dir.thing.Axe.name):
                            tree.start_chopping()

                elif event.key == pygame.K_LSHIFT:
                    game.hero.start_independent_moving()

                elif event.key == pygame.K_c:
                    game.plant_tree()

            # ----------- Обработка событий поднятия/отжатия(?) кнопок -------
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN,
                                 pygame.K_UP]:
                    game.hero.stop_moving()

                # Отпущена кнопка "x" для рубки дерева
                elif event.key == pygame.K_x:
                    for tree in game.field.trees_group:
                        if tree.is_being_chop:
                            tree.stop_chopping()

                elif event.key == pygame.K_LSHIFT:
                    pass
                    # game.hero.stop_independent_moving()

            # ------------------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.update(event)
                # Проверка на то, что человек хочет рубить деревья
                for tree in game.field.trees_group:
                    # Проверка на то, что игрок стоит рядом с текущим деревом,
                    # у него есть топор в инвентаре и
                    # что игрок щёлкнул по текущему дереву
                    if tree.near_to_the_hero(game.hero.rect) and \
                            tree.pressed_on(event) and \
                            game.inventory.has(things_dir.thing.Axe.name):
                        tree.start_chopping()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Проверка на то, что игрок перестал рубить дерево
                for tree in game.field.trees_group:
                    if tree.is_being_chop:
                        tree.stop_chopping()

        cur_time = clock.tick()

        # Отрисовка всех спрайтов

        sprites.draw(screen)
        game.field.trees_group.update(cur_time)
        game.field.trees_group.draw(screen)

        # Отрсовка героя
        hero_group.update(cur_time, groups=game.field.trees_group)
        hero_group.draw(screen)

        # -------------------------------

        game.draw(screen)
        game.update()
        # Отрисовка курсора
        if pygame.mouse.get_focused():
            cursor_group.update(pygame.mouse.get_pos())
            cursor_group.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
