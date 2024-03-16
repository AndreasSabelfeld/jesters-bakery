
class TextureData:

    def __init__(self, byte_data, width: int, height: int):
        self.__byte_data = byte_data
        self.__width = width
        self.__height = height

    def get_byte_data(self):
        return self.__byte_data

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height
