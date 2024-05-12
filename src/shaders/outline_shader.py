from .shader_program import ShaderProgram
from sys import path
from src.toolbox.maths import Maths


class OutlineShader(ShaderProgram):

    __VERTEX_FILE = f"{path[0]}/src/shaders/outline_vertex_shader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/shaders/outline_fragment_shader.glsl"

    def __init__(self):
        self.__location_projection_matrix: int = 0
        self.__location_model_texture: int = 0
        self.__location_outline_thickness: int = 0
        self.__location_outline_colour: int = 0
        self.__location_outline_threshold: int = 0
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def bind_attributes(self):
        super().bind_attribute(0, "a_position")
        super().bind_attribute(1, "a_tex_coords")

    def get_all_uniform_locations(self):
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_model_texture = super().get_uniform_location("model_texture")
        self.__location_outline_thickness = super().get_uniform_location("outline_thickness")
        self.__location_outline_colour = super().get_uniform_location("outline_colour")
        self.__location_outline_threshold = super().get_uniform_location("outline_threshold")

    def connect_texture_units(self) -> None:
        super().load_int(self.__location_model_texture, 0)

    def load_projection_matrix(self, projection: list[list]) -> None:
        super().load_matrix(self.__location_projection_matrix, projection)

    def load_outline_thickness(self, thickness: float) -> None:
        super().load_float(self.__location_outline_thickness, thickness)

    def load_outline_colour(self, colour: list[float]) -> None:
        super().load_4d_vector(self.__location_outline_colour, colour)

    def load_outline_threshold(self, threshold: float):
        super().load_float(self.__location_outline_threshold, threshold)

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
