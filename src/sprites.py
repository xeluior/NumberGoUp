import random

from constants import ORIGIN, PIXELS_PER_TILE, TARGET_FRAMERATE
from src.animation import *
from utils import Point, Direction, sign
import pygame
# import scenes


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
    def __init__(self, image_path: str):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.shadow = pygame.image.load('../resources/img/sprites/1x1-shadow.png').convert_alpha()
        self.location = Point(0, 0)
        self.multiplier = 1
        self.move_dir = Direction.ZERO
        self.parent = None

    def draw(self, surface: pygame.Surface, time_increment: int):
        if abs(self.move_dir) < Direction.EPSILON:
            self.move_dir = Direction.ZERO
            self.location = round(self.location)
        move_increment = self.move_dir * (time_increment / 1000 * 20)
        self.move_dir -= move_increment
        surface.blit(self.shadow, self.shadow.get_rect(center=self.anchor_point()))
        surface.blit(self.image, self.image.get_rect(midbottom=self.anchor_point()))

    def apparent_location(self):
        return self.location + self.move_dir

    def anchor_point(self) -> (int, int):
        return (self.apparent_location().x + 0.5) * PIXELS_PER_TILE, (self.apparent_location().y + 0.5) * PIXELS_PER_TILE

    def move(self, direction: Point):
        raise NotImplementedError

    def handle(self, event: pygame.event.Event):
        return

    def update(self):
        return

    def take_damage(self, amount: int):
        raise NotImplementedError


class Enemy(Entity):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.multiplier = 2
        self.damage = 1
        self.health = 8

    def move(self, location):
        path = self.a_star(location)
        if not path:
            return

        if entity := self.parent.entity_at(path[0]):
            if type(entity) == Player and random.random() < 0.1:
                entity.take_damage(self.damage)
        else:
            self.move_dir = self.location - path[0]
            self.location = path[0]

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.insert(0, current)
        return total_path[2:]

    def a_star(self, goal: Point) -> [Point]:
        # possible nodes = [Point(i, j) for i in range(8) for j in range(8)]
        open_set = [self.location]

        came_from = dict.fromkeys([Point(i, j) for i in range(8) for j in range(8)], None)

        g_score = dict.fromkeys([Point(i, j) for i in range(8) for j in range(8)], float('inf'))
        g_score[self.location] = 0

        f_score = dict.fromkeys([Point(i, j) for i in range(8) for j in range(8)], float('inf'))
        f_score[self.location] = self.location.dist(goal)

        while len(open_set) > 0:
            current = min(open_set, key=lambda x: f_score[x])
            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor in current.neighbors():
                if neighbor not in g_score.keys()\
                        or type(self.parent.entity_at(neighbor)) == Enemy:
                    continue

                tentative_g_score = g_score[current] + current.dist(neighbor)
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + neighbor.dist(goal)
                    if neighbor not in open_set:
                        open_set.append(neighbor)

        return None

    def take_damage(self, amount: int):
        self.health -= amount

    def moving(self):
        return self.move_dir != Direction.ZERO

    def apparent_location(self):
        return self.location + self.move_dir


class Player(Entity):
    def __init__(self):
        super().__init__('../resources/img/sprites/player/front.png')
        self.location.x = 4
        self.location.y = 4
        self.turn = True
        self.multiplier = 2
        self.parent = None
        self.buffer: [pygame.Event] = []
        self.anim = AnimationController({
            'walk_down': Animation([
                pygame.image.load('../resources/img/sprites/player/front2.png'),
                pygame.image.load('../resources/img/sprites/player/front3.png'),
                pygame.image.load('../resources/img/sprites/player/front4.png'),
                pygame.image.load('../resources/img/sprites/player/front5.png'),
                pygame.image.load('../resources/img/sprites/player/front6.png'),
                pygame.image.load('../resources/img/sprites/player/front.png'),
            ], framerate=20)
        }, 'walk_down')

    def update(self):
        if not self.moving() and self.turn and len(self.buffer) > 1:
            self.handle(self.buffer.pop())

    def handle(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if self.moving() or not self.turn:
            self.buffer.append(event)

        if event.key == pygame.K_UP:
            self.move(Direction.UP)
        if event.key == pygame.K_DOWN:
            self.move(Direction.DOWN)
        if event.key == pygame.K_LEFT:
            self.move(Direction.LEFT)
        if event.key == pygame.K_RIGHT:
            self.move(Direction.RIGHT)

        # debug controls
        # if event.key == pygame.K_SPACE:
        #     self.turn = False
        # if event.key == pygame.K_RETURN:
        #     self.parent.exit_code = 2 # Level.WON
        # if event.key == pygame.K_TAB:
        #     self.multiplier *= 10

    def moving(self) -> bool:
        return self.move_dir != Point(0, 0)

    def move(self, direction: Point):
        if self.moving(): return

        target = self.location + direction

        if not self.parent.in_bounds(target): return

        if entity := self.parent.entity_at(target):
            entity.take_damage(self.multiplier)
        else:
            self.anim.play('walk_down')
            self.move_dir = self.location - target
            self.location = target

        self.turn = False

    def take_damage(self, amount: int):
        self.multiplier -= amount

    def apparent_location(self):
        return self.location + self.move_dir

    def draw(self, surface: pygame.Surface, time_increment: int):
        self.image = self.anim.frame_advance(time_increment)
        super().draw(surface, time_increment)