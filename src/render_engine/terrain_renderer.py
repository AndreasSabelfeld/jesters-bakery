from OpenGL.GL import *
from src.toolbox.maths import Maths


class TerrainRenderer:

    def __init__(self, shader, projection_matrix):
        self.__shader = shader
        self.__shader.start()
        self.__projection_matrix = shader.load_projection_matrix(projection_matrix)
        self.__shader.connect_texture_units()
        self.__shader.stop()

    def render(self, terrains: list):
        for terrain in terrains:
            self.prepare_terrain(terrain)
            self.load_model_matrix(terrain)
            glDrawElements(GL_TRIANGLES, terrain.get_model().get_vertex_count(), GL_UNSIGNED_INT, None)
            self.unbind_texture_model()

    def prepare_terrain(self, terrain):
        raw_model = terrain.get_model()
        glBindVertexArray(raw_model.get_vao_id())  # bind the desired VAO to be able to use it
        glEnableVertexAttribArray(0)  # we have put the indices in the 0th address
        glEnableVertexAttribArray(1)  # we have put the textures in the 1st address
        glEnableVertexAttribArray(2)  # we have put the normals in the 2nd address
        self.bind_textures(terrain)
        self.__shader.load_shine_variables(1, 0)

    @staticmethod
    def bind_textures(terrain):
        texture_pack = terrain.get_texture_pack()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_pack.get_background_texture().get_texture_id())
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texture_pack.get_r_texture().get_texture_id())
        glActiveTexture(GL_TEXTURE2)
        glBindTexture(GL_TEXTURE_2D, texture_pack.get_g_texture().get_texture_id())
        glActiveTexture(GL_TEXTURE3)
        glBindTexture(GL_TEXTURE_2D, texture_pack.get_b_texture().get_texture_id())
        glActiveTexture(GL_TEXTURE4)
        glBindTexture(GL_TEXTURE_2D, terrain.get_blend_map().get_texture_id())

    @staticmethod
    def unbind_texture_model():
        glDisableVertexAttribArray(0)  # disable the attributeList after using it
        glDisableVertexAttribArray(1)  # disable the attributeList after using it
        glDisableVertexAttribArray(2)  # disable the attributeList after using it
        glBindVertexArray(0)  # unbind the VAO

    def load_model_matrix(self, terrain):
        transformation_matrix = Maths.create_transformation_matrix([terrain.get_x(), 0, terrain.get_z()], 0, 0, 0, 1)
        self.__shader.load_transformation_matrix(transformation_matrix)
