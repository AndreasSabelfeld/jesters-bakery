from OpenGL.GL import *
from src.toolbox.maths import Maths


class EntityRenderer:

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
            for entity in batch:
                self.prepare_instance(entity)
                glDrawElements(GL_TRIANGLES, model.get_raw_model().get_vertex_count(), GL_UNSIGNED_INT, None)
            self.unbind_textured_model()

    def prepare_textured_model(self, model):
        raw_model = model.get_raw_model()
        glBindVertexArray(raw_model.get_vao_id())  # bind the desired VAO to be able to use it
        glEnableVertexAttribArray(0)  # we have put the indices in the 0th address
        glEnableVertexAttribArray(1)  # we have put the textures in the 1st address
        glEnableVertexAttribArray(2)  # we have put the normals in the 2nd address
        texture = model.get_texture()
        self.__shader.load_number_of_rows(texture.get_number_of_rows())
        if texture.is_has_transparency():
            self.disable_culling()
        self.__shader.load_fake_lighting(texture.is_use_fake_lighting())
        self.__shader.load_shine_variables(texture.get_shine_damper(), texture.get_reflectivity())
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, model.get_texture().get_id())
        self.__shader.load_use_specular_map(texture.is_has_specular_map())
        if texture.is_has_specular_map():
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, texture.get_specular_map())

    def unbind_textured_model(self):
        self.enable_culling()
        glDisableVertexAttribArray(0)  # disable the attributeList after using it
        glDisableVertexAttribArray(1)  # disable the attributeList after using it
        glDisableVertexAttribArray(2)  # disable the attributeList after using it
        glBindVertexArray(0)  # unbind the VAO

    def prepare_instance(self, entity):
        transformation_matrix = Maths.create_transformation_matrix(entity.get_position(), entity.get_rot_x(),
                                                                   entity.get_rot_y(), entity.get_rot_z(),
                                                                   entity.get_scale())
        self.__shader.load_transformation_matrix(transformation_matrix)
        self.__shader.load_offset(entity.get_texture_x_offset(), entity.get_texture_y_offset())

    @staticmethod
    def enable_culling():
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    @staticmethod
    def disable_culling():
        glDisable(GL_CULL_FACE)
        glCullFace(GL_BACK)
