from src.font_rendering.font_shader import FontShader
from OpenGL.GL import *


class FontRenderer:
    """Responsible for rendering text using OpenGL and a shader."""

    def __init__(self):
        """Initializes the FontRenderer and its shader."""
        self.__shader = FontShader()

    def render(self, texts: dict) -> None:
        """Renders the provided texts using the connected fonts.

        :param texts: A dictionary where keys are font instances and values are lists of GUIText instances to render.
        """
        self.prepare()
        for font in texts.keys():
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, font.get_texture_atlas())
            for text in texts.get(font):
                self.render_text(text)
        self.end_rendering()

    def clean_up(self) -> None:
        """Cleans up the shader resources used by the FontRenderer."""
        self.__shader.clean_up()

    def prepare(self) -> None:
        """Prepares the OpenGL state for rendering text."""
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)
        self.__shader.start()

    def render_text(self, text) -> None:
        """Renders a single text object.

        :param text: The GUIText instance to be rendered.
        """
        glBindVertexArray(text.get_mesh())
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        self.__shader.load_color(text.get_color())
        self.__shader.load_translation(text.get_position())
        self.__shader.load_width(text.get_width())
        self.__shader.load_edge(text.get_edge())
        self.__shader.load_border_width(text.get_border_width())
        self.__shader.load_border_edge(text.get_border_edge())
        self.__shader.load_offset(text.get_offset())
        self.__shader.load_outline_color(text.get_outline_color())
        glDrawArrays(GL_TRIANGLES, 0, text.get_vertex_count())
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindVertexArray(0)

    def end_rendering(self) -> None:
        """Ends the rendering process and resets the OpenGL state."""
        self.__shader.stop()
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
