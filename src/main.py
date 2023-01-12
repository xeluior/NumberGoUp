from constants import *
import pygame


def main():
    pygame.init()

    screen_w = PIXELS_PER_GRID_SQUARE * ARENA_GRID_WIDTH
    screen_h = PIXELS_PER_GRID_SQUARE * ARENA_GRID_HEIGHT
    pixeltype = pygame.font.Font('../resources/font/Pixeltype.ttf', 50)

    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_icon(pygame.image.load('../resources/img/icon.png'))
    pygame.display.set_caption(f'{TITLE} v{VERSION}')

    background = pygame.Surface((screen_w, screen_h))
    background.fill('skyblue')
    hill_surface = pygame.image.load('../resources/img/background/WIP-TitleScreen.png')

    title = pixeltype.render(f'{TITLE}', True, 'black')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        screen.blit(background, ORIGIN)
        screen.blit(hill_surface, (0, screen_h / 2))
        screen.blit(title, ((screen_w - title.get_width()) / 2, screen_h / 2 - title.get_height()))

        pygame.display.update()


if __name__ == "__main__":
    main()
