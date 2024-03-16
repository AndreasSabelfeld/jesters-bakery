import math

from src.particles.particle_shader import ParticleShader
from src.toolbox.maths import Maths
from src.pycgtypes import mat4, vec3

from OpenGL.GL import *


class ParticleRenderer:

    __VERTICES = [-0.5, 0.5, -0.5, -0.5, 0.5, 0.5, 0.5, -0.5]
    __MAX_INSTANCES = 10000
    __INSTANCE_DATA_LENGTH = 21

    def __init__(self, loader, projection_matrix: list[list]):
        self.__loader = loader
        self.__vbo = self.__loader.create_empty_vbo(self.__INSTANCE_DATA_LENGTH * self.__MAX_INSTANCES)
        self.__quad = loader.load_gui_to_vao(self.__VERTICES, 2)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 1, 4, self.__INSTANCE_DATA_LENGTH, 0)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 2, 4, self.__INSTANCE_DATA_LENGTH, 4)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 3, 4, self.__INSTANCE_DATA_LENGTH, 8)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 4, 4, self.__INSTANCE_DATA_LENGTH, 12)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 5, 4, self.__INSTANCE_DATA_LENGTH, 16)
        self.__loader.add_instanced_attribute(self.__quad.get_vao_id(), self.__vbo, 6, 1, self.__INSTANCE_DATA_LENGTH, 20)
        self.__shader = ParticleShader()
        self.__shader.start()
        self.__shader.load_projection_matrix(projection_matrix)
        self.__shader.stop()
        self.__pointer = 0

    def render(self, particles: dict, camera) -> None:
        view_matrix = Maths.create_view_matrix(camera)
        self.prepare()
        for texture in particles.keys():
            self.bind_texture(texture)
            particle_list = particles.get(texture)
            self.__pointer = 0
            vbo_data = [0] * len(particle_list) * self.__INSTANCE_DATA_LENGTH
            for particle in particle_list:
                self.update_model_view_matrix(particle.get_position(), particle.get_rotation(),
                                              particle.get_scale(), view_matrix, vbo_data)
                self.update_tex_coord_info(particle, vbo_data)
            self.__loader.update_vbo(self.__vbo, vbo_data)
            glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, self.__quad.get_vertex_count(), len(particle_list))
        self.finish_rendering()

    def clean_up(self) -> None:
        self.__shader.clean_up()

    def update_tex_coord_info(self, particle, data: list[float]):
        data[self.__pointer] = particle.get_tex_offset_1()[0]
        self.__pointer += 1
        data[self.__pointer] = particle.get_tex_offset_1()[1]
        self.__pointer += 1
        data[self.__pointer] = particle.get_tex_offset_2()[0]
        self.__pointer += 1
        data[self.__pointer] = particle.get_tex_offset_2()[1]
        self.__pointer += 1
        data[self.__pointer] = particle.get_blend()
        self.__pointer += 1

    def bind_texture(self, texture):
        if texture.is_additive():
            glBlendFunc(GL_SRC_ALPHA, GL_ONE)  # Additive Blending
        else:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture.get_texture_id())
        self.__shader.load_number_of_rows(texture.get_number_of_rows())

    def update_model_view_matrix(self, position: list[float], rotation: float, scale: float,
                                 view_matrix: list[list], vbo_data: list[float]) -> None:
        model_matrix = mat4()
        model_matrix = model_matrix.translation(vec3(position))

        view_matrix = mat4(*view_matrix)

        model_matrix[(0, 0)] = view_matrix[(0, 0)]
        model_matrix[(0, 1)] = view_matrix[(1, 0)]
        model_matrix[(0, 2)] = view_matrix[(2, 0)]
        model_matrix[(1, 0)] = view_matrix[(0, 1)]
        model_matrix[(1, 1)] = view_matrix[(1, 1)]
        model_matrix[(1, 2)] = view_matrix[(2, 1)]
        model_matrix[(2, 0)] = view_matrix[(0, 2)]
        model_matrix[(2, 1)] = view_matrix[(1, 2)]
        model_matrix[(2, 2)] = view_matrix[(2, 2)]

        model_matrix = model_matrix.rotate(math.radians(rotation), vec3(0, 0, 1))
        model_matrix = model_matrix.scale(vec3(scale, scale, scale))

        model_view_matrix = view_matrix * model_matrix
        self.store_matrix_data(model_view_matrix, vbo_data)

    def store_matrix_data(self, matrix: mat4, vbo_data: list[float]):
        for i in range(4):
            for j in range(4):
                vbo_data[self.__pointer] = matrix[(j, i)]
                self.__pointer += 1

    def prepare(self) -> None:
        self.__shader.start()
        glBindVertexArray(self.__quad.get_vao_id())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        glEnableVertexAttribArray(3)
        glEnableVertexAttribArray(4)
        glEnableVertexAttribArray(5)
        glEnableVertexAttribArray(6)
        glEnable(GL_BLEND)
        glDepthMask(False)

    def finish_rendering(self) -> None:
        glDepthMask(True)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glDisableVertexAttribArray(3)
        glDisableVertexAttribArray(4)
        glDisableVertexAttribArray(5)
        glDisableVertexAttribArray(6)
        glBindVertexArray(0)
        self.__shader.stop()
