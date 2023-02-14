from __future__ import annotations

import random
import pygame
import pygame.image

from constants import FONT_SIZE
from animation import AnimationController, Animation
from constants import ORIGIN, PIXELS_PER_TILE
from utils import *


class Scene:
    def __init__(self):
        self.location: Point2D = Point2D(0, 0)
        self.layer = 0
        self.exit_code = -1
        self._children: [Scene] = []
        self.parent: Scene | None = None

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
        for child in sorted(self._children, key=lambda i: i.location.y):
            child.draw(surface, time_increment)

    def update(self):
        for child in self._children:
            child.update()

    def handle(self, event: pygame.event.Event):
        for child in self._children:
            child.handle(event)

    def get_child_by_type(self, t: str):
        """
        Gets the first child where the child's type matches the given string
        """
        for child in self._children:
            if child.__class__.__name__ == t:
                return child
        return None


class TitleScreen(Scene):
    START_GAME = 1
    EXIT = 2

    def __init__(self, title, font, window_size):
        super().__init__()

        self.add(TextSprite(title, font, anchor='midbottom', pos=(window_size[0] / 2, window_size[1] / 2)))
        pygame.mouse.set_visible(True)

    def draw(self, surface: pygame.surface.Surface, time_increment: int):
        surface.fill('skyblue')
        super().draw(surface, time_increment)

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit_code = self.EXIT
            elif event.key == pygame.K_RETURN:
                self.get_child_by_type('TextSprite').set_color('white')
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                self.exit_code = self.START_GAME
        elif event.type == pygame.MOUSEMOTION:
            child = self.get_child_by_type('TextSprite')
            if child.rect.collidepoint(event.pos):
                child.set_color('white')
            else:
                child.set_color('black')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            child = self.get_child_by_type('TextSprite')
            if child.rect.collidepoint(event.pos):
                self.exit_code = self.START_GAME


class Level(Scene):
    LOST = 1
    WON = 2

    def __init__(self, level: int = 1, score: int = 0):
        super().__init__()

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
        for i in range(round(math.log(level + 1, 2))):
            location = Point2D(random.randrange(8), random.randrange(8))

            while location in [e.location for e in self._children]:
                location = Point2D(random.randrange(8), random.randrange(8))
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

    @staticmethod
    def in_bounds(point):
        return Point2D(0, 0) <= point <= Point2D(7, 7)

    def entity_at(self, point) -> Entity | None:
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
        super().draw(surface, time_increment)
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


class TextSprite(Scene):
    def __init__(self, text='', font=None, color='black', anchor='center', pos=ORIGIN):
        super().__init__()

        self.__font = font
        self.__text = text
        self.__color = color
        self.__anchor = anchor
        self.image = self.__font.render(self.__text, False, self.__color)
        self.rect = self.image.get_rect(**{anchor: pos})

    def draw(self, surface, time_increment):
        surface.blit(self.image, self.rect)

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


class Entity(Scene):
    def __init__(self, image_path: str):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.shadow = pygame.image.load('../resources/img/sprites/1x1-shadow.png').convert_alpha()
        self.multiplier = 1
        self.move_dir = Direction.ZERO

    def draw(self, surface: pygame.Surface, time_increment: int):
        if abs(self.move_dir) < Direction.EPSILON:
            self.move_dir = Direction.ZERO
            self.location = self.location.__round__()
        move_increment = self.move_dir * (time_increment / 1000 * 20)
        self.move_dir -= move_increment
        surface.blit(self.shadow, self.shadow.get_rect(center=tuple(self.apparent_location())))
        surface.blit(self.image, self.image.get_rect(midbottom=tuple(self.apparent_location())))

    def apparent_location(self) -> Point2D:
        return (self.location + self.move_dir + Point2D(0.5, 0.5)) * PIXELS_PER_TILE

    def move(self, direction: Point2D):
        raise NotImplementedError

    def handle(self, event: pygame.event.Event):
        return

    def update(self):
        return

    def take_damage(self, amount: int):
        raise NotImplementedError

    def moving(self):
        return self.move_dir != Direction.ZERO


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

    def move(self, direction: Point2D):
        if self.moving():
            return

        target = self.location + direction

        if not self.parent.in_bounds(target):
            return

        if entity := self.parent.entity_at(target):
            entity.take_damage(self.multiplier)
        else:
            self.anim.play('walk_down')
            self.move_dir = self.location - target
            self.location = target

        self.turn = False

    def take_damage(self, amount: int):
        self.multiplier -= amount

    def draw(self, surface: pygame.Surface, time_increment: int):
        self.image = self.anim.frame_advance(time_increment)
        super().draw(surface, time_increment)


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

        if (type(self.parent) == Level) and (entity := self.parent.entity_at(path[0])):
            if type(entity) == Player and random.random() < 0.1:
                entity.take_damage(self.damage)
        else:
            self.move_dir = self.location - path[0]
            self.location = path[0]

    @staticmethod
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from.keys():
            current = came_from[current]
            total_path.insert(0, current)
        return total_path[2:]

    def a_star(self, goal: Point2D) -> [Point2D]:
        # possible nodes = [Point(i, j) for i in range(8) for j in range(8)]
        open_set = [self.location]

        came_from = dict.fromkeys([Point2D(i, j) for i in range(8) for j in range(8)], None)

        g_score = dict.fromkeys([Point2D(i, j) for i in range(8) for j in range(8)], float('inf'))
        g_score[self.location] = 0

        f_score = dict.fromkeys([Point2D(i, j) for i in range(8) for j in range(8)], float('inf'))
        f_score[self.location] = self.location.dist(goal)

        while len(open_set) > 0:
            current = min(open_set, key=lambda x: f_score[x])
            if current == goal:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            for neighbor in current.neighbors():
                if neighbor not in g_score.keys() \
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
