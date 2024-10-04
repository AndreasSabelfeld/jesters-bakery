from .shader_program import ShaderProgram
from src.toolbox.path import PATH
from src.toolbox.maths import Maths


class StaticShader(ShaderProgram):

    __MAX_LIGHTS = 5

    __VERTEX_FILE = f"{PATH}/src/shaders/vertexShader.glsl"
    __GEOMETRY_FILE = f"{PATH}/src/shaders/geometryShader.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/shaders/fragmentShader.glsl"

    def __init__(self):
        """
        Initializes the StaticShader
        """
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
        """
        Binds attribute variables for the shader program.
        """
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "texture_coords")
        super().bind_attribute(2, "normal")

    def get_all_uniform_locations(self):
        """
        Gets all uniform locations for the shader program.
        """
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
        """
        Loads the size of the shadow map.

        :params size: The size to load into the shadow map.
        """
        super().load_float(self.__location_shadow_map_size, size)

    def load_shadow_distance(self, shadow_distance: float) -> None:
        """
        Loads the shadow distance.

        :params shadow_distance: The distance to load for shadows.
        """
        super().load_float(self.__location_shadow_distance, shadow_distance)

    def connect_texture_units(self) -> None:
        """
        Connects texture units for the shader program.
        """
        super().load_int(self.__location_shadow_map, 5)
        super().load_int(self.__location_model_texture, 0)
        super().load_int(self.__location_specular_map, 1)

    def load_use_specular_map(self, use_map: bool) -> None:
        """
        Loads a boolean indicating if to use a specular map.

        :params use_map: Boolean value to indicate use of the specular map.
        """
        super().load_boolean(self.__location_uses_specular_map, use_map)

    def load_to_shadow_space_matrix(self, offset: list[list], ortho_projection_matrix: list[list],
                                     light_view_matrix: list[list]) -> None:
        """
        Loads the matrices to transform coordinates to shadow space.

        :params offset: The offset matrix to load.
        :params ortho_projection_matrix: The orthogonal projection matrix to load.
        :params light_view_matrix: The light's view matrix to load.
        """
        super().load_matrix(self.__location_shadow_offset, offset)
        super().load_matrix(self.__location_ortho_projection_matrix, ortho_projection_matrix)
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_clip_plane(self, plane: list[float]) -> None:
        """
        Loads the clip plane for the shader.

        :params plane: The clip plane values to load.
        """
        super().load_4d_vector(self.__location_plane, plane)

    def load_number_of_rows(self, number_of_rows: int) -> None:
        """
        Loads the number of texture rows.

        :params number_of_rows: The number of rows to load.
        """
        super().load_float(self.__location_number_of_rows, number_of_rows)

    def load_offset(self, x: float, y: float) -> None:
        """
        Loads the texture offset

        :params x: The x offset to load.
        :params y: The y offset to load.
        """
        super().load_2d_vector(self.__location_offset, [x, y])

    def load_fog_density(self, density: float) -> None:
        """
        Loads the fog density.

        :params density: The density of the fog to load.
        """
        super().load_float(self.__location_fog_density, density)

    def load_fog_gradient(self, gradient: float) -> None:
        """
        Loads the fog gradient.

        :params gradient: The gradient of the fog to load.
        """
        super().load_float(self.__location_fog_gradient, gradient)

    def load_sky_color(self, r: float, g: float, b: float) -> None:
        """
        Loads the color of the sky.

        :params r: The red component of the sky color.
        :params g: The green component of the sky color.
        :params b: The blue component of the sky color.
        """
        super().load_vector(self.__location_sky_color, [r, g, b])

    def load_fake_lighting(self, use_fake: bool) -> None:
        """
        Loads a boolean if to use of fake lighting.

        :params use_fake: Boolean value to indicate the use of fake lighting.
        """
        super().load_boolean(self.__location_use_fake_lighting, use_fake)

    def load_shine_variables(self, damper: float, reflectivity: float) -> None:
        """
        Loads the shine damper and reflectivity variables.

        :params damper: The shine damper value to load.
        :params reflectivity: The reflectivity value to load.
        """
        super().load_float(self.__location_shine_damper, damper)
        super().load_float(self.__location_reflectivity, reflectivity)

    def load_transformation_matrix(self, matrix: list[list]) -> None:
        """
        Loads the transformation matrix for the model.

        :params matrix: The transformation matrix to load.
        """
        super().load_matrix(self.__location_transformation_matrix, matrix)

    def load_projection_matrix(self, projection: list[list]) -> None:
        """
        Loads the projection matrix.

        :params projection: The projection matrix to load.
        """
        super().load_matrix(self.__location_projection_matrix, projection)

    def load_view_matrix(self, camera) -> None:
        """
        Loads the view matrix

        :params camera: The camera object to generate the view matrix.
        """
        view_matrix = Maths.create_view_matrix(camera)
        super().load_matrix(self.__location_view_matrix, view_matrix)

    def load_lights(self, lights: list) -> None:
        """
        Loads the lights into the shader.

        :params lights: A list of light objects to load.
        """
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

    @classmethod
    def get_geometry_file(cls) -> str:
        """
        Returns the geometry shader file path.

        :return: The path of the geometry shader file.
        """
        return cls.__GEOMETRY_FILE
