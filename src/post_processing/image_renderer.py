from src.post_processing.fbo import FBO
from OpenGL.GL import *


class ImageRenderer:

    def __init__(self, width: int = None, height: int = None):
        self.__fbo = None
        if width is not None and height is not None:
            self.__fbo = FBO(width, height, False, FBO.NONE)

    def render_quad(self) -> None:
        if self.__fbo is not None:
            self.__fbo.bind_frame_buffer()
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        if self.__fbo is not None:
            self.__fbo.unbind_frame_buffer()

    def get_output_texture(self) -> int:
        return self.__fbo.get_color_texture()

    def clean_up(self):
        if self.__fbo is not None:
            self.__fbo.clean_up()
            