import math
from math import floor

from src.constants import SUBPIXEL


def sign(i):
    return i / abs(i) if i != 0 else 0


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if type(other) not in (int, float, complex):
            raise TypeError

        return Point(self.x * other, self.y * other)

    def __add__(self, other):
        if type(other) != Point:
            raise TypeError

        return Point(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -other

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __eq__(self, other):
        if type(other) != Point:
            return False

        return self.x == other.x and self.y == other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __lt__(self, other):
        return self <= other and self != other

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __gt__(self, other):
        return self >= other and self != other

    def __iter__(self):
        yield self.x
        yield self.y

    def __round__(self, n=None):
        return Point(round(self.x), round(self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash(str(self))

    def dist(self, other):
        if type(other) != Point:
            raise TypeError
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)

    def neighbors(self):
        return [
            self + Direction.UP,
            self + Direction.RIGHT,
            self + Direction.DOWN,
            self + Direction.LEFT
        ]


class Direction:
    ZERO = Point(0, 0)
    EPSILON = Point(SUBPIXEL, SUBPIXEL)
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
