from src.render_engine.time import Time
from src.pycgtypes import vec3, vec4, mat4
from src.particles.particle import Particle

import math
from random import random


class ComplexParticleSystem:

    def __init__(self, texture, pps: float, speed: float, gravity_complient: float, life_length: float, scale: float):
        self.__texture = texture
        self.__pps = pps
        self.__average_speed = speed
        self.__gravity_complient = gravity_complient
        self.__average_life_length = life_length
        self.__average_scale = scale

        self.__speed_error = self.__life_error = self.__scale_error = 0
        self.__random_rotation = False
        self.__direction = None
        self.__direction_deviation = 0

    def set_direction(self, direction: list[float], deviation: float) -> None:
        self.__direction = direction
        self.__direction_deviation = deviation

    def randomize_rotation(self) -> None:
        self.__random_rotation = True

    def set_speed_error(self, error: float) -> None:
        self.__speed_error = error * self.__average_speed

    def set_life_error(self, error: float) -> None:
        self.__life_error = error * self.__average_life_length

    def set_scale_error(self, error: float) -> None:
        self.__scale_error = error * self.__average_scale

    def generate_particles(self, system_center: list[float]) -> None:
        delta = Time.get_delta_time()
        particles_to_create = self.__pps * delta
        count = math.floor(particles_to_create)
        partial_particle = particles_to_create % 1
        for i in range(count):
            self.emit_particle(system_center)
        if random() < partial_particle:
            self.emit_particle(system_center)

    def emit_particle(self, center: list[float]):
        if self.__direction is not None:
            velocity = self.generate_random_unit_vector_within_cone(self.__direction, self.__direction_deviation)
        else:
            velocity = self.generate_random_unit_vector()
        velocity = velocity.normalize()
        velocity *= self.generate_value(self.__average_speed, self.__speed_error)
        scale = self.generate_value(self.__average_scale, self.__scale_error)
        life_length = self.generate_value(self.__average_life_length, self.__life_error)
        Particle(self.__texture, center, list(velocity), self.__gravity_complient, life_length, self.generate_rotation(), scale)

    @staticmethod
    def generate_value(average: float, error_margin: float) -> float:
        offset = (random() - 0.5) * 2.0 * error_margin
        return average + offset

    def generate_rotation(self) -> float:
        if self.__random_rotation:
            return random() * 360.0
        else:
            return 0

    @staticmethod
    def generate_random_unit_vector_within_cone(cone_direction: list[float], angle: float) -> vec4:
        cos_angle = math.cos(angle)
        theta = random() * 2.0 * math.pi
        z = cos_angle + (random() * (1 - cos_angle))
        root_one_minus_z_squared = math.sqrt(1 - z * z)
        x = root_one_minus_z_squared * math.cos(theta)
        y = root_one_minus_z_squared * math.sin(theta)

        direction = vec4(x, y, z, 1)
        if cone_direction[0] != 0 or cone_direction[1] != 0 or (cone_direction[2] != 1 and cone_direction[2] != -1):
            rotate_axis = vec3.cross(vec3(cone_direction), vec3(0, 0, 1))
            rotate_axis = rotate_axis.normalize()
            rotate_angle = math.acos(vec3(cone_direction) * vec3(0, 0, 1))
            rotation_matrix = mat4()
            rotation_matrix = rotation_matrix.rotation(-rotate_angle, rotate_axis)
            direction = rotation_matrix * direction
        elif cone_direction[2] == -1:
            direction.z *= -1
        return direction

    @staticmethod
    def generate_random_unit_vector() -> vec3:
        theta = random() * 2.0 * math.pi
        z = random() * 2.0 - 1
        root_one_minus_z_squared = math.sqrt(1 - z * z)
        x = root_one_minus_z_squared * math.cos(theta)
        y = root_one_minus_z_squared * math.sin(theta)
        return vec3(x, y, z)
