from OpenGL.GL import *
from src.render_engine.display_manager import DisplayManager


class WaterFrameBuffers:

    __REFLECTION_WIDTH = 320
    __REFLECTION_HEIGHT = 180

    __REFRACTION_WIDTH = 1280
    __REFRACTION_HEIGHT = 720

    def __init__(self):
        # initialize variables
        self.__reflection_frame_buffer = 0
        self.__reflection_texture = 0
        self.__reflection_depth_buffer = 0

        self.__refraction_frame_buffer = 0
        self.__refraction_texture = 0
        self.__refraction_depth_texture = 0

        self.initialise_reflection_frame_buffer()
        self.initialise_refraction_frame_buffer()

    def clean_up(self):
        glDeleteFramebuffers(self.__reflection_frame_buffer)
        glDeleteTextures(self.__reflection_texture)
        glDeleteRenderbuffers(self.__reflection_depth_buffer)
        glDeleteFramebuffers(self.__refraction_frame_buffer)
        glDeleteTextures(self.__refraction_texture)
        glDeleteTextures(self.__refraction_depth_texture)

    def bind_reflection_frame_buffer(self):
        # call before rendering to this FBO
        self.bind_frame_buffer(self.__reflection_frame_buffer, self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)

    def bind_refraction_frame_buffer(self):
        # call before rendering to this FBO
        self.bind_frame_buffer(self.__refraction_frame_buffer, self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)

    @staticmethod
    def unbind_current_frame_buffer():
        # call to switch to default frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, DisplayManager.get_viewport()[0], DisplayManager.get_viewport()[1])

    def get_reflection_texture(self):
        # get the resulting texture
        return self.__reflection_texture

    def get_refraction_texture(self):
        # get the resulting texture
        return self.__refraction_texture

    def get_refraction_depth_texture(self):
        # get the resulting depth texture
        return self.__refraction_depth_texture

    def initialise_reflection_frame_buffer(self):
        self.__reflection_frame_buffer = self.create_frame_buffer()
        self.__reflection_texture = self.create_texture_attachment(self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)
        self.__reflection_depth_buffer = self.create_depth_buffer_attachment(self.__REFLECTION_WIDTH, self.__REFLECTION_HEIGHT)
        self.unbind_current_frame_buffer()

    def initialise_refraction_frame_buffer(self):
        self.__refraction_frame_buffer = self.create_frame_buffer()
        self.__refraction_texture = self.create_texture_attachment(self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)
        self.__refraction_depth_texture = self.create_depth_texture_attachment(self.__REFRACTION_WIDTH, self.__REFRACTION_HEIGHT)
        self.unbind_current_frame_buffer()

    @staticmethod
    def bind_frame_buffer(frame_buffer: int, width: int, height: int):
        glBindTexture(GL_TEXTURE_2D, 0)  # to make sure the texture isn't bound
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        glViewport(0, 0, width, height)

    @staticmethod
    def create_frame_buffer():
        # generate ID for frame buffer
        frame_buffer = glGenFramebuffers(1)
        # bind the frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, frame_buffer)
        # indicate that we will always render to color attachment 0
        glDrawBuffer(GL_COLOR_ATTACHMENT0)
        return frame_buffer

    @staticmethod
    def create_texture_attachment(width: int, height: int):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, texture, 0)

        return texture

    @staticmethod
    def create_depth_texture_attachment(width: int, height: int):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT32, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, texture, 0)

        return texture

    @staticmethod
    def create_depth_buffer_attachment(width: int, height: int):
        depth_buffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depth_buffer)
        return depth_buffer
