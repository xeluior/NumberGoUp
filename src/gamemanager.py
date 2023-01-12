import pygame
from level import Level
from sprites import TextSprite
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

    def run(self):
        title_screen = TitleScreen(TITLE, self.font, self.screen.get_size())
        while not title_screen.action():
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit(0)

            title_screen.render_on(self.screen)
            pygame.display.update()

        level = Level(1)


class TitleScreen:
    def __init__(self, title, font, window_size):
        self.background = pygame.Surface(window_size)
        self.set_piece = SetPiece(
            image='../resources/img/background/WIP-TitleScreen.png',
            rect_kwargs={'bottomleft': (0, window_size[1])}
        )
        self.title = TextSprite(title, font)

        self.background.fill('skyblue')
        self.title.rect.midbottom = [window_size[0] / 2, window_size[1] / 2]

    def render_on(self, screen):
        screen.blit(self.background, ORIGIN)
        screen.blit(self.set_piece.image, self.set_piece.rect)
        screen.blit(self.title.image, self.title.rect)

    def action(self):
        if self.title.rect.collidepoint(pygame.mouse.get_pos()):
            self.title.set_color('white')
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            self.title.set_color('black')
            return False


class SetPiece(pygame.sprite.Sprite):
    """
    A sprite subclass that is used to draw decorations on the titlescreen (and possibly other non-grid screens)
    """
    def __init__(self, image: str, rect_kwargs: dict):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect(**rect_kwargs)
