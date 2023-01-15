import pygame
import scenes
from constants import *


class GameManager:
    def __init__(self):
        screen_w = PIXELS_PER_GRID_SQUARE * ARENA_GRID_WIDTH
        screen_h = PIXELS_PER_GRID_SQUARE * ARENA_GRID_HEIGHT
        screen_title = f"{TITLE} v{VERSION}"

        pygame.init()

        self.font = pygame.font.Font('../resources/font/Pixeltype.ttf', FONT_SIZE)
        icon = pygame.image.load('../resources/img/icon.png')

        pygame.display.set_icon(icon)
        pygame.display.set_caption(screen_title)
        self.screen = pygame.display.set_mode((screen_w, screen_h))

        self.score = 0

    def run(self):
        title_screen = scenes.TitleScreen(TITLE, self.font, self.screen.get_size())
        if self.event_loop(title_screen) != scenes.TitleScreen.START_GAME:
            return

        while True:
            for current_level in range(32):
                level = scenes.Level(current_level+1)
                result = self.event_loop(level)

                if result == scenes.Level.LOST:
                    self.score += level.score
                    break
                elif result == scenes.Level.WON:
                    self.score += level.score

            score_disp = scenes.TitleScreen(str(self.score), self.font, self.screen.get_size())
            if self.event_loop(score_disp) != scenes.TitleScreen.START_GAME:
                return
            self.score = 0


    def event_loop(self, scene):
        clock = pygame.time.Clock()
        while scene.exit_code < 0:
            if len(pygame.event.get(pygame.QUIT)):
                pygame.quit()
                exit(0)

            scene.update()
            scene.draw(self.screen)

            clock.tick(60)
            pygame.display.update()

        return scene.exit_code
