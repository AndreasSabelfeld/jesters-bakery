from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.post_processing.contrast_shader import ContrastShader


class ContrastChanger:

    def __init__(self):
        self.__renderer = ImageRenderer()
        self.__shader = ContrastShader()

    def render(self, texture: int) -> None:
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def clean_up(self) -> None:
        self.__renderer.clean_up()
        self.__shader.clean_up()
