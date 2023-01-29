from __future__ import annotations

import math
import random
import pygame

from constants import ORIGIN, PIXELS_PER_TILE, FONT_SIZE
from sprites import TextSprite, Player, Enemy, Entity
from utils import *


class Scene:
    """
    Parent class for all scenes, probably not needed cause Python, but fuck it
    """
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.exit_code = -1
        self._children: [Scene] = []
        self.parent: Scene = None

    def add(self, child: Scene):
        child.parent = self
        self._children.append(child)

    def remove(self, child: Scene | int):
        if child in self._children:
            child.parent = None
            self._children.remove(child)
            return child
        elif child < len(self._children):
            return self._children.pop(child)
        return None

    def child(self, i: int) -> Scene:
        return self._children[i] if i < len(self._children) else None

    def draw(self, surface: pygame.surface.Surface, time_increment: int):
        for child in self._children:
            child.draw(surface, time_increment)

    def update(self):
        for child in self._children:
            child.update()

    def handle(self, event: pygame.event.Event):
        for child in self._children:
            child.handle(event)


class TitleScreen(Scene):
    START_GAME = 1
    EXIT = 2

    def __init__(self, title, font, window_size):
        Scene.__init__(self)

        self.title = TextSprite(title, font, anchor='midbottom')
        pygame.mouse.set_visible(True)

    def draw(self, surface, time_increment: int):
        surface.fill('skyblue')
        self.title.rect.center = (surface.get_width() / 2, surface.get_height() / 2)
        surface.blit(self.title.image, self.title.rect)

    def update(self):
        return

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.title.rect.collidepoint(event.pos):
                self.title.set_color('white')

        if event.type == pygame.MOUSEBUTTONDOWN and self.title.rect.collidepoint(event.pos):
            self.exit_code = self.START_GAME

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.title.set_color('white')
            elif event.key == pygame.K_ESCAPE:
                self.exit_code = self.EXIT

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            self.exit_code = self.START_GAME


class Level(Scene):
    LOST = 1
    WON = 2

    def __init__(self, level: int = 1, score: int = 0):
        Scene.__init__(self)

        self.turns = 0
        self.score = score
        self.score_hud = TextSprite(
            f'{self.score}',
            pygame.font.Font('../resources/font/Pixeltype.ttf', FONT_SIZE),
            'white',
            'topleft',
            (0, 0)
        )
        wood = pygame.image.load('../resources/img/tiles/wood-floor.png').convert()
        self.background = pygame.Surface((wood.get_width() * 10, wood.get_height() * 10))
        for i in range(10):
            for j in range(10):
                self.background.blit(wood, (i * PIXELS_PER_TILE, j * PIXELS_PER_TILE))

        self.add(Player())
        for i in range(round(math.log(level+1, 2))):
            location = Point(random.randrange(8), random.randrange(8))

            while location in [e.location for e in self._children]:
                location = Point(random.randrange(8), random.randrange(8))
            enemy = Enemy('../resources/img/sprites/goblin.png')
            enemy.location = location
            self.add(enemy)
        self.multiplier_hud = TextSprite(
            f'x{self.player().multiplier}',
            pygame.font.Font('../resources/font/Pixeltype.ttf', FONT_SIZE),
            'white',
            'bottomleft'
        )
        pygame.mouse.set_visible(False)

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.exit_code = self.LOST
        super().handle(event)

    def in_bounds(self, point):
        return Point(0, 0) <= point <= Point(7, 7)

    def entity_at(self, point) -> Entity:
        for e in self._children:
            if e.location == point:
                return e
        return None

    def player(self) -> Player | None:
        for e in self._children:
            if type(e) == Player:
                return e

    def draw(self, surface, time_increment):
        surface.blit(self.background, ORIGIN)
        for e in self._children:
            e.draw(surface, time_increment)
        self.multiplier_hud.rect.bottomleft = (0, surface.get_height())
        self.multiplier_hud.set_text(f'x{self.player().multiplier}')
        surface.blit(self.multiplier_hud.image, self.multiplier_hud.rect)

        self.score_hud.set_text(f'{self.score}')
        surface.blit(self.score_hud.image, self.score_hud.rect)

    def update(self):
        super().update()
        if self.player().moving() or self.player().turn:
            return

        for enemy in self._children:
            if enemy == self.player():
                continue

            if enemy.health < 1:
                self.score += self.player().multiplier
                self.player().multiplier *= enemy.multiplier
                self.remove(enemy)
                break

            if enemy.moving():
                continue

            enemy.move(self.player().location)

        if len(self._children) <= 1:
            self.exit_code = Level.WON

        if self.player().multiplier < 1:
            self.exit_code = Level.LOST

        self.turns += 1
        self.player().turn = True
