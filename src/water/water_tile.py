

class WaterTile:
    __tile_size = 60

    def __init__(self, center_x: float, center_z: float, height: float, size: float = 60):
        self.__x = center_x
        self.__z = center_z
        self.__height = height
        WaterTile.__tile_size = size

    def get_height(self):
        return self.__height

    def get_x(self):
        return self.__x

    def get_z(self):
        return self.__z

    @classmethod
    def get_tile_size(cls):
        return cls.__tile_size
