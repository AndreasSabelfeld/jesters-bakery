import glfw
from OpenGL.GL import *
from OpenGL.GL.EXT.texture_filter_anisotropic import *
from OpenGL.GLUT import *
from PIL import Image
import numpy
from src.toolbox.path import PATH

from src.models.raw_model import RawModel
from src.textures.texture_data import TextureData


class Loader:
    """
    This class creates and keeps track of all VAOs and VBOs and is responsible for binding them
    """
    __vaos = []
    __vbos = []
    __textures = []
    __extensions_supported = []

    def __init__(self):
        Loader.read_supported_extensions()

    def create_empty_vbo(self, float_count: int) -> int:
        vbo = glGenBuffers(1)
        self.__vbos.append(vbo)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, float_count * 4, None, GL_STREAM_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        return vbo

    @staticmethod
    def add_instanced_attribute(vao: int, vbo: int, attribute: int, data_size: int, instanced_data_length: int,
                                offset: int) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBindVertexArray(vao)
        glVertexAttribPointer(attribute, data_size, GL_FLOAT, False, instanced_data_length * 4, ctypes.c_void_p(offset * 4))
        glVertexAttribDivisor(attribute, 1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @staticmethod
    def update_vbo(vbo: int, data: list[float]) -> None:
        data = numpy.array(data, dtype='float32')  # convert the data into a float32 array

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(data) * 4, None, GL_STREAM_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, len(data) * 4, data)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def load_to_vao(self, positions: list[float], texture_coords: list[float], normals: list[float], indices: list[int]):
        vao_id = self.create_vao()               # creates VAO
        self.bind_indices_buffer(indices)        # every vertex is given an index for the order
        self.store_data_in_attribute_list(0, 3, positions)          # binds the positions into the 0th place in the VAO
        self.store_data_in_attribute_list(1, 2, texture_coords)     # binds the texture coords into 1st place in the VAO
        self.store_data_in_attribute_list(2, 3, normals)            # binds the normals into 2nd place in the VAO
        self.unbind_vao()                                           # unbinds the vao
        return RawModel(vao_id, len(indices), positions, indices.copy())   # returns raw model object

    def load_tangents_to_vao(self, positions: list[float], texture_coords: list[float], normals: list[float],
                             tangents: list[float], indices: list[int]):

        vao_id = self.create_vao()
        self.bind_indices_buffer(indices)
        self.store_data_in_attribute_list(0, 3, positions)
        self.store_data_in_attribute_list(1, 2, texture_coords)
        self.store_data_in_attribute_list(2, 3, normals)
        self.store_data_in_attribute_list(3, 3, tangents)
        self.unbind_vao()
        return RawModel(vao_id, len(indices), positions, indices.copy())

    def load_gui_to_vao(self, positions: list[float], dimension: int):
        vao_id = self.create_vao()
        self.store_data_in_attribute_list(0, dimension, positions)
        self.unbind_vao()
        return RawModel(vao_id, len(positions) // dimension)

    def load_font_to_vao(self, positions: list[float], texture_coords: list[float]) -> int:
        vao_id = self.create_vao()               # creates VAO
        self.store_data_in_attribute_list(0, 2, positions)       # binds the positions into the 0th place in the VAO
        self.store_data_in_attribute_list(1, 2, texture_coords)  # binds the texture coords into 1st place in the VAO
        self.unbind_vao()                                 # unbinds the vao
        return vao_id

    @classmethod
    def load_texture(cls, file_name: str, bias: float = -0.6):
        try:
            img = Image.open(f"{PATH}/res/{file_name}.png").convert('RGBA')
        except Exception as e:
            print(e)
            # missing texture
            img = Image.new(mode="RGB", size=(2, 2), color=(210, 0, 160))
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip image upside down

        ix, iy, image = img.size[0], img.size[1], img.tobytes("raw", "RGBA", 0, -1)

        texture_id = glGenTextures(1)             # generate a texture ID
        cls.__textures.append(texture_id)
        glBindTexture(GL_TEXTURE_2D, texture_id)  # make it current
        # copy the texture into the current texture texture_id
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)

        if b'GL_EXT_texture_filter_anisotropic' in cls.__extensions_supported:
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, 0)
            amount = min(4, glGetFloat(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT))
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, amount)
        else:
            print("Anisotropic filtering not supported!")
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_LOD_BIAS, bias)

        return texture_id

    def load_cube_map(self, texture_files: list[str]):
        """Order of the cube map textures has to be: RIGHT, LEFT, TOP, BOTTOM, BACK, FRONT"""
        texture_id = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

        for i in range(len(texture_files)):
            data = self.decode_texture_file(f"{texture_files[i]}")
            glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL_RGBA, data.get_width(), data.get_height(), 0,
                         GL_RGBA, GL_UNSIGNED_BYTE, data.get_byte_data())

        glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        self.__textures.append(texture_id)
        return texture_id

    @staticmethod
    def decode_texture_file(file_name: str):
        try:
            img = Image.open(f"{PATH}/res/{file_name}.png").convert('RGBA')
            img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip image upside down
        except Exception as e:
            print(e)
            missing_texture = Image.new(mode="RGB", size=(2, 2), color=(210, 0, 160))
            missing_texture.save(f"{PATH}/res/pngs/missing_texture.png")
            img = Image.open(f"{PATH}/res/pngs/missing_texture.png").convert('RGBA')
            img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip image upside down
        width, height, data = img.size[0], img.size[1], img.tobytes("raw", "RGBA", 0, -1)
        return TextureData(data, width, height)

    @classmethod
    def clean_up(cls):
        for vao in cls.__vaos:
            glDeleteVertexArrays(1, [vao])
        for vbo in cls.__vbos:
            glDeleteBuffers(1, [vbo])
        for texture in cls.__textures:
            glDeleteTextures(1, [texture])

    @classmethod
    def create_vao(cls):
        vao_id = glGenVertexArrays(1)   # creates 1 vertex array
        cls.__vaos.append(vao_id)       # appends it to the VAO list in the class
        glBindVertexArray(vao_id)       # binds the VAO to use it
        return vao_id

    @classmethod
    def store_data_in_attribute_list(cls, attribute_number: int, coordinate_size: int, data: list[float]):
        data = numpy.array(data, dtype='float32')   # convert the data into a float32 array
        vbo_id = glGenBuffers(1)                    # create 1 VBO buffer
        cls.__vbos.append(vbo_id)                   # appends it to the VBO list in the class
        glBindBuffer(GL_ARRAY_BUFFER, vbo_id)       # binds the buffer to use it
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)  # specifies the buffer, data and usage
        glVertexAttribPointer(attribute_number, coordinate_size, GL_FLOAT, False, 0, None)  # put the VBO into a VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    @staticmethod
    def unbind_vao():
        glBindVertexArray(0)

    @classmethod
    def bind_indices_buffer(cls, indices: list[int]):
        indices = numpy.array(indices, dtype=numpy.uint32)  # convert the data into an unsigned integer array
        vbo_id = glGenBuffers(1)
        cls.__vbos.append(vbo_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, vbo_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    @classmethod
    def read_supported_extensions(cls):
        num_of_extensions = glGetIntegerv(GL_NUM_EXTENSIONS)
        for i in range(num_of_extensions):
            cls.__extensions_supported.append(glGetStringi(GL_EXTENSIONS, i))
