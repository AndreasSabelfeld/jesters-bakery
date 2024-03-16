from OpenGL.GL import *

from src.render_engine.display_manager import DisplayManager


class ShadowFrameBuffer:
    """
    The frame buffer for the shadow pass. This class sets up the depth texture
    which can be rendered to during the shadow render pass, producing a shadow
    map.
    """

    def __init__(self, width: int, height: int):
        """
        Initialises the frame buffer and shadow map of a certain size.
        :param width: the width of the shadow map in pixels.
        :param height: the height of the shadow map in pixels.
        """
        self.__WIDTH = width
        self.__HEIGHT = height
        self.__fbo = None
        self.__shadow_map = None
        self.initialise_frame_buffer()

    def clean_up(self) -> None:
        """
        Deletes the frame buffer and shadow map texture when the game closes.
        """
        glDeleteFramebuffers(1, [self.__fbo])
        glDeleteTextures(1, [self.__shadow_map])

    def bind_frame_buffer(self) -> None:
        self.__bind_frame_buffer(self.__fbo, self.__WIDTH, self.__HEIGHT)

    @staticmethod
    def unbind_frame_buffer() -> None:
        """
        Unbinds the frame buffer, setting the default frame buffer as the current render target.
        """
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, DisplayManager.get_width(), DisplayManager.get_height())

    def get_shadow_map(self) -> int:
        """
        :return: The ID of the shadow map texture.
        """
        return self.__shadow_map

    def initialise_frame_buffer(self) -> None:
        """
        Creates the frame buffer and adds its depth attachment texture.
        :return:
        """
        self.__fbo = self.__create_frame_buffer()
        self.__shadow_map = self.__create_depth_buffer_attachment(self.__WIDTH, self.__HEIGHT)
        self.unbind_frame_buffer()

    @staticmethod
    def __bind_frame_buffer(frame_buffer: int, width: int, height: int) -> None:
        """
        Binds the frame buffer as the current render target.
        :param frame_buffer: the frame buffer.
        :param width: the width of the frame buffer.
        :param height: the height of the frame buffer.
        :return:
        """
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, frame_buffer)
        glViewport(0, 0, width, height)

    @staticmethod
    def __create_frame_buffer() -> int:
        """
        Creates a frame buffer and binds it so that attachments can be added to
        it. The draw buffer is set to none, indicating that there's no colour
        buffer to be rendered to.
        :return: The newly created frame buffer's ID.
        """
        frame_buffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        return frame_buffer

    @staticmethod
    def __create_depth_buffer_attachment(width: int, height: int) -> int:
        """
        Creates a depth buffer texture attachment.
        :param width: the width of the texture.
        :param height: the height of the texture.
        :return: The ID of the depth texture.
        """
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT16, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT,
                     ctypes.c_void_p(0))
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, texture, 0)
        return texture
