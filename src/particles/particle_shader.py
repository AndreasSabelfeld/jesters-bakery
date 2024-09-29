from src.shaders.shader_program import ShaderProgram

from src.toolbox.path import PATH


class ParticleShader(ShaderProgram):
    __VERTEX_FILE = f"{PATH}/src/particles/particleVertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/particles/particleFragment.glsl"

    def __init__(self):
        self.__location_number_of_rows: int = -1
        self.__location_projection_matrix: int = -1
        super().__init__(self.get_vertex_file(), self.get_fragment_file())  # needs to be called at the END of the function

    def get_all_uniform_locations(self) -> None:
        self.__location_number_of_rows = super().get_uniform_location("number_of_rows")
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")

    def bind_attributes(self):
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "model_view_matrix")
        super().bind_attribute(5, "tex_offsets")
        super().bind_attribute(6, "blend_factor")

    def load_number_of_rows(self, number_of_rows: float):
        super().load_float(self.__location_number_of_rows, number_of_rows)

    def load_projection_matrix(self, projection_matrix: list[list]) -> None:
        super().load_matrix(self.__location_projection_matrix, projection_matrix)

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
