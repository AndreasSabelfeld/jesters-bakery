from src.shaders.shader_program import ShaderProgram
from sys import path


class CombineShader(ShaderProgram):

    __VERTEX_FILE = f"{path[0]}/src/bloom/simple_vertex.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/bloom/combine_fragment.glsl"

    def __init__(self):
        self.__location_color_texture: int = 0
        self.__location_highlight_texture: int = 0
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self) -> None:
        self.__location_color_texture = super().get_uniform_location("color_texture")
        self.__location_highlight_texture = super().get_uniform_location("highlight_texture")

    def bind_attributes(self) -> None:
        super().bind_attribute(0, "position")

    def connect_texture_units(self) -> None:
        super().load_int(self.__location_color_texture, 0)
        super().load_int(self.__location_highlight_texture, 1)

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
