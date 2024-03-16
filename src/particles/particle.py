import math

from src.entities.player import Player
from src.render_engine.time import Time
from src.particles.particle_master import ParticleMaster
from src.particles.particle_texture import ParticleTexture
from src.pycgtypes import vec3


class Particle:

    def __init__(self, texture: ParticleTexture, position: list[float], velocity: list[float], gravity_effect: float,
                 life_length: float, rotation: float, scale: float):
        self.__texture = texture
        self.__position = position
        self.__velocity = velocity
        self.__gravity_effect = gravity_effect
        self.__life_length = life_length
        self.__rotation = rotation
        self.__scale = scale
        ParticleMaster.add_particle(self)

        self.__tex_offset_1 = [0.0, 0.0]
        self.__tex_offset_2 = [0.0, 0.0]
        self.__blend = 0.0

        self.__elapsed_time = 0
        self.__distance = 0

    def get_distance(self) -> float:
        return self.__distance

    def get_tex_offset_1(self) -> list[float]:
        return self.__tex_offset_1

    def get_tex_offset_2(self) -> list[float]:
        return self.__tex_offset_2

    def get_blend(self) -> float:
        return self.__blend

    def get_texture(self) -> ParticleTexture:
        return self.__texture

    def get_position(self) -> list[float]:
        return self.__position

    def get_rotation(self) -> float:
        return self.__rotation

    def get_scale(self) -> float:
        return self.__scale

    def update(self, camera) -> bool:
        delta_time = Time.get_delta_time()
        self.__velocity[1] += Player.get_gravity() * self.__gravity_effect * delta_time
        change = self.__velocity
        change = [change[0] * delta_time,
                  change[1] * delta_time,
                  change[2] * delta_time]
        self.__position = [self.__position[0] + change[0],
                           self.__position[1] + change[1],
                           self.__position[2] + change[2]]
        self.__distance = (vec3(camera.get_position()) - vec3(self.__position)).length()
        self.__elapsed_time += delta_time
        self.__update_texture_coord_info()
        return self.__elapsed_time < self.__life_length

    def __update_texture_coord_info(self):
        life_factor = self.__elapsed_time / self.__life_length
        stage_count = self.__texture.get_number_of_rows() ** 2
        atlas_progression = life_factor * stage_count
        index_1 = math.floor(atlas_progression)
        index_2 = index_1 + 1 if index_1 < stage_count - 1 else index_1
        self.__blend = atlas_progression % 1
        self.__set_texture_offset(self.__tex_offset_1, index_1)
        self.__set_texture_offset(self.__tex_offset_2, index_2)

    def __set_texture_offset(self, offset: list[float], index: int):
        column = index % self.__texture.get_number_of_rows()
        row = index // self.__texture.get_number_of_rows()
        offset[0] = column / self.__texture.get_number_of_rows()
        offset[1] = row / self.__texture.get_number_of_rows()
