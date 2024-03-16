from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.bloom.bright_filter_shader import BrightFilterShader


class BrightFilter:

    def __init__(self, width: int, height: int):
        self.__shader = BrightFilterShader()
        self.__renderer = ImageRenderer(width, height)

    def render(self, texture: int) -> None:
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def get_output_texture(self) -> int:
        return self.__renderer.get_output_texture()

    def clean_up(self):
        self.__renderer.clean_up()
        self.__shader.clean_up()
