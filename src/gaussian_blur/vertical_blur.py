from OpenGL.GL import *
from src.post_processing.image_renderer import ImageRenderer
from src.gaussian_blur.vertical_blur_shader import VerticalBlurShader


class VerticalBlur:

    def __init__(self, target_fbo_width: int, target_fbo_height: int):
        self.__shader = VerticalBlurShader()
        self.__shader.start()
        self.__shader.load_target_height(target_fbo_width)
        self.__shader.stop()
        self.__renderer = ImageRenderer(target_fbo_width, target_fbo_height)

    def render(self, texture: int) -> None:
        self.__shader.start()
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        self.__renderer.render_quad()
        self.__shader.stop()

    def get_output_texture(self) -> int:
        return self.__renderer.get_output_texture()

    def clean_up(self) -> None:
        self.__renderer.clean_up()
        self.__shader.clean_up()
