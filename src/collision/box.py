from src.collision.end_point import EndPoint


class Box:
    """
    Represents an axis-aligned bounding box (AABB) with minimum and maximum points along the x, y, and z axes.
    Used for collision detection in 3D space.
    """

    def __init__(self, min_points: list[float], max_points: list[float]):
        """
        Initializes the Box with minimum and maximum points along the x, y, and z axes.

        :param min_points: List of minimum x, y, z coordinates of the box.
        :param max_points: List of maximum x, y, z coordinates of the box.
        """
        self.__min_x = EndPoint(self, min_points[0], True)
        self.__min_y = EndPoint(self, min_points[1], True)
        self.__min_z = EndPoint(self, min_points[2], True)
        self.__max_x = EndPoint(self, max_points[0], False)
        self.__max_y = EndPoint(self, max_points[1], False)
        self.__max_z = EndPoint(self, max_points[2], False)

        self.__min = [self.__min_x,   # x
                      self.__min_y,   # y
                      self.__min_z]   # z
        self.__max = [self.__max_x,
                      self.__max_y,
                      self.__max_z]

    def update(self, min_points: list[float], max_points: list[float]) -> None:
        """
        Updates the minimum and maximum points of the Box.

        :param min_points: New minimum x, y, z coordinates of the box.
        :param max_points: New maximum x, y, z coordinates of the box.
        """
        self.__min[0].value = min_points[0]
        self.__min[1].value = min_points[1]
        self.__min[2].value = min_points[2]
        self.__max[0].value = max_points[0]
        self.__max[1].value = max_points[1]
        self.__max[2].value = max_points[2]

    @staticmethod
    def calculate_points(position: list[float], size: float) -> tuple[list, list]:
        """
        Calculates the minimum and maximum points of the Box based on a position and size.

        :param position: The central position (x, y, z) of the box.
        :param size: The size of the box.
        :return: A tuple containing the list of minimum and maximum coordinates.
        """
        min_coords = [position[0] - size / 2,  # x
                      position[1],             # y
                      position[2] - size / 2]  # z
        max_coords = [position[0] + size / 2,
                      position[1] + size,
                      position[2] + size / 2]
        return min_coords, max_coords

    def get_x(self) -> tuple:
        """
        Returns the min and max EndPoints for the x-axis.

        :return: A tuple containing the min and max EndPoints for the x-axis.
        """
        return self.__min[0], self.__max[0]

    def get_y(self) -> tuple:
        """
        Returns the min and max EndPoints for the y-axis.

        :return: A tuple containing the min and max EndPoints for the y-axis.
        """
        return self.__min[1], self.__max[1]

    def get_z(self) -> tuple:
        """
        Returns the min and max EndPoints for the z-axis.

        :return: A tuple containing the min and max EndPoints for the z-axis.
        """
        return self.__min[2], self.__max[2]

    def get_min_x(self) -> EndPoint:
        """
        Returns the minimum EndPoint for the x-axis.

        :return: The minimum EndPoint for the x-axis.
        """
        return self.__min_x

    def get_min_y(self) -> EndPoint:
        """
        Returns the minimum EndPoint for the y-axis.

        :return: The minimum EndPoint for the y-axis.
        """
        return self.__min_y

    def get_min_z(self) -> EndPoint:
        """
        Returns the minimum EndPoint for the z-axis.

        :return: The minimum EndPoint for the z-axis.
        """
        return self.__min_z

    def get_max_x(self) -> EndPoint:
        """
        Returns the maximum EndPoint for the x-axis.

        :return: The maximum EndPoint for the x-axis.
        """
        return self.__max_x

    def get_max_y(self) -> EndPoint:
        """
        Returns the maximum EndPoint for the y-axis.

        :return: The maximum EndPoint for the y-axis.
        """
        return self.__max_y

    def get_max_z(self) -> EndPoint:
        """
        Returns the maximum EndPoint for the z-axis.

        :return: The maximum EndPoint for the z-axis.
        """
        return self.__max_z
