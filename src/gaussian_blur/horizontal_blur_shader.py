from src.shaders.shader_program import ShaderProgram
from sys import path


class HorizontalBlurShader(ShaderProgram):

    __VERTEX_FILE = f"{path[0]}/src/gaussian_blur/horizontal_blur_vertex.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/gaussian_blur/blur_fragment.glsl"

    def __init__(self):
        self.__location_target_width: int = -1
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def load_target_width(self, width: float) -> None:
        super().load_float(self.__location_target_width, width)

    def get_all_uniform_locations(self) -> None:
        self.__location_target_width = super().get_uniform_location("target_width")

    def bind_attributes(self) -> None:
        super().bind_attribute(0, "position")

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
