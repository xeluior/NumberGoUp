import math

from constants import SUBPIXEL


def sign(i):
    return i / abs(i) if i != 0 else 0


class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other: int | float | complex):
        if type(other) not in (int, float, complex):
            raise TypeError

        return Point2D(self.x * other, self.y * other)

    def __add__(self, other):
        if type(other) != Point2D:
            raise TypeError

        return Point2D(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -other

    def __abs__(self):
        return Point2D(abs(self.x), abs(self.y))

    def __eq__(self, other) -> bool:
        if type(other) != Point2D:
            return False

        return self.x == other.x and self.y == other.y

    def __le__(self, other) -> bool:
        if type(other) != Point2D:
            raise TypeError

        return self.x <= other.x and self.y <= other.y

    def __lt__(self, other) -> bool:
        if type(other) != Point2D:
            raise TypeError

        return self <= other and self != other

    def __ge__(self, other) -> bool:
        if type(other) != Point2D:
            raise TypeError

        return self.x >= other.x and self.y >= other.y

    def __gt__(self, other) -> bool:
        if type(other) != Point2D:
            raise TypeError

        return self >= other and self != other

    def __iter__(self):
        yield self.x
        yield self.y

    def __round__(self: 'Point2D', ndigits: int = 0) -> 'Point2D':
        return Point2D(round(self.x, ndigits), round(self.y, ndigits))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash(str(self))

    def dist(self, other: 'Point2D') -> float:
        if type(other) != Point2D:
            raise TypeError
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)

    def neighbors(self) -> ['Point2D']:
        return [
            self + Direction.UP,
            self + Direction.RIGHT,
            self + Direction.DOWN,
            self + Direction.LEFT
        ]


class Direction:
    ZERO = Point2D(0, 0)
    EPSILON = Point2D(SUBPIXEL, SUBPIXEL)
    UP = Point2D(0, -1)
    DOWN = Point2D(0, 1)
    LEFT = Point2D(-1, 0)
    RIGHT = Point2D(1, 0)
