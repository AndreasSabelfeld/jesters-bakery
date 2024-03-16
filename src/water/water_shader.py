from sys import path
from src.shaders.shader_program import ShaderProgram
from src.toolbox.maths import Maths


class WaterShader(ShaderProgram):
    __VERTEX_FILE = f"{path[0]}/src/water/waterVertexShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/water/waterFragmentShader.glsl"

    def __init__(self):
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            WaterShader.__FRAGMENT_FILE = f"{path[0]}/src/water/cel_waterFragmentShader.glsl"

        self.__location_model_matrix: int = 0
        self.__location_projection_matrix: int = 0
        self.__location_view_matrix: int = 0
        self.__location_reflection_texture: int = 0
        self.__location_refraction_texture: int = 0
        self.__location_dudv_map: int = 0
        self.__location_move_factor: int = 0
        self.__location_camera_position: int = 0
        self.__location_normal_map: int = 0
        self.__location_light_color: int = 0
        self.__location_light_position: int = 0
        self.__location_depth_map: int = 0
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def get_all_uniform_locations(self):
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_view_matrix = super().get_uniform_location("view_matrix")
        self.__location_model_matrix = super().get_uniform_location("model_matrix")
        self.__location_reflection_texture = super().get_uniform_location("reflection_texture")
        self.__location_refraction_texture = super().get_uniform_location("refraction_texture")
        self.__location_dudv_map = super().get_uniform_location("dudv_map")
        self.__location_move_factor = super().get_uniform_location("move_factor")
        self.__location_camera_position = super().get_uniform_location("camera_position")
        self.__location_normal_map = super().get_uniform_location("normal_map")
        self.__location_light_color = super().get_uniform_location("light_color")
        self.__location_light_position = super().get_uniform_location("light_position")
        self.__location_depth_map = super().get_uniform_location("depth_map")

    def connect_texture_units(self):
        super().load_int(self.__location_reflection_texture, 0)
        super().load_int(self.__location_refraction_texture, 1)
        super().load_int(self.__location_dudv_map, 2)
        super().load_int(self.__location_normal_map, 3)
        super().load_int(self.__location_depth_map, 4)

    def load_light(self, sun):
        super().load_vector(self.__location_light_color, sun.get_color())
        super().load_vector(self.__location_light_position, sun.get_position())

    def load_move_factor(self, factor: float):
        super().load_float(self.__location_move_factor, factor)

    def bind_attributes(self):
        super().bind_attribute(0, "position")

    def load_projection_matrix(self, matrix: list[list]):
        super().load_matrix(self.__location_projection_matrix, matrix)

    def load_view_matrix(self, camera):
        matrix = Maths.create_view_matrix(camera)
        super().load_matrix(self.__location_view_matrix, matrix)
        super().load_vector(self.__location_camera_position, camera.get_position())

    def load_model_matrix(self, model_matrix: list[list]):
        super().load_matrix(self.__location_model_matrix, model_matrix)
