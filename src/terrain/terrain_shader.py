from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH
from src.toolbox.maths import Maths


class TerrainShader(ShaderProgram):
    """
    Shader class for rendering terrains.
    """

    __MAX_LIGHTS = 5

    __VERTEX_FILE = f"{PATH}/src/terrain/terrainVertexShader.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/terrain/terrainFragmentShader.glsl"

    def __init__(self):
        """
        Initializes the terrain shader
        """
        if ShaderProgram.get_is_cel():
            # if cel shading is activated use another shader
            TerrainShader.__FRAGMENT_FILE = f"{PATH}/src/shaders/cel_terrainFragmentShader.glsl"
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
        """
        Binds shader attributes for position, texture coordinates, and normals.
        """
        super().bind_attribute(0, "position")
        super().bind_attribute(1, "texture_coords")
        super().bind_attribute(2, "normal")

    def get_all_uniform_locations(self):
        """
        Collects and stores all uniform locations from the shader program.
        """
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
        """
        Loads the size of the shadow map into the shader.

        :params size: The size of the shadow map.
        """
        super().load_float(self.__location_shadow_map_size, size)

    def load_shadow_distance(self, shadow_distance: float) -> None:
        """
        Loads the shadow distance into the shader.

        :params shadow_distance: The shadow distance value.
        """
        super().load_float(self.__location_shadow_distance, shadow_distance)

    def load_to_shadow_space_matrix(self, offset: list[list], ortho_projection_matrix: list[list],
                                    light_view_matrix: list[list]) -> None:
        """
        Loads the matrices required for shadow space transformation.

        :params offset: The offset matrix.
        :params ortho_projection_matrix: The orthogonal projection matrix.
        :params light_view_matrix: The light view matrix.
        """
        super().load_matrix(self.__location_offset, offset)
        super().load_matrix(self.__location_ortho_projection_matrix, ortho_projection_matrix)
        super().load_matrix(self.__location_light_view_matrix, light_view_matrix)

    def load_clip_plane(self, plane: list[float]):
        """
        Loads the clipping plane into the shader.

        :params plane: The clipping plane.
        """
        super().load_4d_vector(self.__location_plane, plane)

    def connect_texture_units(self):
        """
        Connects the texture units to the shader.
        """
        super().load_int(self.__location_background_texture, 0)
        super().load_int(self.__location_r_texture, 1)
        super().load_int(self.__location_g_texture, 2)
        super().load_int(self.__location_b_texture, 3)
        super().load_int(self.__location_blend_map, 4)
        super().load_int(self.__location_shadow_map, 5)

    def load_fog_density(self, density: float):
        """
        Loads the fog density into the shader.

        :params density: The density of the fog.
        """
        super().load_float(self.__location_fog_density, density)

    def load_fog_gradient(self, gradient: float):
        """
        Loads the fog gradient into the shader.

        :params gradient: The gradient of the fog.
        """
        super().load_float(self.__location_fog_gradient, gradient)

    def load_sky_color(self, r: float, g: float, b: float):
        """
        Loads the sky color into the shader.

        :params r: The red component of the sky color.
        :params g: The green component of the sky color.
        :params b: The blue component of the sky color.
        """
        super().load_vector(self.__location_sky_color, [r, g, b])

    def load_shine_variables(self, damper: float, reflectivity: float):
        """
        Loads the shine variables into the shader.

        :params damper: The shine damper value.
        :params reflectivity: The reflectivity value.
        """
        super().load_float(self.__location_shine_damper, damper)
        super().load_float(self.__location_reflectivity, reflectivity)

    def load_transformation_matrix(self, matrix: list[list]):
        """
        Loads the transformation matrix into the shader.

        :params matrix: The transformation matrix.
        """
        super().load_matrix(self.__location_transformation_matrix, matrix)

    def load_projection_matrix(self, projection: list[list]):
        """
        Loads the projection matrix into the shader.

        :params projection: The projection matrix.
        """
        super().load_matrix(self.__location_projection_matrix, projection)

    def load_view_matrix(self, camera):
        """
        Loads the view matrix into the shader based on the camera's position.

        :params camera: The camera object.
        """
        view_matrix = Maths.create_view_matrix(camera)
        super().load_matrix(self.__location_view_matrix, view_matrix)

    def load_lights(self, lights: list):
        """
        Loads lights into the shader for rendering.

        :params lights: A list of light objects.
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
    def get_vertex_file(cls):
        """
        Returns the path to the vertex shader file.

        :return: The vertex shader file path.
        """
        return cls.__VERTEX_FILE

    @classmethod
    def get_fragment_file(cls):
        """
        Returns the path to the fragment shader file.

        :return: The fragment shader file path.
        """
        return cls.__FRAGMENT_FILE
