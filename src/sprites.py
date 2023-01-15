import random

from constants import ORIGIN, PIXELS_PER_GRID_SQUARE
from utils import Point, Direction
import pygame


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text='', font=None, color='black', anchor='center', pos=ORIGIN):
        self.__font = font
        self.__text = text
        self.__color = color
        self.__anchor = anchor
        self.image = self.__font.render(self.__text, False, self.__color)
        self.rect = self.image.get_rect(**{anchor: pos})

    def set_text(self, new_text: str):
        self.__text = new_text
        self.render()

    def set_color(self, new_color):
        self.__color = new_color
        self.render()

    def set_font(self, new_font):
        self.__font = new_font
        self.render()

    def render(self):
        rect_anchor = {self.__anchor: getattr(self.rect, self.__anchor)}
        self.image = self.__font.render(self.__text, False, self.__color)
        self.rect = self.image.get_rect(**rect_anchor)


class Entity:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.shadow = pygame.image.load('../resources/img/sprites/1x1-shadow.png').convert_alpha()
        self.location = Point(0, 0)
        self.multiplier = 1

    def draw(self, surface):
        surface.blit(self.shadow, self.shadow.get_rect(center=self.anchor_point()))
        surface.blit(self.image, self.image.get_rect(midbottom=self.anchor_point()))

    def anchor_point(self):
        return (self.location.x + 0.5) * PIXELS_PER_GRID_SQUARE, (self.location.y + 0.5) * PIXELS_PER_GRID_SQUARE


class Enemy(Entity):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.multiplier = 2
        self.damage = 1
        self.health = 8

    def move(self, direction, level):
        if level.player.turn: return

        entity = level.entity_at(self.location + direction)
        if entity:
            if entity == level.player and random.random() < 0.05:
                entity.multiplier -= self.damage
        else:
            self.location += direction


class Player(Entity):
    def __init__(self):
        super().__init__('../resources/img/sprites/player.png')
        self.location.x = 4
        self.location.y = 4
        self.turn = True

    def move(self, direction, level):
        if not self.turn: return

        if entity := level.entity_at(self.location + direction):
            entity.health -= self.multiplier
        else:
            self.location += direction

        self.turn = False
