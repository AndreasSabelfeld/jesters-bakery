
class TextureData:
    """
    Class representing texture data.
    """

    def __init__(self, byte_data, width: int, height: int):
        """
        Initializes a new TextureData instance.

        :params byte_data: The byte data of the texture.
        :params width: The width of the texture.
        :params height: The height of the texture.
        """
        self.__byte_data = byte_data
        self.__width = width
        self.__height = height

    def get_byte_data(self):
        """
        Returns the byte data of the texture.

        :return: The byte data.
        """
        return self.__byte_data

    def get_width(self):
        """
        Returns the width of the texture.

        :return: The width.
        """
        return self.__width

    def get_height(self):
        """
        Returns the height of the texture.

        :return: The height.
        """
        return self.__height
