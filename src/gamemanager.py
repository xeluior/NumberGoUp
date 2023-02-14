from math import floor

import pygame
import scenes
import sprites
from constants import *


class GameManager:
    def __init__(self):
        self.screen_w = PIXELS_PER_TILE * ARENA_GRID_WIDTH
        self.screen_h = PIXELS_PER_TILE * ARENA_GRID_HEIGHT
        screen_title = f"{TITLE} v{VERSION}"

        pygame.init()

        self.font = pygame.font.Font('resources/font/Pixeltype.ttf', FONT_SIZE)
        icon = pygame.image.load('resources/img/icon.png')

        pygame.display.set_icon(icon)
        pygame.display.set_caption(screen_title)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.RESIZABLE)

        self.score = 0

    def run(self):
        title_screen = scenes.TitleScreen(TITLE, self.font, (self.screen_w, self.screen_h))
        if self.event_loop(title_screen) != scenes.TitleScreen.START_GAME:
            return

        while True:
            for current_level in range(FINAL_LEVEL):
                level = scenes.Level(current_level+1, self.score)
                result = self.event_loop(level)

                if result == scenes.Level.LOST:
                    self.score = level.score
                    print(f'level {current_level+1}: {self.score} ({self.score / (current_level+1)})')
                    break
                elif result == scenes.Level.WON:
                    self.score = level.score + (current_level + 1) * floor(max((64 - level.turns) / 16, 0))

            score_disp = scenes.TitleScreen(str(self.score), self.font, (self.screen_w, self.screen_h))
            if self.event_loop(score_disp) != scenes.TitleScreen.START_GAME:
                return
            self.score = 0

    def event_loop(self, scene):
        clock = pygame.time.Clock()
        scene_surf = pygame.Surface(size=(self.screen_w, self.screen_h))
        while scene.exit_code < 0:
            time_increment = clock.tick()
            scene.update()
            scene.draw(scene_surf, time_increment)

            # apply scaling to the scene to fit the current window size
            window_size = pygame.display.get_window_size()
            window_center = (window_size[0] / 2, window_size[1] / 2)
            scene_size = scene_surf.get_size()
            scale_factor = min(
                        window_size[0]/scene_size[0],
                        window_size[1]/scene_size[1]
                    )
            scale_factor = floor(scale_factor) if INTEGER_SCALING else scale_factor
            new_size = (scene_size[0] * scale_factor, scene_size[1] * scale_factor)
            scaled_scene = pygame.transform.scale(scene_surf, new_size)
            scene_pos = (
                (window_size[0] - scaled_scene.get_width()) / 2,
                (window_size[1] - scaled_scene.get_height()) / 2
            )
            self.screen.blit(
                scaled_scene,
                scene_pos
            )

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                else:
                    if hasattr(event, 'pos'):
                        event.pos = (
                            (event.pos[0] - scene_pos[0]) / scale_factor,
                            (event.pos[1] - scene_pos[1]) / scale_factor
                        )
                    scene.handle(event)

        return scene.exit_code
