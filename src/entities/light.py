
class Light:
    """
    Entity that emits light into the world
    """
    def __init__(self, position: list[float], color: list[float], attenuation: list[float] = (1, 0, 0)):
        """Creates a light object with a position and an RGB color"""
        self.__position = position
        self.__color = color
        self.__attenuation = attenuation

    def set_position(self, position: list[float]):
        self.__position = position

    def get_position(self):
        return self.__position

    def set_color(self, color: list[float]):
        self.__color = color

    def get_color(self):
        return self.__color

    def set_attenuation(self, vector: list[float]):
        self.__attenuation = vector

    def get_attenuation(self):
        return self.__attenuation
