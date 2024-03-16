

class Character:

    def __init__(self, id: int, x_texture_coord: float, y_texture_coord: float, x_tex_size: float, y_tex_size: float,
                 x_offset: float, y_offset: float, size_x: float, size_y: float, x_advance: float):
        self.__id = id
        self.__x_texture_coord = x_texture_coord
        self.__y_texture_coord = y_texture_coord
        self.__x_offset = x_offset
        self.__y_offset = y_offset
        self.__size_x = size_x
        self.__size_y = size_y
        self.__x_max_texture_coord = x_tex_size + x_texture_coord
        self.__y_max_texture_coord = y_tex_size + y_texture_coord
        self.__x_advance = x_advance

    def get_id(self) -> int:
        return self.__id

    def get_x_texture_coord(self) -> float:
        return self.__x_texture_coord

    def get_y_texture_coord(self) -> float:
        return self.__y_texture_coord

    def get_x_max_texture_coord(self) -> float:
        return self.__x_max_texture_coord

    def get_y_max_texture_coord(self) -> float:
        return self.__y_max_texture_coord

    def get_x_offset(self) -> float:
        return self.__x_offset

    def get_y_offset(self) -> float:
        return self.__y_offset

    def get_size_x(self) -> float:
        return self.__size_x

    def get_size_y(self) -> float:
        return self.__size_y

    def get_x_advance(self) -> float:
        return self.__x_advance
