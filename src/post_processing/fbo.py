from OpenGL.GL import *
from src.render_engine.display_manager import DisplayManager


class FBO:
    NONE = 0
    DEPTH_TEXTURE = 1
    DEPTH_RENDER_BUFFER = 2

    def __init__(self, width: int, height: int, multi_target: bool = False, depth_buffer_type: int = None):
        """
        Creates an FBO of a specified width and height, with the desired type of
        depth buffer attachment.
        :param width: the width of the FBO.
        :param height: the height of the FBO.
        :param depth_buffer_type: an int indicating the type of depth buffer attachment that this FBO should use.
        (leave empty to use a multi-sampled FBO)
        """
        self.__frame_buffer = None
        self.__color_texture = None
        self.__depth_texture = None
        self.__depth_buffer = None
        self.__color_buffer0 = None
        self.__color_buffer1 = None

        self.__width = width
        self.__height = height
        self.__multisample = False
        self.__multi_target = multi_target
        if depth_buffer_type is None:
            self.__multisample = True
            self._initialize_frame_buffer(self.DEPTH_RENDER_BUFFER)
        else:
            self._initialize_frame_buffer(depth_buffer_type)

    def clean_up(self) -> None:
        """
        Deletes the frame buffer and its attachments when the game closes.
        """
        glDeleteFramebuffers(self.__frame_buffer)
        glDeleteTextures(self.__color_texture)
        glDeleteTextures(self.__depth_texture)
        glDeleteRenderbuffers(self.__depth_buffer)
        glDeleteRenderbuffers(self.__color_buffer0)
        glDeleteRenderbuffers(self.__color_buffer1)

    def bind_frame_buffer(self) -> None:
        """
        Binds the frame buffer, setting it as the current render target. Anything
        rendered after this will be rendered to this FBO, and not to the screen.
        """
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self.__frame_buffer)
        glViewport(0, 0, self.__width, self.__height)

    @staticmethod
    def unbind_frame_buffer() -> None:
        """
        Unbinds the frame buffer, setting the default frame buffer as the current
        render target. Anything rendered after this will be rendered to the
        screen, and not this FBO.
        """
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, DisplayManager.get_width(), DisplayManager.get_height())

    def bind_to_read(self) -> None:
        """
        Binds the current FBO to be read from
        """
        glBindTexture(GL_TEXTURE_2D, 0)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.__frame_buffer)
        glReadBuffer(GL_COLOR_ATTACHMENT0)

    def resolve_to_fbo(self, output_fbo, read_buffer: int) -> None:
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, output_fbo.get_frame_buffer())
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.__frame_buffer)
        glReadBuffer(read_buffer)
        glBlitFramebuffer(0, 0, self.__width, self.__height, 0, 0, output_fbo.get_width(), output_fbo.get_height(),
                          GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT, GL_NEAREST)
        self.unbind_frame_buffer()

    def resolve_to_screen(self):
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0)
        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.get_frame_buffer())
        glDrawBuffer(GL_FRONT)
        glBlitFramebuffer(0, 0, self.__width, self.__height, 0, 0, DisplayManager.get_width(), DisplayManager.get_height(),
                          GL_COLOR_BUFFER_BIT, GL_NEAREST)
        self.unbind_frame_buffer()

    def _initialize_frame_buffer(self, fbo_type: int) -> None:
        """
        Creates the FBO along with a colour buffer texture attachment, and
        possibly a depth buffer.
        :param fbo_type: the type of depth buffer attachment to be attached to the FBO.
        """
        self._create_frame_buffer()
        if self.__multisample and self.__multi_target:
            self.__color_buffer0 = self._create_multisample_color_attachment(GL_COLOR_ATTACHMENT0)
            self.__color_buffer1 = self._create_multisample_color_attachment(GL_COLOR_ATTACHMENT1)
        elif self.__multisample:
            self._create_multisample_color_attachment()
        else:
            self._create_texture_attachment()
        if fbo_type == self.DEPTH_RENDER_BUFFER:
            self._create_depth_buffer_attachment()
        elif fbo_type == self.DEPTH_TEXTURE:
            self._create_depth_texture_attachment()
        self.unbind_frame_buffer()

    def _create_frame_buffer(self) -> None:
        """
        Creates a new frame buffer object and sets the buffer to which drawing
        will occur - colour attachment 0. This is the attachment where the colour
        buffer texture is.
        """
        self.__frame_buffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.__frame_buffer)
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        self._determine_draw_buffer()

    def _determine_draw_buffer(self) -> None:
        draw_buffers = [GL_COLOR_ATTACHMENT0]
        if self.__multi_target:
            draw_buffers.append(GL_COLOR_ATTACHMENT1)
        glDrawBuffers(draw_buffers)

    def _create_texture_attachment(self) -> None:
        """
        Creates a texture and sets it as the colour buffer attachment for this FBO.
        """
        self.__color_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__color_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, self.__width, self.__height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.__color_texture, 0)

    def _create_depth_texture_attachment(self) -> None:
        """
        Adds a depth buffer to the FBO in the form of a texture, which can later be sampled.
        """
        self.__depth_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.__depth_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT24, self.__width, self.__height, 0, GL_DEPTH_COMPONENT,
                     GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.__depth_texture, 0)

    def _create_multisample_color_attachment(self, color_attachment: int = None) -> int:
        color_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, color_buffer)
        glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_RGBA8, self.__width, self.__height)
        if color_attachment is not None:
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, color_attachment, GL_RENDERBUFFER, color_buffer)
        else:
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, color_buffer)
        return color_buffer

    def _create_depth_buffer_attachment(self) -> None:
        """
        Adds a depth buffer to the FBO in the form of a render buffer. This can't
        be used for sampling in the shaders.
        """
        self.__depth_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.__depth_buffer)
        if not self.__multisample:
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, self.__width, self.__height)
        else:
            glRenderbufferStorageMultisample(GL_RENDERBUFFER, 4, GL_DEPTH_COMPONENT24, self.__width, self.__height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.__depth_buffer)

    def get_color_texture(self) -> int:
        """
        :return: The ID of the texture containing the colour buffer of the FBO.
        """
        return self.__color_texture

    def get_depth_texture(self) -> int:
        """
        :return: The texture containing the FBOs depth buffer.
        """
        return self.__depth_texture

    def get_frame_buffer(self) -> int:
        return self.__frame_buffer

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height
