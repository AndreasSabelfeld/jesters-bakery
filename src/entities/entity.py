from src.models.textured_model import TexturedModel
from src.toolbox.maths import Maths


class Entity:
    """
    Class for creating an entity (instance) of a textured model object with a position, rotation and scale
    """
    def __init__(self, model: TexturedModel, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float, texture_index: int = 0):
        """
        Initializes the entity with a model, position, rotation, scale, and an optional texture index.

        :param model: The textured model connected with the entity.
        :param position: The position of the entity.
        :param rot_x: The rotation around the x-axis.
        :param rot_y: The rotation around the y-axis.
        :param rot_z: The rotation around the z-axis.
        :param scale: The scale of the entity.
        :param texture_index: The index of the texture in the texture atlas (default is 0).
        """
        self.__model = model
        self.__position = position
        self.__rot_x = rot_x
        self.__rot_y = rot_y
        self.__rot_z = rot_z
        self.__scale = scale
        self.__texture_index = texture_index    # default there is only 1 texture in the texture atlas

    def increase_position(self, dx: float, dy: float, dz: float) -> None:
        """
        Increases the position of the entity by specified amounts.

        :param dx: Amount to increase the x position.
        :param dy: Amount to increase the y position.
        :param dz: Amount to increase the z position.
        """
        self.set_position([self.get_position()[0] + dx,
                           self.get_position()[1] + dy,
                           self.get_position()[2] + dz])

    def increase_rotation(self, dx: float, dy: float, dz: float) -> None:
        """
        Increases the rotation of the entity by specified amounts.

        :param dx: Amount to increase the rotation around the x-axis.
        :param dy: Amount to increase the rotation around the y-axis.
        :param dz: Amount to increase the rotation around the z-axis.
        """
        self.set_rot_x(self.get_rot_x() + dx)
        self.set_rot_y(self.get_rot_y() + dy)
        self.set_rot_z(self.get_rot_z() + dz)

    def get_texture_x_offset(self) -> float:
        """
        Calculates the x offset for the texture based on the texture index.

        :return: The x offset of the texture.
        """
        column = int(self.get_texture_index() % self.get_model().get_texture().get_number_of_rows())
        return column / self.get_model().get_texture().get_number_of_rows()

    def get_texture_y_offset(self) -> float:
        """
        Calculates the y offset for the texture based on the texture index.

        :return: The y offset of the texture.
        """
        row = int(self.get_texture_index() / self.get_model().get_texture().get_number_of_rows())
        return row / self.get_model().get_texture().get_number_of_rows()

    def get_transformation_matrix(self) -> list[list]:
        """Generates the transformation matrix for the entity.

        :return: The transformation matrix of the entity.
        """
        return Maths.create_transformation_matrix(self.get_position(), self.get_rot_x(), self.get_rot_y(),
                                                  self.get_rot_z(), self.get_scale())

    def get_model(self) -> TexturedModel:
        """Gets the model of the entity.

        :return: The textured model connected with the entity.
        """
        return self.__model

    def set_model(self, model: TexturedModel) -> None:
        """Sets the model of the entity.

        :param model: The new model for the entity.
        """
        self.__model = model

    def get_position(self) -> list[float]:
        """Gets the current position of the entity.

        :return: The position of the entity.
        """
        return self.__position

    def set_position(self, vector: list[float]) -> None:
        """Sets the position of the entity.

        :param vector: The new position for the entity.
        """
        self.__position = vector

    def get_rot_x(self) -> float:
        """Gets the current rotation around the x-axis.

        :return: The rotation around the x-axis.
        """
        return self.__rot_x

    def set_rot_x(self, value: float) -> None:
        """Sets the rotation around the x-axis.

        :param value: The new rotation around the x-axis.
        """
        self.__rot_x = value

    def get_rot_y(self) -> float:
        """Gets the current rotation around the y-axis.

        :return: The rotation around the y-axis.
        """
        return self.__rot_y

    def set_rot_y(self, value: float) -> None:
        """Sets the rotation around the y-axis.

        :param value: The new rotation around the y-axis.
        """
        self.__rot_y = value

    def get_rot_z(self) -> float:
        """Gets the current rotation around the z-axis.

        :return: The rotation around the z-axis.
        """
        return self.__rot_z

    def set_rot_z(self, value: float) -> None:
        """Sets the rotation around the z-axis.

        :param value: The new rotation around the z-axis.
        """
        self.__rot_z = value

    def get_scale(self) -> float:
        """Gets the current scale of the entity.

        :return: The scale of the entity.
        """
        return self.__scale

    def set_scale(self, value: float) -> None:
        """Sets the scale of the entity.

        :param value: The new scale for the entity.
        """
        self.__scale = value

    def set_texture_index(self, index: int) -> None:
        """Sets the texture index for the entity.

        :param index: The new texture index.
        """
        self.__texture_index = index

    def get_texture_index(self) -> int:
        """Gets the current texture index of the entity.

        :return: The texture index of the entity.
        """
        return self.__texture_index
