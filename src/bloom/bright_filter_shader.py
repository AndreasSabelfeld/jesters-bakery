from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class BrightFilterShader(ShaderProgram):
    """
    Shader program for applying a bright filter during the post-processing phase.
    """

    __VERTEX_FILE = f"{PATH}/src/bloom/simple_vertex.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/bloom/bright_filter_fragment.glsl"

    def __init__(self):
        """
        Initializes the BrightFilterShader by loading the vertex and fragment shader files.
        """
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self):
        """
        Collects the locations of all uniform variables used in the shader program.
        (Here there are none)
        """
        ...

    def bind_attributes(self) -> None:
        """
        Binds attribute locations to variables in the shader program.
        """
        super().bind_attribute(0, "position")

    @classmethod
    def get_vertex_file(cls) -> str:
        """
        Gets the file path for the vertex shader.

        :return: The file path of the vertex shader.
        """
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        """
        Gets the file path for the fragment shader.

        :return: The file path of the fragment shader.
        """
        return cls.__FRAGMENT_FILE
