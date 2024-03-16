from src.shaders.shader_program import ShaderProgram
from sys import path


class FontShader(ShaderProgram):
    __VERTEX_FILE = f"{path[0]}/src/font_rendering/fontVertex.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/font_rendering/fontFragment.glsl"

    def __init__(self):
        self.__location_color: int = -1
        self.__location_translation: int = -1
        self.__location_width: int = -1
        self.__location_edge: int = -1
        self.__location_border_width: int = -1
        self.__location_border_edge: int = -1
        self.__location_offset: int = -1
        self.__location_outline_color: int = -1

        super().__init__(self.get_vertex_file(), self.get_fragment_file())  # needs to be called at the END of the function

    def get_all_uniform_locations(self) -> None:
        self.__location_color = super().get_uniform_location("color")
        self.__location_translation = super().get_uniform_location("translation")
        self.__location_width = super().get_uniform_location("width")
        self.__location_edge = super().get_uniform_location("edge")
        self.__location_border_width = super().get_uniform_location("border_width")
        self.__location_border_edge = super().get_uniform_location("border_edge")
        self.__location_offset = super().get_uniform_location("offset")
        self.__location_outline_color = super().get_uniform_location("outline_color")

    def bind_attributes(self):
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "texture_coords")

    def load_color(self, color: list[float]) -> None:
        super().load_vector(self.__location_color, color)

    def load_translation(self, translation: list[float]) -> None:
        super().load_2d_vector(self.__location_translation, translation)

    def load_width(self, width: float) -> None:
        super().load_float(self.__location_width, width)

    def load_edge(self, edge: float) -> None:
        super().load_float(self.__location_edge, edge)

    def load_border_width(self, border_width: float) -> None:
        super().load_float(self.__location_border_width, border_width)

    def load_border_edge(self, border_edge: float) -> None:
        super().load_float(self.__location_border_edge, border_edge)

    def load_offset(self, offset: list[float]) -> None:
        super().load_2d_vector(self.__location_offset, offset)

    def load_outline_color(self, outline_color: list[float]) -> None:
        super().load_vector(self.__location_outline_color, outline_color)

    @classmethod
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE
