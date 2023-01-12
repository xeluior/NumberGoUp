from constants import *
import pygame


def main():
    screen_w = PIXELS_PER_GRID_SQUARE * ARENA_GRID_WIDTH
    screen_h = PIXELS_PER_GRID_SQUARE * ARENA_GRID_HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((screen_w, screen_h))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        pygame.display.update()


if __name__ == "__main__":
    main()
