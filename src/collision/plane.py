from src.pycgtypes import vec3
from src.collision.utility import dot
from functools import lru_cache


class Plane:
    """
    Represents a plane in 3D space, defined by an origin point and a normal vector.
    The plane can be constructed from three points forming a triangle or from a normal vector and an origin point.

    Attributes:
        normal (vec3): The normal vector to the plane.
        origin (vec3): A point on the plane.
        equation (list[float]): The coefficients of the plane equation in the form [A, B, C, D] for Ax + By + Cz + D = 0.
    """

    def __init__(self, origin: vec3, normal: vec3):
        """
        Initializes the plane with a point (origin) and a normal vector.

        :param origin: A point on the plane.
        :param normal: The normal vector to the plane.
        """
        self.normal = normal
        self.origin = origin
        self.equation = [0.0] * 4
        self.equation[0] = normal.x
        self.equation[1] = normal.y
        self.equation[2] = normal.z
        self.equation[3] = -(normal.x * origin.x + normal.y * origin.y + normal.z * origin.z)

    @classmethod
    def from_triangle(cls, p1: vec3, p2: vec3, p3: vec3):
        """
        Creates a plane from three points that form a triangle by computing the normal vector
        from the cross product of two edges of the triangle.

        :param p1: The first point of the triangle.
        :param p2: The second point of the triangle.
        :param p3: The third point of the triangle.
        :return: A Plane instance of the plane formed by the triangle.
        """
        normal = (p2 - p1).cross(p3 - p1)
        try:
            normal = normal.normalize()
        except ZeroDivisionError:
            # I don't know what exactly in a 3D model causes the normal to be non-existent...
            # probably a faulty 3D model with vertices at the exact same position.
            pass
        return cls(p1, normal)

    def is_front_facing_to(self, direction: list[float]) -> bool:
        """
        Determines if the plane is front-facing to a given direction vector.

        :param direction: A vector of the direction to check.
        :return: True if the plane is front-facing to the direction, False otherwise.
        """
        product = dot(self.normal, direction)
        return product <= 0

    def signed_distance_to(self, point: list[float]) -> float:
        """
        Calculates the signed distance from a point to the plane. The distance is positive if the point is on the
        side of the plane pointed to by the normal vector, and negative if on the opposite side.

        :param point: The point to calculate the distance from.
        :return: The signed distance from the point to the plane.
        """
        return dot(point, self.normal) + self.equation[3]
