from src.shaders.shader_program import ShaderProgram
from sys import path


class ContrastShader(ShaderProgram):

    __VERTEX_FILE = f"{path[0]}/src/post_processing/contrast_vertex.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/post_processing/contrast_fragment.glsl"

    def __init__(self):
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self):
        ...

    def bind_attributes(self):
        ...

    @classmethod
    def get_vertex_file(cls):
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls):
        return cls.__FRAGMENT_FILE
