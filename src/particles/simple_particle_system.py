from src.render_engine.time import Time
from src.pycgtypes.vec3 import vec3
from src.particles.particle import Particle

import math
from random import random


class SimpleParticleSystem:

    def __init__(self, texture, pps: float, speed: float, gravity_complient: float, life_length: float):
        self.__texture = texture
        self.__pps = pps
        self.__speed = speed
        self.__gravity_complient = gravity_complient
        self.__life_length = life_length

    def generate_particles(self, system_center: list[float]) -> None:
        delta = Time.get_delta_time()
        particles_to_create = self.__pps * delta
        count = math.floor(particles_to_create)
        partial_particle = particles_to_create % 1
        for i in range(count):
            self.emit_particle(system_center)
        if random() < partial_particle:
            self.emit_particle(system_center)

    def emit_particle(self, center: list[float]) -> None:
        dir_x = random() * 2.0 - 1.0
        dir_z = random() * 2.0 - 1.0
        velocity = vec3(dir_x, 1, dir_z)
        velocity = velocity.normalize()
        velocity *= self.__speed
        Particle(self.__texture, center, list(velocity), self.__gravity_complient, self.__life_length, 0, 1)
