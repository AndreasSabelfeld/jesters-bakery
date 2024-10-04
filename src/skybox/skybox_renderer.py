from OpenGL.GL import *
from .skybox_shader import SkyboxShader
from src.render_engine.time import Time


class SkyboxRenderer:
    """
    Handles the rendering of a skybox in a 3D environment, using a day-night cycle.
    """

    __SIZE = 500
    __VERTICES = [
        -__SIZE, __SIZE, -__SIZE,
        -__SIZE, -__SIZE, -__SIZE,
        __SIZE, -__SIZE, -__SIZE,
        __SIZE, -__SIZE, -__SIZE,
        __SIZE, __SIZE, -__SIZE,
        -__SIZE, __SIZE, -__SIZE,

        -__SIZE, -__SIZE, __SIZE,
        -__SIZE, -__SIZE, -__SIZE,
        -__SIZE, __SIZE, -__SIZE,
        -__SIZE, __SIZE, -__SIZE,
        -__SIZE, __SIZE, __SIZE,
        -__SIZE, -__SIZE, __SIZE,

        __SIZE, -__SIZE, -__SIZE,
        __SIZE, -__SIZE, __SIZE,
        __SIZE, __SIZE, __SIZE,
        __SIZE, __SIZE, __SIZE,
        __SIZE, __SIZE, -__SIZE,
        __SIZE, -__SIZE, -__SIZE,

        -__SIZE, -__SIZE, __SIZE,
        -__SIZE, __SIZE, __SIZE,
        __SIZE, __SIZE, __SIZE,
        __SIZE, __SIZE, __SIZE,
        __SIZE, -__SIZE, __SIZE,
        -__SIZE, -__SIZE, __SIZE,

        -__SIZE, __SIZE, -__SIZE,
        __SIZE, __SIZE, -__SIZE,
        __SIZE, __SIZE, __SIZE,
        __SIZE, __SIZE, __SIZE,
        -__SIZE, __SIZE, __SIZE,
        -__SIZE, __SIZE, -__SIZE,

        -__SIZE, -__SIZE, -__SIZE,
        -__SIZE, -__SIZE, __SIZE,
        __SIZE, -__SIZE, -__SIZE,
        __SIZE, -__SIZE, -__SIZE,
        -__SIZE, -__SIZE, __SIZE,
        __SIZE, -__SIZE, __SIZE
    ]

    __DAY_TEXTURE_FILES = ["pngs/skybox/dayRight", "pngs/skybox/dayLeft", "pngs/skybox/dayTop",
                           "pngs/skybox/dayBottom", "pngs/skybox/dayBack", "pngs/skybox/dayFront"]
    __NIGHT_TEXTURE_FILES = ["pngs/skybox/nightRight", "pngs/skybox/nightLeft", "pngs/skybox/nightTop",
                             "pngs/skybox/nightBottom", "pngs/skybox/nightBack", "pngs/skybox/nightFront"]

    def __init__(self, loader, projection_matrix: list[list]):
        """
        Initializes the skybox renderer by loading cube maps and setting up the shader.

        :params loader: The loader to handle VAO and textures.
        :params projection_matrix: The projection matrix for the skybox.
        """
        self.__cube = loader.load_gui_to_vao(self.__VERTICES, 3)
        self.__day_texture = loader.load_cube_map(self.__DAY_TEXTURE_FILES)
        self.__night_texture = loader.load_cube_map(self.__NIGHT_TEXTURE_FILES)
        self.__shader = SkyboxShader()
        self.__shader.start()
        self.__shader.connect_texture_units()
        self.__shader.load_projection_matrix(projection_matrix)
        self.__shader.stop()

        self.__time = 0

    def render(self, camera, r: float, g: float, b: float) -> None:
        """
        Renders the skybox using the current camera view and fog color.

        :params camera: The camera used for rendering the skybox.
        :params r: The r component of the fog color.
        :params g: The g component of the fog color.
        :params b: The b component of the fog color.
        """
        self.__shader.start()
        self.__shader.load_view_matrix(camera)
        self.__shader.load_fog_color(r, g, b)
        glBindVertexArray(self.__cube.get_vao_id())
        glEnableVertexAttribArray(0)
        self.bind_textures(*self.day_night_cycle())
        glDrawArrays(GL_TRIANGLES, 0, self.__cube.get_vertex_count())
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        self.__shader.stop()

    def bind_textures(self, tex_1, tex_2, blend_factor: float) -> None:
        """
        Binds the day and night textures and sets the blend factor.

        :params tex_1: The first texture to bind.
        :params tex_2: The second texture to bind.
        :params blend_factor: The blend factor between the two textures.
        """
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex_1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, tex_2)
        self.__shader.load_blend_factor(blend_factor)

    def day_night_cycle(self) -> tuple:
        """
        Calculates the current time in the day-night cycle and returns the textures and blend factor.

        :return: A tuple containing the two textures and the blend factor.
        """
        self.__time += Time.get_delta_time() * 1000
        self.__time %= 24000  # 24-minute long days

        if 0 <= self.__time < 5000:
            tex_1 = self.__night_texture
            tex_2 = self.__night_texture
            blend_factor = (self.__time - 0) / (5000 - 0)
        elif 5000 <= self.__time < 8000:
            tex_1 = self.__night_texture
            tex_2 = self.__day_texture
            blend_factor = (self.__time - 5000) / (8000 - 5000)
        elif 8000 <= self.__time < 21000:
            tex_1 = self.__day_texture
            tex_2 = self.__day_texture
            blend_factor = (self.__time - 8000) / (21000 - 8000)
        else:
            tex_1 = self.__day_texture
            tex_2 = self.__night_texture
            blend_factor = (self.__time - 21000) / (24000 - 21000)

        return tex_1, tex_2, blend_factor
