from src.pycgtypes import vec3
from src.collision.utility import dot
from functools import lru_cache


class Plane:
    def __init__(self, origin: vec3, normal: vec3):
        self.normal = normal
        self.origin = origin
        self.equation = [0.0] * 4
        self.equation[0] = normal.x
        self.equation[1] = normal.y
        self.equation[2] = normal.z
        self.equation[3] = -(normal.x * origin.x + normal.y * origin.y + normal.z * origin.z)

    @classmethod
    def from_triangle(cls, p1: vec3, p2: vec3, p3: vec3):
        normal = (p2 - p1).cross(p3 - p1)
        normal = normal.normalize()
        return cls(p1, normal)

    def is_front_facing_to(self, direction: list[float]):
        product = dot(self.normal, direction)
        return product <= 0

    def signed_distance_to(self, point: list[float]):
        return dot(point, self.normal) + self.equation[3]
