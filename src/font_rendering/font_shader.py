from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class FontShader(ShaderProgram):
    """Shader program for rendering fonts."""

    __VERTEX_FILE = f"{PATH}/src/font_rendering/fontVertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/font_rendering/fontFragment.glsl"

    def __init__(self):
        """Initializes the FontShader and gets uniform locations."""
        self.__location_color: int = -1
        self.__location_translation: int = -1
        self.__location_width: int = -1
        self.__location_edge: int = -1
        self.__location_border_width: int = -1
        self.__location_border_edge: int = -1
        self.__location_offset: int = -1
        self.__location_outline_color: int = -1

        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self) -> None:
        """Collects the locations of all uniform variables used in the shader."""
        self.__location_color = super().get_uniform_location("color")
        self.__location_translation = super().get_uniform_location("translation")
        self.__location_width = super().get_uniform_location("width")
        self.__location_edge = super().get_uniform_location("edge")
        self.__location_border_width = super().get_uniform_location("border_width")
        self.__location_border_edge = super().get_uniform_location("border_edge")
        self.__location_offset = super().get_uniform_location("offset")
        self.__location_outline_color = super().get_uniform_location("outline_color")

    def bind_attributes(self) -> None:
        """Binds attribute locations for the vertex shader."""
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "texture_coords")

    def load_color(self, color: list[float]) -> None:
        """Loads the color uniform into the shader.

        :param color: A list of float values of the color (RGB).
        """
        super().load_vector(self.__location_color, color)

    def load_translation(self, translation: list[float]) -> None:
        """Loads the translation uniform into the shader.

        :param translation: A list of float values of the translation (x, y).
        """
        super().load_2d_vector(self.__location_translation, translation)

    def load_width(self, width: float) -> None:
        """Loads the width uniform into the shader.

        :param width: A float of the width of the text.
        """
        super().load_float(self.__location_width, width)

    def load_edge(self, edge: float) -> None:
        """Loads the edge uniform into the shader.

        :param edge: A float of the edge size for the text.
        """
        super().load_float(self.__location_edge, edge)

    def load_border_width(self, border_width: float) -> None:
        """Loads the border width uniform into the shader.

        :param border_width: A float of the width of the text border.
        """
        super().load_float(self.__location_border_width, border_width)

    def load_border_edge(self, border_edge: float) -> None:
        """Loads the border edge uniform into the shader.

        :param border_edge: A float of the border edge size for the text.
        """
        super().load_float(self.__location_border_edge, border_edge)

    def load_offset(self, offset: list[float]) -> None:
        """Loads the offset uniform into the shader.

        :param offset: A list of float values of the offset (x, y).
        """
        super().load_2d_vector(self.__location_offset, offset)

    def load_outline_color(self, outline_color: list[float]) -> None:
        """Loads the outline color uniform into the shader.

        :param outline_color: A list of float values of the outline color (RGB).
        """
        super().load_vector(self.__location_outline_color, outline_color)

    @classmethod
    def get_vertex_file(cls) -> str:
        """Returns the path to the vertex shader file.

        :return: The path to the vertex shader file.
        """
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        """Returns the path to the fragment shader file.

        :return: The path to the fragment shader file.
        """
        return cls.__FRAGMENT_FILE
