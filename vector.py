import math

class Vector:
    x: float
    y: float
    z: float

    def default():
        return Vector(0, 0, 0)

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __mul__(self, other: float):
        return Vector(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __rmul__(self, other: float):
        return Vector(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __truediv__(self, other: float):
        return Vector(
            self.x / other,
            self.y / other,
            self.z / other
        )

    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def length(self):
        return math.sqrt(self.length_squared())

    def cross_product(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        length = self.length()
        return Vector(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def distance_to(self, other):
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )