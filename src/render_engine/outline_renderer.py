from OpenGL.GL import *
from src.toolbox.maths import Maths


class OutlineRenderer:

    def __init__(self, shader, projection_matrix):
        self.__shader = shader
        self.__shader.start()
        self.__shader.connect_texture_units()
        self.__shader.load_projection_matrix(projection_matrix)
        self.__shader.stop()

    def render(self, entities: dict):
        for model in list(entities.keys()):
            self.prepare_textured_model(model)
            batch = entities.get(model)
            for _ in batch:
                glDrawElements(GL_TRIANGLES, model.get_raw_model().get_vertex_count(), GL_UNSIGNED_INT, None)
            self.unbind_textured_model()

    def prepare_textured_model(self, model):
        raw_model = model.get_raw_model()
        glBindVertexArray(raw_model.get_vao_id())  # bind the desired VAO to be able to use it
        glEnableVertexAttribArray(0)  # we have put the indices in the 0th address
        glEnableVertexAttribArray(1)  # we have put the textures in the 1st address
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.get_texture().get_id())

    def unbind_textured_model(self):
        glDisableVertexAttribArray(0)  # disable the attributeList after using it
        glDisableVertexAttribArray(1)  # disable the attributeList after using it
        glBindVertexArray(0)  # unbind the VAO
