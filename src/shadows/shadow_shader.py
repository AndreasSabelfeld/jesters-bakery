from src.shaders.shader_program import ShaderProgram

from sys import path


class ShadowShader(ShaderProgram):
    __VERTEX_FILE = f"{path[0]}/src/shadows/shadowVertexShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/shadows/shadowFragmentShader.glsl"

    def __init__(self):
        # self.__location_mvp_matrix: int = -1
        self.__location_light_view_matrix: int = -1
        self.__location_projection_matrix: int = -1
        self.__location_model_matrix: int = -1
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self) -> None:
        self.__location_light_view_matrix = super().get_uniform_location("light_view_matrix")
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_model_matrix = super().get_uniform_location("model_matrix")

    def bind_attributes(self) -> None:
        super().bind_attribute(0, "in_position")
        super().bind_attribute(1, "in_texture_coords")

    def load_light_view_matrix(self, light_view_matrix: list[list]) -> None:
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_projection_matrix(self, projection_matrix: list[list]) -> None:
        super().load_matrix(self.__location_projection_matrix, projection_matrix)

    def load_model_matrix(self, model_matrix: list[list]) -> None:
        super().load_matrix(self.__location_model_matrix, model_matrix)

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
