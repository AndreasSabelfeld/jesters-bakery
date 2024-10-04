from OpenGL.GL import *
from src.toolbox.maths import Maths


class TerrainRenderer:

    def __init__(self, shader, projection_matrix):
        """
        Initializes the TerrainRenderer with a shader and projection matrix.

        :params shader: The shader used for rendering terrain.
        :params projection_matrix: The projection matrix for the scene.
        """
        self.__shader = shader
        self.__shader.start()
        self.__projection_matrix = shader.load_projection_matrix(projection_matrix)
        self.__shader.connect_texture_units()
        self.__shader.stop()

    def render(self, terrains: list) -> None:
        """
        Renders the provided list of terrains.

        :params terrains: A list of terrain objects to be rendered.
        """
        for terrain in terrains:
            self.prepare_terrain(terrain)
            self.load_model_matrix(terrain)
            glDrawElements(GL_TRIANGLES, terrain.get_model().get_vertex_count(), GL_UNSIGNED_INT, None)
            self.unbind_texture_model()

    def prepare_terrain(self, terrain) -> None:
        """
        Prepares a terrain for rendering.

        :params terrain: The terrain object to prepare.
        """
        raw_model = terrain.get_model()
        glBindVertexArray(raw_model.get_vao_id())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        self.bind_textures(terrain)
        self.__shader.load_shine_variables(1, 0)

    @staticmethod
    def bind_textures(terrain) -> None:
        """
        Binds the textures for the given terrain.

        :params terrain: The terrain object whose textures will be bound.
        """
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
    def unbind_texture_model() -> None:
        """
        Unbinds the textures and VAO after rendering.
        """
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindVertexArray(0)

    def load_model_matrix(self, terrain) -> None:
        """
        Loads the transformation matrix for the terrain model.

        :params terrain: The terrain object for which to load the matrix.
        """
        transformation_matrix = Maths.create_transformation_matrix([terrain.get_x(), 0, terrain.get_z()], 0, 0, 0, 1)
        self.__shader.load_transformation_matrix(transformation_matrix)
