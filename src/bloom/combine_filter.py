from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.bloom.combine_shader import CombineShader


class CombineFilter:

    def __init__(self):
        self.__shader = CombineShader()
        self.__shader.start()
        self.__shader.connect_texture_units()
        self.__shader.stop()
        self.__renderer = ImageRenderer()

    def render(self, color_texture: int, highlight_texture: int) -> None:
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, color_texture)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, highlight_texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def clean_up(self) -> None:
        self.__renderer.clean_up()
        self.__shader.clean_up()
