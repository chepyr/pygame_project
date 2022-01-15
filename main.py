import pygame
from main_character import MainCharacter
from things_dir.plant import Tree, Grass
import modified_group

GRASS_COLOR = (131, 146, 76)
SCREEN_SIZE = (1000, 800)


def main():
    pygame.init()
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(SCREEN_SIZE)
    screen.fill(GRASS_COLOR)

    # sprites = pygame.sprite.Group()
    sprites = modified_group.ModifiedGroup()
    for _ in range(20):
        Grass(sprites)
    for _ in range(8):
        Tree(sprites)

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
                if pressed_button in [79, 80, 81, 82]:
                    hero.moving = True
                    hero.set_moving_direction(pressed_button)

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]:
                    hero.moving = False

        cur_time = clock.tick()
        if hero.moving:
            hero_group.update(cur_time, move=True, groups=sprites)
        sprites.draw(screen)
        hero_group.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
