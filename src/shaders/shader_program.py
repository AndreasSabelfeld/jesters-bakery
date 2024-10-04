from OpenGL.GL import *
from OpenGL.GLUT import *
from abc import abstractmethod  # for abstract methods


class ShaderProgram:
    """
    Class for loading and linking all shaders to the program.
    """

    __is_cel = False

    def __init__(self, vertex_file: str, fragment_file: str, geometry_file: str = None):
        """
        Initializes the shader program by loading and linking shaders.

        :params vertex_file: The file path to the vertex shader.
        :params fragment_file: The file path to the fragment shader.
        :params geometry_file: The file path to the geometry shader (optional).
        """
        self.__vertex_shader_id = self.load_shader(vertex_file, GL_VERTEX_SHADER)
        self.__fragment_shader_id = self.load_shader(fragment_file, GL_FRAGMENT_SHADER)
        self.__program_id = glCreateProgram()                           # create program
        glAttachShader(self.__program_id, self.__vertex_shader_id)      # attach the shader to the program
        glAttachShader(self.__program_id, self.__fragment_shader_id)    # attach the shader to the program
        self.__use_geometry_shader = False
        if geometry_file:
            self.__use_geometry_shader = True
            self.__geometry_shader_id = self.load_shader(geometry_file, GL_GEOMETRY_SHADER)
            glAttachShader(self.__program_id, self.__geometry_shader_id)
        self.bind_attributes()
        glLinkProgram(self.__program_id)                                # link the program to the shaders
        glValidateProgram(self.__program_id)                            # validate the program
        glUseProgram(self.__program_id)
        self.get_all_uniform_locations()

    @abstractmethod
    def get_all_uniform_locations(self):
        """
        Abstract method to get all uniform locations. Must be implemented by subclasses.
        """
        pass

    def get_uniform_location(self, uniform_name: str):
        """
        Gets the location of a uniform variable in the shader program.

        :params uniform_name: The name of the uniform variable.
        :return: The location of the uniform variable.
        """
        return glGetUniformLocation(self.get_program_id(), uniform_name)

    @staticmethod
    def load_int(location: int, value: int):
        """
        Loads an integer value into a uniform variable.

        :params location: The location of the uniform variable.
        :params value: The integer value to load.
        """
        glUniform1i(location, value)

    @staticmethod
    def load_float(location: int, value: float):
        """
        Loads a float value into a uniform variable.

        :params location: The location of the uniform variable.
        :params value: The float value to load.
        """
        glUniform1f(location, value)

    @staticmethod
    def load_vector(location: int, vector: list[float]):
        """
        Loads a 3D vector into a uniform variable in the specified GLSL shader.

        :params location: The location of the uniform variable.
        :params vector: The 3D vector to load.
        """
        glUniform3f(location, vector[0], vector[1], vector[2])  # x y z

    @staticmethod
    def load_4d_vector(location: int, vector: list[float]):
        """
        Loads a 4D vector into a uniform variable in the specified GLSL shader.

        :params location: The location of the uniform variable.
        :params vector: The 4D vector to load.
        """
        glUniform4f(location, vector[0], vector[1], vector[2], vector[3])  # x y z

    @staticmethod
    def load_2d_vector(location: int, vector: list[float]):
        """
        Loads a 2D vector into a uniform variable in the specified GLSL shader.

        :params location: The location of the uniform variable.
        :params vector: The 2D vector to load.
        """
        glUniform2f(location, vector[0], vector[1])             # x y

    @staticmethod
    def load_boolean(location: int, boolean: float):
        """
        Loads a boolean value into a uniform variable.

        :params location: The location of the uniform variable.
        :params boolean: The boolean value to load.
        """
        to_load = 0
        if boolean:
            to_load = 1
        glUniform1f(location, to_load)

    @staticmethod
    def load_matrix(location: int, matrix: list[list]):
        """
        Loads a matrix into a uniform variable in the specified GLSL shader.

        :params location: The location of the uniform variable.
        :params matrix: The matrix to load.
        """
        glUniformMatrix4fv(location, 1, False, matrix)

    def start(self):
        """
        Activates the shader program.
        """
        glUseProgram(self.get_program_id())

    @staticmethod
    def stop():
        """
        Deactivates the shader program.
        """
        glUseProgram(0)

    def clean_up(self):
        """
        Cleans up the shader program by detaching and deleting shaders.
        """
        self.stop()
        glDetachShader(self.get_program_id(), self.get_vertex_shader_id())
        glDetachShader(self.get_program_id(), self.get_fragment_shader_id())
        glDeleteShader(self.get_vertex_shader_id())
        glDeleteShader(self.get_fragment_shader_id())
        glDeleteProgram(self.get_program_id())

    @abstractmethod
    def bind_attributes(self):
        """
        Abstract method to bind shader attributes. Must be implemented by subclasses.
        """
        pass

    def bind_attribute(self, attribute: int, variable_name: str):
        """
        Binds an attribute variable to the shader program.

        :params attribute: The index of the attribute variable.
        :params variable_name: The name of the variable in the shader.
        """
        glBindAttribLocation(self.get_program_id(), attribute, variable_name)

    @staticmethod
    def load_shader(file: str, shader_type: int):
        """
        Loads and compiles a shader from the specified file.

        :params file: The file path to the shader.
        :params shader_type: The type of shader (vertex, fragment, geometry).
        :return: The ID of the compiled shader.
        """
        try:
            shader_file = open(file, 'r')                      # read file
            shader_source = ''.join(shader_file.readlines())   # create a continuous string
        except Exception as e:
            print(e)                                        # print exception
            raise SystemExit
        shader_id = glCreateShader(shader_type)             # create the shader
        glShaderSource(shader_id, shader_source)            # load the shader source code
        glCompileShader(shader_id)                          # compile the shader
        if glGetShaderiv(shader_id, GL_COMPILE_STATUS) == GL_FALSE:
            print(glGetShaderInfoLog(shader_id))       # print the info log if it didn't compile correctly
            error_message = "Could not compile shader."
            raise Exception(error_message)
        return shader_id

    def get_program_id(self):
        """
        Gets the ID of the shader program.

        :return: The program ID.
        """
        return self.__program_id

    def get_vertex_shader_id(self):
        """
        Gets the ID of the vertex shader.

        :return: The vertex shader ID.
        """
        return self.__vertex_shader_id

    def get_fragment_shader_id(self):
        """
        Gets the ID of the fragment shader.

        :return: The fragment shader ID.
        """
        return self.__fragment_shader_id

    def is_use_geometry_shader(self) -> bool:
        """
        Checks if the geometry shader is used.

        :return: True if geometry shader is used, False otherwise.
        """
        return self.__use_geometry_shader

    @classmethod
    def set_is_cel(cls, use_cel: bool):
        """
        Sets the cel shading flag.

        :params use_cel: Boolean value to set cel shading.
        """
        cls.__is_cel = use_cel

    @classmethod
    def get_is_cel(cls):
        """
        Returns the cel shading flag.

        :return: True if cel shading is enabled, False otherwise.
        """
        return cls.__is_cel
