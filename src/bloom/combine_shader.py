from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class CombineShader(ShaderProgram):
    """
    Shader program for combining color and highlight textures during post-processing.
    """

    __VERTEX_FILE = f"{PATH}/src/bloom/simple_vertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/bloom/combine_fragment.glsl"

    def __init__(self):
        """
        Initializes the CombineShader.
        """
        self.__location_color_texture: int = 0
        self.__location_highlight_texture: int = 0
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self) -> None:
        """
        Collects the uniform locations from the shader program.
        """
        self.__location_color_texture = super().get_uniform_location("color_texture")
        self.__location_highlight_texture = super().get_uniform_location("highlight_texture")

    def bind_attributes(self) -> None:
        """
        Binds the attributes in the shader program.
        """
        super().bind_attribute(0, "position")

    def connect_texture_units(self) -> None:
        """
        Connects the texture units.
        """
        super().load_int(self.__location_color_texture, 0)
        super().load_int(self.__location_highlight_texture, 1)

    @classmethod
    def get_vertex_file(cls) -> str:
        """
        Returns the file path of the vertex shader.

        :return: The file path of the vertex shader.
        """
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        """
        Returns the file path of the fragment shader.

        :return: The file path of the fragment shader.
        """
        return cls.__FRAGMENT_FILE
