from src.collision.end_point import EndPoint


class Box:

    def __init__(self, min_points: list[float], max_points: list[float]):
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
        self.__min[0].value = min_points[0]
        self.__min[1].value = min_points[1]
        self.__min[2].value = min_points[2]
        self.__max[0].value = max_points[0]
        self.__max[1].value = max_points[1]
        self.__max[2].value = max_points[2]

    @staticmethod
    def calculate_points(position: list[float], size: float) -> tuple[list, list]:
        min_coords = [position[0] - size / 2,  # x
                      position[1],              # y
                      position[2] - size / 2]  # z
        max_coords = [position[0] + size / 2,
                      position[1] + size,
                      position[2] + size / 2]
        return min_coords, max_coords

    def get_x(self) -> tuple:
        return self.__min[0], self.__max[0]

    def get_y(self) -> tuple:
        return self.__min[1], self.__max[1]

    def get_z(self) -> tuple:
        return self.__min[2], self.__max[2]

    def get_min_x(self) -> EndPoint:
        return self.__min_x

    def get_min_y(self) -> EndPoint:
        return self.__min_y

    def get_min_z(self) -> EndPoint:
        return self.__min_z

    def get_max_x(self) -> EndPoint:
        return self.__max_x

    def get_max_y(self) -> EndPoint:
        return self.__max_y

    def get_max_z(self) -> EndPoint:
        return self.__max_z
