from src.shaders.shader_program import ShaderProgram
from src.toolbox.path import PATH


class GuiShader(ShaderProgram):

    __VERTEX_FILE = f"{PATH}/src/guis/guiVertexShader.glsl"
    __FRAGMENT_FILE = f"{PATH}/src/guis/guiFragmentShader.glsl"

    def __init__(self):
        self.__location_transformation_matrix = 0

        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

    def get_all_uniform_locations(self):
        self.__location_transformation_matrix = super().get_uniform_location("transformation_matrix")

    def bind_attributes(self):
        super().bind_attribute(0, "position")

    def load_transformation(self, matrix: list[list]):
        super().load_matrix(self.__location_transformation_matrix, matrix)
