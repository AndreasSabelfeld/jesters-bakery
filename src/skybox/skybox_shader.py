from src.toolbox.path import PATH
from src.shaders.shader_program import ShaderProgram
from src.toolbox.maths import Maths
from src.render_engine.time import Time


class SkyboxShader(ShaderProgram):
    """
    Handles the skybox shader, including uniforms for projection, view, and fog.
    """

    __VERTEX_FILE = f"{PATH}/src/skybox/skyboxVertexShader.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/skybox/skyboxFragmentShader.glsl"

    __ROTATE_SPEED = 1

    def __init__(self):
        """
        Initializes the SkyboxShader and sets up uniform locations.
        If cel shading is enabled, it uses the cel-shaded fragment shader.
        """
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            SkyboxShader.__FRAGMENT_FILE = f"{PATH}/src/skybox/cel_skyboxFragmentShader.glsl"

        self.__location_projection_matrix = 0
        self.__location_view_matrix = 0
        self.__location_fog_color = 0
        self.__location_cube_map_1 = 0
        self.__location_cube_map_2 = 0
        self.__location_blend_factor = 0
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

        self.__rotation = 0

    def get_all_uniform_locations(self) -> None:
        """
        Gets all uniform locations
        """
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_view_matrix = super().get_uniform_location("view_matrix")
        self.__location_fog_color = super().get_uniform_location("fog_color")
        self.__location_cube_map_1 = super().get_uniform_location("cube_map_1")
        self.__location_cube_map_2 = super().get_uniform_location("cube_map_2")
        self.__location_blend_factor = super().get_uniform_location("blend_factor")

    def bind_attributes(self) -> None:
        """
        Binds the attributes
        """
        super().bind_attribute(0, "position")

    def connect_texture_units(self) -> None:
        """
        Connects texture units to the shader program.
        """
        super().load_int(self.__location_cube_map_1, 0)
        super().load_int(self.__location_cube_map_2, 1)

    def load_blend_factor(self, blend: float) -> None:
        """
        Loads the blend factor into the shader.

        :params blend: The blend factor between the day and night textures.
        """
        super().load_float(self.__location_blend_factor, blend)

    def load_fog_color(self, r: float, g: float, b: float) -> None:
        """
        Loads the fog color into the shader.

        :params r: The red component of the fog color.
        :params g: The green component of the fog color.
        :params b: The blue component of the fog color.
        """
        super().load_vector(self.__location_fog_color, [r, g, b])

    def load_projection_matrix(self, matrix: list[list]) -> None:
        """
        Loads the projection matrix into the shader.

        :params matrix: The projection matrix to load.
        """
        super().load_matrix(self.__location_projection_matrix, matrix)

    def load_view_matrix(self, camera) -> None:
        """
        Loads the view matrix into the shader, applying a rotation to simulate the skybox rotation.

        :params camera: The camera from which to create the view matrix.
        """
        matrix = Maths.create_view_matrix(camera)
        self.__rotation += self.__ROTATE_SPEED * Time.get_delta_time()
        matrix = Maths.rotate_matrix_y_axis(matrix, self.__rotation)
        super().load_matrix(self.__location_view_matrix, matrix)
