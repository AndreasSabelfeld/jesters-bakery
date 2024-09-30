from src.models.textured_model import TexturedModel
from src.toolbox.maths import Maths


class Entity:
    """
    Class for creating an entity (instance) of a textured model object with a position, rotation and scale
    """
    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float, texture_index: int = 0):
        self.__model = model
        self.__position = position
        self.__rot_x = rot_x
        self.__rot_y = rot_y
        self.__rot_z = rot_z
        self.__scale = scale
        self.__texture_index = texture_index    # default there is only 1 texture in the texture atlas

    def increase_position(self, dx: float, dy: float, dz: float):
        self.set_position([self.get_position()[0] + dx,
                           self.get_position()[1] + dy,
                           self.get_position()[2] + dz])

    def increase_rotation(self, dx: float, dy: float, dz: float):
        self.set_rot_x(self.get_rot_x() + dx)
        self.set_rot_y(self.get_rot_y() + dy)
        self.set_rot_z(self.get_rot_z() + dz)

    def get_texture_x_offset(self):
        column = int(self.get_texture_index() % self.get_model().get_texture().get_number_of_rows())
        return column / self.get_model().get_texture().get_number_of_rows()

    def get_texture_y_offset(self):
        row = int(self.get_texture_index() / self.get_model().get_texture().get_number_of_rows())
        return row / self.get_model().get_texture().get_number_of_rows()

    def get_transformation_matrix(self) -> list[list]:
        return Maths.create_transformation_matrix(self.get_position(), self.get_rot_x(), self.get_rot_y(),
                                                  self.get_rot_z(), self.get_scale())

    def get_model(self) -> TexturedModel:
        return self.__model

    def set_model(self, model):
        self.__model = model

    def get_position(self) -> list[float]:
        return self.__position

    def set_position(self, vector):
        self.__position = vector

    def get_rot_x(self) -> float:
        return self.__rot_x

    def set_rot_x(self, value):
        self.__rot_x = value

    def get_rot_y(self) -> float:
        return self.__rot_y

    def set_rot_y(self, value):
        self.__rot_y = value

    def get_rot_z(self) -> float:
        return self.__rot_z

    def set_rot_z(self, value):
        self.__rot_z = value

    def get_scale(self) -> float:
        return self.__scale

    def set_scale(self, value):
        self.__scale = value

    def set_texture_index(self, index: int):
        self.__texture_index = index

    def get_texture_index(self) -> int:
        return self.__texture_index
