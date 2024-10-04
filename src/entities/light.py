class Light:
    """
    Entity that emits light into the world
    """
    def __init__(self, position: list[float], color: list[float], attenuation: list[float] = (1, 0, 0)):
        """
        Creates a light object with a position and an RGB color.

        :param position: The position of the light in the world.
        :param color: The RGB color of the light.
        :param attenuation: The attenuation factors for the light (default is (1, 0, 0)).
        """
        self.__position = position
        self.__color = color
        self.__attenuation = attenuation

    def set_position(self, position: list[float]) -> None:
        """
        Sets the position of the light.

        :param position: The new position of the light.
        """
        self.__position = position

    def get_position(self) -> list[float]:
        """
        Gets the current position of the light.

        :return: The position of the light.
        """
        return self.__position

    def set_color(self, color: list[float]) -> None:
        """
        Sets the color of the light.

        :param color: The new RGB color of the light.
        """
        self.__color = color

    def get_color(self) -> list[float]:
        """
        Gets the current color of the light.

        :return: The RGB color of the light.
        """
        return self.__color

    def set_attenuation(self, vector: list[float]) -> None:
        """
        Sets the attenuation factors for the light.

        :param vector: The new attenuation factors for the light.
        """
        self.__attenuation = vector

    def get_attenuation(self) -> list[float]:
        """
        Gets the current attenuation factors of the light.

        :return: The attenuation factors of the light.
        """
        return self.__attenuation
