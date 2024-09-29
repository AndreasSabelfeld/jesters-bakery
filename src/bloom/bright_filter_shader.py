from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class BrightFilterShader(ShaderProgram):

    __VERTEX_FILE = f"{PATH}/src/bloom/simple_vertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/bloom/bright_filter_fragment.glsl"

    def __init__(self):
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self):
        ...

    def bind_attributes(self):
        super().bind_attribute(0, "position")

    @classmethod
    def get_vertex_file(cls):
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls):
        return cls.__FRAGMENT_FILE
