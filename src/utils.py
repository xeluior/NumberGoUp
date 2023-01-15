class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        if type(other) not in (int, float, complex):
            raise ValueError

        return Point(self.x * other, self.y * other)

    def __add__(self, other):
        if type(other) != Point:
            raise ValueError

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


class Direction:
    UP = Point(0, -1)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
