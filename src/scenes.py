import random
import pygame
import pygame.sprite

from constants import ORIGIN, PIXELS_PER_GRID_SQUARE
from sprites import TextSprite, Player, Enemy
from utils import *


class Scene:
    """
    Parent class for all scenes, probably not needed cause Python, but fuck it
    """
    def __init__(self):
        self.exit_code = -1

    def draw(self, surface):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class TitleScreen(Scene):
    START_GAME = 1

    def __init__(self, title, font, window_size):
        Scene.__init__(self)

        self.background = pygame.Surface(window_size)
        self.title = TextSprite(title, font, anchor='midbottom', pos=(window_size[0]/2, window_size[1]/2))

        self.background.fill('skyblue')

    def draw(self, surface):
        surface.blit(self.background, ORIGIN)
        surface.blit(self.title.image, self.title.rect)

    def update(self):
        if self.title.rect.collidepoint(pygame.mouse.get_pos()):
            self.title.set_color('white')
            if pygame.mouse.get_pressed()[0]:
                self.exit_code = self.START_GAME
        else:
            self.title.set_color('black')


class Level(Scene):
    LOST = 1
    WON = 2

    def __init__(self, level: int):
        Scene.__init__(self)

        self.turns = 0
        self.wood = pygame.image.load('../resources/img/tiles/wood-floor.png').convert()
        self.stone = pygame.image.load('../resources/img/tiles/stone-brick.png').convert()
        self.score = 0
        self.player = Player()
        self.enemies = []

        for i in range(4):
            location = Point(random.randrange(8), random.randrange(8))

            if not (location in [e.location for e in self.enemies]
                    or location == self.player.location):
                enemy = Enemy('../resources/img/sprites/goblin.png')
                enemy.location = location
                self.enemies.append(enemy)

    def entity_at(self, point):
        if self.player.location == point:
            return self.player
        for enemy in self.enemies:
            if enemy.location == point:
                return enemy
        return None

    def draw(self, surface):
        for i in range(8):
            for j in range(8):
                tile = self.wood if (i + j) % 2 else self.stone
                surface.blit(tile, (i * PIXELS_PER_GRID_SQUARE, j * PIXELS_PER_GRID_SQUARE))
        self.player.draw(surface)
        for enemy in self.enemies:
            enemy.draw(surface)

    def update(self):
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_DOWN:
                self.player.move(Direction.DOWN, self)
            if event.key == pygame.K_UP:
                self.player.move(Direction.UP, self)
            if event.key == pygame.K_LEFT:
                self.player.move(Direction.LEFT, self)
            if event.key == pygame.K_RIGHT:
                self.player.move(Direction.RIGHT, self)

        if not self.player.turn:
            for enemy in self.enemies:
                if enemy.health < 1:
                    self.player.multiplier *= enemy.multiplier
                    self.score += 1
                    self.enemies.remove(enemy)

                if len(self.enemies) < 1:
                    self.exit_code = Level.WON

                dist = self.player.location - enemy.location

                if abs(dist.x) > abs(dist.y):
                    if dist.x > 0:
                        enemy.move(Direction.RIGHT, self)
                    else:
                        enemy.move(Direction.LEFT, self)
                else:
                    if dist.y > 0:
                        enemy.move(Direction.DOWN, self)
                    else:
                        enemy.move(Direction.UP, self)

            if self.player.multiplier < 1:
                self.exit_code = Level.LOST
            self.player.turn = True
