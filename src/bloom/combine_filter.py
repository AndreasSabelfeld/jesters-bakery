from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.bloom.combine_shader import CombineShader


class CombineFilter:
    """
    Combines two textures using a shader for post-processing effects like bloom.
    """

    def __init__(self):
        """
        Initializes the CombineFilter by setting up the CombineShader.
        """
        self.__shader = CombineShader()
        self.__shader.start()
        self.__shader.connect_texture_units()
        self.__shader.stop()
        self.__renderer = ImageRenderer()

    def render(self, color_texture: int, highlight_texture: int) -> None:
        """
        Renders the combined output of the color and highlight textures using the CombineShader.

        :param color_texture: The ID of the color texture.
        :param highlight_texture: The ID of the highlight texture.
        """
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, color_texture)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, highlight_texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def clean_up(self) -> None:
        """
        Cleans up resources used by the renderer and shader.
        """
        self.__renderer.clean_up()
        self.__shader.clean_up()
