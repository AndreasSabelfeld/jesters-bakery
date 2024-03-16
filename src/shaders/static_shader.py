from .shader_program import ShaderProgram
from sys import path
from src.toolbox.maths import Maths


class StaticShader(ShaderProgram):

    __MAX_LIGHTS = 5

    __VERTEX_FILE = f"{path[0]}/src/shaders/vertexShader.glsl"
    __GEOMETRY_FILE = f"{path[0]}/src/shaders/geometryShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/shaders/fragmentShader.glsl"

    def __init__(self):
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            StaticShader.__FRAGMENT_FILE = f"{path[0]}/src/shaders/cel_fragmentShader.glsl"

        self.__location_transformation_matrix: int = 0  # no location
        self.__location_projection_matrix: int = 0
        self.__location_view_matrix: int = 0
        self.__location_light_position: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_light_color: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_attenuation: list[int] = [0] * self.__MAX_LIGHTS
        self.__location_shine_damper: int = 0
        self.__location_reflectivity: int = 0
        self.__location_use_fake_lighting: int = 0
        self.__location_sky_color: int = 0
        self.__location_number_of_rows: int = 0
        self.__location_offset: int = 0
        self.__location_fog_density: int = 0
        self.__location_fog_gradient: int = 0
        self.__location_plane: int = 0
        self.__location_shadow_offset: int = 0
        self.__location_ortho_projection_matrix: int = 0
        self.__location_light_view_matrix: int = 0
        self.__location_shadow_map: int = 0
        self.__location_shadow_distance: int = 0
        self.__location_shadow_map_size: int = 0
        self.__location_specular_map: int = 0
        self.__location_uses_specular_map: int = 0
        self.__location_model_texture: int = 0
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
        self.__location_use_fake_lighting = super().get_uniform_location("use_fake_lighting")
        self.__location_sky_color = super().get_uniform_location("sky_color")
        self.__location_number_of_rows = super().get_uniform_location("number_of_rows")
        self.__location_offset = super().get_uniform_location("offset")
        self.__location_fog_density = super().get_uniform_location("fog_density")
        self.__location_fog_gradient = super().get_uniform_location("fog_gradient")
        self.__location_plane = super().get_uniform_location("plane")
        self.__location_shadow_offset = super().get_uniform_location("shadow_offset")
        self.__location_ortho_projection_matrix = super().get_uniform_location("ortho_projection_matrix")
        self.__location_light_view_matrix = super().get_uniform_location("light_view_matrix")
        self.__location_shadow_map = super().get_uniform_location("shadow_map")
        self.__location_shadow_distance = super().get_uniform_location("shadow_distance")
        self.__location_shadow_map_size = super().get_uniform_location("shadow_map_size")
        self.__location_specular_map = super().get_uniform_location("specular_map")
        self.__location_uses_specular_map = super().get_uniform_location("uses_specular_map")
        self.__location_model_texture = super().get_uniform_location("model_texture")

        for i in range(self.__MAX_LIGHTS):
            self.__location_light_position[i] = super().get_uniform_location(f"light_position[{i}]")
            self.__location_light_color[i] = super().get_uniform_location(f"light_color[{i}]")
            self.__location_attenuation[i] = super().get_uniform_location(f"attenuation[{i}]")

    def load_shadow_map_size(self, size: float) -> None:
        super().load_float(self.__location_shadow_map_size, size)

    def load_shadow_distance(self, shadow_distance: float) -> None:
        super().load_float(self.__location_shadow_distance, shadow_distance)

    def connect_texture_units(self) -> None:
        super().load_int(self.__location_shadow_map, 5)
        super().load_int(self.__location_model_texture, 0)
        super().load_int(self.__location_specular_map, 1)

    def load_use_specular_map(self, use_map: bool) -> None:
        super().load_boolean(self.__location_uses_specular_map, use_map)

    def load_to_shadow_space_matrix(self, offset: list[list], ortho_projection_matrix: list[list],
                                    light_view_matrix: list[list]) -> None:
        super().load_matrix(self.__location_shadow_offset, offset)
        super().load_matrix(self.__location_ortho_projection_matrix, ortho_projection_matrix)
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_clip_plane(self, plane: list[float]) -> None:
        super().load_4d_vector(self.__location_plane, plane)

    def load_number_of_rows(self, number_of_rows: int) -> None:
        super().load_float(self.__location_number_of_rows, number_of_rows)

    def load_offset(self, x: float, y: float) -> None:
        super().load_2d_vector(self.__location_offset, [x, y])

    def load_fog_density(self, density: float) -> None:
        super().load_float(self.__location_fog_density, density)

    def load_fog_gradient(self, gradient: float) -> None:
        super().load_float(self.__location_fog_gradient, gradient)

    def load_sky_color(self, r: float, g: float, b: float) -> None:
        super().load_vector(self.__location_sky_color, [r, g, b])

    def load_fake_lighting(self, use_fake: bool) -> None:
        super().load_boolean(self.__location_use_fake_lighting, use_fake)

    def load_shine_variables(self, damper: float, reflectivity: float) -> None:
        super().load_float(self.__location_shine_damper, damper)
        super().load_float(self.__location_reflectivity, reflectivity)

    def load_transformation_matrix(self, matrix: list[list]) -> None:
        super().load_matrix(self.__location_transformation_matrix, matrix)

    def load_projection_matrix(self, projection: list[list]) -> None:
        super().load_matrix(self.__location_projection_matrix, projection)

    def load_view_matrix(self, camera) -> None:
        view_matrix = Maths.create_view_matrix(camera)
        super().load_matrix(self.__location_view_matrix, view_matrix)

    def load_lights(self, lights: list) -> None:
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
    def get_vertex_file(cls) -> str:
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls) -> str:
        return cls.__FRAGMENT_FILE

    @classmethod
    def get_geometry_file(cls) -> str:
        return cls.__GEOMETRY_FILE
