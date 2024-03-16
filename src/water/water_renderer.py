from OpenGL.GL import *
from .water_tile import WaterTile
from src.toolbox.maths import Maths
from src.render_engine.time import Time


class WaterRenderer:

    __DUDV_MAP = "waterDUDV"
    __NORMAL_MAP = "normalMap"
    __WAVE_SPEED = 0.03

    def __init__(self, loader, shader, projection_matrix: list[list], fbos):
        self.__quad = None
        self.__fbos = fbos
        self.__dudv_texture = loader.load_texture(self.__DUDV_MAP)
        self.__normal_map = loader.load_texture(self.__NORMAL_MAP)
        self.__move_factor = 0
        self.__shader = shader
        self.__shader.start()
        self.__shader.connect_texture_units()
        self.__shader.load_projection_matrix(projection_matrix)
        self.__shader.stop()
        self.set_up_vao(loader)

    def render(self, water: list, camera, sun):
        self.prepare_render(camera, sun)
        for tile in water:
            model_matrix = Maths.create_transformation_matrix([tile.get_x(), tile.get_height(), tile.get_z()], 0, 0, 0, WaterTile.get_tile_size())
            self.__shader.load_model_matrix(model_matrix)
            glDrawArrays(GL_TRIANGLES, 0, self.__quad.get_vertex_count())
            self.unbind()

    def prepare_render(self, camera, sun):
        self.__shader.start()
        self.__shader.load_view_matrix(camera)
        self.__move_factor += self.__WAVE_SPEED * Time.get_delta_time()
        self.__move_factor %= 1
        self.__shader.load_move_factor(self.__move_factor)
        self.__shader.load_light(sun)
        glBindVertexArray(self.__quad.get_vao_id())
        glEnableVertexAttribArray(0)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.get_reflection_texture())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.get_refraction_texture())
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, self.__dudv_texture)
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, self.__normal_map)
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, self.__fbos.get_refraction_depth_texture())

    def unbind(self):
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def set_up_vao(self, loader):
        # Just x and z vertex positions here, y is set to 0 in v.shader
        vertices = [-1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1]
        self.__quad = loader.load_gui_to_vao(vertices, 2)
