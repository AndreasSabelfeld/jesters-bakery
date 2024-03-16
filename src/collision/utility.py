import ctypes

from src.pycgtypes import vec3, mat3
import math


def dot(v1, v2) -> float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


def check_point_in_triangle(point: vec3, pa: vec3, pb: vec3, pc: vec3) -> bool:
    e10 = pb - pa
    e20 = pc - pa
    a = dot(e10, e10)
    b = dot(e10, e20)
    c = dot(e20, e20)
    ac_bb = (a * c) - (b * b)
    vp = vec3(point.x - pa.x, point.y - pa.y, point.z - pa.z)
    d = dot(vp, e10)
    e = dot(vp, e20)
    x = (d * c) - (e * b)
    y = (e * a) - (d * b)
    z = x + y - ac_bb
    return (int(z) & ~(int(x) | int(y))) & 0x80000000 != 0


def get_lowest_root(a: float, b: float, c: float, max_r: float, root: ctypes.pointer) -> bool:
    if a == 0:
        return False
    # Check if a solution exists
    determinant = b * b - 4.0 * a * c

    # If determinant is negative, it means no solutions.
    if determinant < 0.0:
        return False
    # Calculate the two roots:
    sqrt_d = math.sqrt(determinant)
    r1 = (-b - sqrt_d) / (2 * a)
    r2 = (-b + sqrt_d) / (2 * a)
    # Sort so x1 <= x2
    if r1 > r2:
        temp = r2
        r2 = r1
        r1 = temp
    # Get the lowest root
    if 0 < r1 < max_r:
        root.contents.value = r1
        return True
    # It is possible that we want x2 - this can happen if x1 < 0
    if 0 < r2 < max_r:
        root.contents.value = r2
        return True
    # No (valid) solutions
    return False


def convert_to_ellipsoid_space(radius: vec3, vector: vec3) -> vec3:
    change_of_basis = mat3()
    change_of_basis[(0, 0)] = 1/radius.x
    change_of_basis[(1, 1)] = 1/radius.y
    change_of_basis[(2, 2)] = 1/radius.z

    return change_of_basis * vector


def convert_to_r3_space(radius: vec3, vector: vec3) -> vec3:
    change_of_basis = mat3()
    change_of_basis[(0, 0)] = 1/radius.x
    change_of_basis[(1, 1)] = 1/radius.y
    change_of_basis[(2, 2)] = 1/radius.z

    return change_of_basis.inverse() * vector
