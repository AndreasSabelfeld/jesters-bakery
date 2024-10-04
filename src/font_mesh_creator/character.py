class Character:
    """
    Represents a character (letter) with texture coordinates and size information.
    """

    def __init__(self, id: int, x_texture_coord: float, y_texture_coord: float, x_tex_size: float, y_tex_size: float,
                 x_offset: float, y_offset: float, size_x: float, size_y: float, x_advance: float):
        """Initializes a Character instance with the given parameters.

        :param id: The ID of the character.
        :param x_texture_coord: The x texture coordinate.
        :param y_texture_coord: The y texture coordinate.
        :param x_tex_size: The width of the texture.
        :param y_tex_size: The height of the texture.
        :param x_offset: The x offset of the character.
        :param y_offset: The y offset of the character.
        :param size_x: The width of the character.
        :param size_y: The height of the character.
        :param x_advance: The x advance for character spacing.
        """
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
        """Returns the ID of the character."""
        return self.__id

    def get_x_texture_coord(self) -> float:
        """Returns the x texture coordinate of the character."""
        return self.__x_texture_coord

    def get_y_texture_coord(self) -> float:
        """Returns the y texture coordinate of the character."""
        return self.__y_texture_coord

    def get_x_max_texture_coord(self) -> float:
        """Returns the maximum x texture coordinate of the character."""
        return self.__x_max_texture_coord

    def get_y_max_texture_coord(self) -> float:
        """Returns the maximum y texture coordinate of the character."""
        return self.__y_max_texture_coord

    def get_x_offset(self) -> float:
        """Returns the x offset of the character."""
        return self.__x_offset

    def get_y_offset(self) -> float:
        """Returns the y offset of the character."""
        return self.__y_offset

    def get_size_x(self) -> float:
        """Returns the width of the character."""
        return self.__size_x

    def get_size_y(self) -> float:
        """Returns the height of the character."""
        return self.__size_y

    def get_x_advance(self) -> float:
        """Returns the x advance of the character."""
        return self.__x_advance
