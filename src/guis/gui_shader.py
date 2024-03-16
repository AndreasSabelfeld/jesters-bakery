from src.shaders.shader_program import ShaderProgram
from sys import path


class GuiShader(ShaderProgram):

    __VERTEX_FILE = f"{path[0]}/src/guis/guiVertexShader.glsl"
    __FRAGMENT_FILE = f"{path[0]}/src/guis/guiFragmentShader.glsl"

    def __init__(self):
        super().__init__(self.__VERTEX_FILE, self.__FRAGMENT_FILE)

        self.__location_transformation_matrix = 0

    def get_all_uniform_locations(self):
        self.__location_transformation_matrix = super().get_uniform_location("transformation_matrix")

    def bind_attributes(self):
        super().bind_attribute(0, "position")

    def load_transformation(self, matrix: list[list]):
        super().load_matrix(self.__location_transformation_matrix, matrix)
