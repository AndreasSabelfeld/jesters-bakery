from src.shaders.shader_program import ShaderProgram
from sys import path
from src.toolbox.maths import Maths


class TerrainShader(ShaderProgram):

    __MAX_LIGHTS = 5

    __VERTEX_FILE = f"{path[0]}/src/terrain/terrainVertexShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/terrain/terrainFragmentShader.glsl"

    def __init__(self):
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            TerrainShader.__FRAGMENT_FILE = f"{path[0]}/src/shaders/cel_terrainFragmentShader.glsl"
        self.__location_transformation_matrix: int = 0  # no location
        self.__location_projection_matrix: int = 0
        self.__location_view_matrix: int = 0
        self.__location_light_position: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_light_color: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_attenuation: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_shine_damper: int = 0
        self.__location_reflectivity: int = 0
        self.__location_sky_color: int = 0
        self.__location_fog_density: int = 0
        self.__location_fog_gradient: int = 0
        self.__location_background_texture: int = 0
        self.__location_r_texture: int = 0
        self.__location_g_texture: int = 0
        self.__location_b_texture: int = 0
        self.__location_blend_map: int = 0
        self.__location_plane: int = 0
        self.__location_offset: int = 0
        self.__location_ortho_projection_matrix: int = 0
        self.__location_light_view_matrix: int = 0
        self.__location_shadow_map: int = 0
        self.__location_shadow_distance: int = 0
        self.__location_shadow_map_size: int = 0
        super().__init__(self.get_vertex_file(), self.get_fragment_file())

    def bind_attributes(self):
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "texture_coords")
        super().bind_attribute(2, "normal")

    def get_all_uniform_locations(self):
        self.__location_transformation_matrix = super().get_uniform_location("transformation_matrix")
        self.__location_projection_matrix = super().get_uniform_location("projection_matrix")
        self.__location_view_matrix = super().get_uniform_location("view_matrix")
        self.__location_shine_damper = super().get_uniform_location("shine_damper")
        self.__location_reflectivity = super().get_uniform_location("reflectivity")
        self.__location_sky_color = super().get_uniform_location("sky_color")
        self.__location_fog_density = super().get_uniform_location("fog_density")
        self.__location_fog_gradient = super().get_uniform_location("fog_gradient")
        self.__location_background_texture = super().get_uniform_location("background_texture")
        self.__location_r_texture = super().get_uniform_location("r_texture")
        self.__location_g_texture = super().get_uniform_location("g_texture")
        self.__location_b_texture = super().get_uniform_location("b_texture")
        self.__location_blend_map = super().get_uniform_location("blend_map")
        self.__location_plane = super().get_uniform_location("plane")
        self.__location_offset = super().get_uniform_location("offset")
        self.__location_ortho_projection_matrix = super().get_uniform_location("ortho_projection_matrix")
        self.__location_light_view_matrix = super().get_uniform_location("light_view_matrix")
        self.__location_shadow_map = super().get_uniform_location("shadow_map")
        self.__location_shadow_distance = super().get_uniform_location("shadow_distance")
        self.__location_shadow_map_size = super().get_uniform_location("shadow_map_size")

        for i in range(self.__MAX_LIGHTS):
            self.__location_light_position[i] = super().get_uniform_location(f"light_position[{i}]")
            self.__location_light_color[i] = super().get_uniform_location(f"light_color[{i}]")
            self.__location_attenuation[i] = super().get_uniform_location(f"attenuation[{i}]")

    def load_shadow_map_size(self, size: float):
        super().load_float(self.__location_shadow_map_size, size)

    def load_shadow_distance(self, shadow_distance: float) -> None:
        super().load_float(self.__location_shadow_distance, shadow_distance)

    def load_to_shadow_space_matrix(self, offset: list[list], ortho_projection_matrix: list[list],
                                    light_view_matrix: list[list]) -> None:
        super().load_matrix(self.__location_offset, offset)
        super().load_matrix(self.__location_ortho_projection_matrix, ortho_projection_matrix)
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_clip_plane(self, plane: list[float]):
        super().load_4d_vector(self.__location_plane, plane)

    def connect_texture_units(self):
        super().load_int(self.__location_background_texture, 0)
        super().load_int(self.__location_r_texture, 1)
        super().load_int(self.__location_g_texture, 2)
        super().load_int(self.__location_b_texture, 3)
        super().load_int(self.__location_blend_map, 4)
        super().load_int(self.__location_shadow_map, 5)

    def load_fog_density(self, density: float):
        super().load_float(self.__location_fog_density, density)

    def load_fog_gradient(self, gradient: float):
        super().load_float(self.__location_fog_gradient, gradient)

    def load_sky_color(self, r: float, g: float, b: float):
        super().load_vector(self.__location_sky_color, [r, g, b])

    def load_shine_variables(self, damper: float, reflectivity: float):
        super().load_float(self.__location_shine_damper, damper)
        super().load_float(self.__location_reflectivity, reflectivity)

    def load_transformation_matrix(self, matrix: list[list]):
        super().load_matrix(self.__location_transformation_matrix, matrix)

    def load_projection_matrix(self, projection: list[list]):
        super().load_matrix(self.__location_projection_matrix, projection)

    def load_view_matrix(self, camera):
        view_matrix = Maths.create_view_matrix(camera)
        super().load_matrix(self.__location_view_matrix, view_matrix)

    def load_lights(self, lights: list):
        for i in range(self.__MAX_LIGHTS):
            if i < len(lights):
                super().load_vector(self.__location_light_position[i], lights[i].get_position())
                super().load_vector(self.__location_light_color[i], lights[i].get_color())
                super().load_vector(self.__location_attenuation[i], lights[i].get_attenuation())
            else:
                super().load_vector(self.__location_light_position[i], [0, 0, 0])
                super().load_vector(self.__location_light_color[i], [0, 0, 0])
                super().load_vector(self.__location_attenuation[i], [1, 0, 0])

    @classmethod
    def get_vertex_file(cls):
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls):
        return cls.__FRAGMENT_FILE
