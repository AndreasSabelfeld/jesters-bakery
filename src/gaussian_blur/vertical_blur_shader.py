from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class VerticalBlurShader(ShaderProgram):

    __VERTEX_FILE = f"{PATH}/src/gaussian_blur/vertical_blur_vertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/gaussian_blur/blur_fragment.glsl"

    def __init__(self):
        self.__location_target_height: int = -1
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def load_target_height(self, height: float) -> None:
        super().load_float(self.__location_target_height, height)

    def get_all_uniform_locations(self) -> None:
        self.__location_target_height = super().get_uniform_location("target_height")

    def bind_attributes(self) -> None:
        super().bind_attribute(0, "position")

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
