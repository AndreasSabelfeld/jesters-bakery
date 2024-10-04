from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class ShadowShader(ShaderProgram):
    """
    ShadowShader handles the loading and binding of shaders used for shadows.
    """

    __VERTEX_FILE = f"{PATH}/src/shadows/shadowVertexShader.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/shadows/shadowFragmentShader.glsl"

    def __init__(self):
        """
        Initializes the ShadowShader with default locations for shader attributes.
        """
        # self.__location_mvp_matrix: int = -1
        self.__location_light_view_matrix: int = -1
        self.__location_projection_matrix: int = -1
        self.__location_model_matrix: int = -1
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def get_all_uniform_locations(self) -> None:
        """
        Gets all uniform locations for the shadow shader program.
        """
        self.__location_light_view_matrix = super().get_uniform_location("light_view_matrix")
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_model_matrix = super().get_uniform_location("model_matrix")

    def bind_attributes(self) -> None:
        """
        Binds attribute variables for the shadow shader program.
        """
        super().bind_attribute(0, "in_position")
        super().bind_attribute(1, "in_texture_coords")

    def load_light_view_matrix(self, light_view_matrix: list[list]) -> None:
        """
        Loads the light's view matrix into the shader.

        :params light_view_matrix: The light's view matrix to load.
        """
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_projection_matrix(self, projection_matrix: list[list]) -> None:
        """
        Loads the projection matrix into the shader.

        :params projection_matrix: The projection matrix to load.
        """
        super().load_matrix(self.__location_projection_matrix, projection_matrix)

    def load_model_matrix(self, model_matrix: list[list]) -> None:
        """
        Loads the model matrix into the shader.

        :params model_matrix: The model matrix to load.
        """
        super().load_matrix(self.__location_model_matrix, model_matrix)

    @classmethod
    def get_vertex_file(cls) -> str:
        """
        Returns the vertex shader file path.

        :return: The path of the vertex shader file.
        """
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        """
        Returns the fragment shader file path.

        :return: The path of the fragment shader file.
        """
        return cls.__FRAGMENT_FILE
