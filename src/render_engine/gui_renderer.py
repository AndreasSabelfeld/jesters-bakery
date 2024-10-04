from OpenGL.GL import *

from src.guis.gui_shader import GuiShader
from src.toolbox.maths import Maths


class GuiRenderer:
    """
    2D orthographic texture renderer. Rendered textures will appear in front of everything.
    """
    __positions = [-1, 1, -1, -1, 1, 1, 1, -1]
    __quad = None

    def __init__(self, loader):
        """Creates a GuiRenderer instance.

        :params loader: Loader object.
        """
        if GuiRenderer.__quad is None:
            GuiRenderer.__quad = loader.load_gui_to_vao(GuiRenderer.__positions, 2)
        self.__shader = GuiShader()

    def render(self, guis: list):
        """Renders the given GUI elements.

        :params guis: A list of GUI elements to render.
        """
        self.__shader.start()
        glBindVertexArray(self.__quad.get_vao_id())
        glEnableVertexAttribArray(0)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for gui in guis:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, gui.get_texture())
            matrix = Maths.create_2d_transformation_matrix(gui.get_position(), gui.get_scale())
            self.__shader.load_transformation(matrix)
            glDrawArrays(GL_TRIANGLE_STRIP, 0, self.__quad.get_vertex_count())
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def clean_up(self):
        """Cleans up the shader resources."""
        self.__shader.clean_up()
