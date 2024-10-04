from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.bloom.bright_filter_shader import BrightFilterShader


class BrightFilter:
    """
    Applies a bright filter to a texture, used for post-processing effects such as bloom.
    """

    def __init__(self, width: int, height: int):
        """
        Initializes the BrightFilter by setting up the shader and renderer.

        :param width: The width of the texture to render to.
        :param height: The height of the texture to render to.
        """
        self.__shader = BrightFilterShader()
        self.__renderer = ImageRenderer(width, height)

    def render(self, texture: int) -> None:
        """
        Renders the bright filter effect onto the given texture.

        :param texture: The ID of the texture to apply the bright filter to.
        """
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def get_output_texture(self) -> int:
        """
        Returns the output texture after rendering the bright filter.

        :return: The ID of the output texture.
        """
        return self.__renderer.get_output_texture()

    def clean_up(self) -> None:
        """
        Cleans up resources used by the renderer and shader.
        """
        self.__renderer.clean_up()
        self.__shader.clean_up()
