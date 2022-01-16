import pygame
import modified_group
import things_dir.plant
from main_character import MainCharacter
import inventory_class

GRASS_COLOR = (131, 146, 76)
SCREEN_SIZE = (1000, 800)


def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.mouse.set_visible(False)
    screen.fill(GRASS_COLOR)

    cursor_group = modified_group.ModifiedGroup()
    things_dir.thing.Cursor(cursor_group)

    sprites = modified_group.ModifiedGroup()
    trees_sprites = modified_group.ModifiedGroup()

    # Инвентарь
    axe = things_dir.thing.Axe()
    inventory = inventory_class.Inventory()
    inventory.add_item(axe)

    for _ in range(20):
        things_dir.plant.Grass(sprites)
    for _ in range(3):
        things_dir.plant.Tree(trees_sprites)

    hero_group = modified_group.ModifiedGroup()
    hero = MainCharacter(hero_group)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(GRASS_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                pressed_button = pygame.key.get_pressed().index(1)
                # Нажатие стрелок для передвижения персонажа
                if pressed_button in [79, 80, 81, 82]:
                    hero.moving = True
                    hero.set_moving_direction(pressed_button)

                # Зажата кнопка 'i' для просмотра инвентаря
                elif pressed_button == 12:
                    inventory.print_content()

                else:
                    print(pressed_button)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN,
                                 pygame.K_UP]:
                    hero.moving = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Проверка на то, что человек хочет рубить деревья
                for tree in trees_sprites:
                    # Проверка на то, что игрок стоит рядом с текущим деревом,
                    # у него есть топор в инвентаре и
                    # что игрок щёлкнул по текущему дереву
                    if tree.near_to_the_hero(hero.rect) and \
                            tree.pressed_on(event) and \
                            inventory.has(things_dir.thing.Axe.name):
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

        # Отрсовка героя
        if hero.moving:
            hero_group.update(cur_time, move=True, groups=trees_sprites)
        hero_group.draw(screen)

        # Отрисовка курсора
        if pygame.mouse.get_focused():
            cursor_group.update(pygame.mouse.get_pos())
            cursor_group.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
