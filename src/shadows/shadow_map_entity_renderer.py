from OpenGL.GL import *

from src.pycgtypes import mat4
from src.toolbox.maths import Maths
import src.render_engine.master_renderer as master_renderer


class ShadowMapEntityRenderer:

    def __init__(self, shader):
        """
        :param shader:the simple shader program being used for the shadow render pass.
        :param projection_view_matrix: the orthographic projection matrix multiplied by the light's "view" matrix.
        """
        self.__shader = shader

    def render(self, entities: dict) -> None:
        """
        Renders entieis to the shadow map. Each model is first bound and then all
        the entities using that model are rendered to the shadow map.
        :param entities: the entities to be rendered to the shadow map.
        :return:
        """
        for model in entities.keys():
            raw_model = model.get_raw_model()
            self.bind_model(raw_model)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, model.get_texture().get_id())
            if model.get_texture().is_has_transparency():
                master_renderer.MasterRenderer.disable_culling()
            for entity in entities.get(model):
                self.prepare_instance(entity)
                glDrawElements(GL_TRIANGLES, raw_model.get_vertex_count(), GL_UNSIGNED_INT, None)
            if model.get_texture().is_has_transparency():
                master_renderer.MasterRenderer.enable_culling()
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindVertexArray(0)

    @staticmethod
    def bind_model(raw_model) -> None:
        """
        Binds a raw model before rendering. Only the attribute 0 is enabled here
        because that is where the positions are stored in the VAO, and only the
        positions are required in the vertex shader.
        :param raw_model: the model to be bound.
        :return:
        """
        glBindVertexArray(raw_model.get_vao_id())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

    def prepare_instance(self, entity) -> None:
        """
        Prepares an entity to be rendered. The model matrix is created in the
        usual way and then multiplied with the projection and view matrix (often
        in the past we've done this in the vertex shader) to create the
        mvp-matrix. This is then loaded to the vertex shader as a uniform.
        :param entity: the entity to be prepared for rendering.
        :return:
        """
        model_matrix = mat4(*Maths.create_transformation_matrix(entity.get_position(), entity.get_rot_x(),
                                                               entity.get_rot_y(), entity.get_rot_z(), entity.get_scale()))
        self.__shader.load_model_matrix(model_matrix.toList())
