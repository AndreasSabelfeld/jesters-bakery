from sys import path
from src.shaders.shader_program import ShaderProgram
from src.toolbox.maths import Maths
from src.render_engine.time import Time


class SkyboxShader(ShaderProgram):
    __VERTEX_FILE = f"{path[0]}/src/skybox/skyboxVertexShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/skybox/skyboxFragmentShader.glsl"

    __ROTATE_SPEED = 1

    def __init__(self):
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            SkyboxShader.__FRAGMENT_FILE = f"{path[0]}/src/skybox/cel_skyboxFragmentShader.glsl"

        self.__location_projection_matrix = 0
        self.__location_view_matrix = 0
        self.__location_fog_color = 0
        self.__location_cube_map_1 = 0
        self.__location_cube_map_2 = 0
        self.__location_blend_factor = 0
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

        self.__rotation = 0

    def get_all_uniform_locations(self):
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_view_matrix = super().get_uniform_location("view_matrix")
        self.__location_fog_color = super().get_uniform_location("fog_color")
        self.__location_cube_map_1 = super().get_uniform_location("cube_map_1")
        self.__location_cube_map_2 = super().get_uniform_location("cube_map_2")
        self.__location_blend_factor = super().get_uniform_location("blend_factor")

    def bind_attributes(self):
        super().bind_attribute(0, "position")

    def connect_texture_units(self):
        super().load_int(self.__location_cube_map_1, 0)
        super().load_int(self.__location_cube_map_2, 1)

    def load_blend_factor(self, blend: float):
        super().load_float(self.__location_blend_factor, blend)

    def load_fog_color(self, r: float, g: float, b: float):
        super().load_vector(self.__location_fog_color, [r, g, b])

    def load_projection_matrix(self, matrix: list[list]):
        super().load_matrix(self.__location_projection_matrix, matrix)

    def load_view_matrix(self, camera):
        matrix = Maths.create_view_matrix(camera)
        self.__rotation += self.__ROTATE_SPEED * Time.get_delta_time()
        matrix = Maths.rotate_matrix_y_axis(matrix, self.__rotation)
        super().load_matrix(self.__location_view_matrix, matrix)
