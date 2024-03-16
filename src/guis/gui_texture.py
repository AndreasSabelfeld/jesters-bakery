
class GuiTexture:
    """2D texture that will appear orthographically on the screen. Is rendered on top of everything"""

    def __init__(self, texture: int, position: list[float], scale: list[float]):
        """
        Create a new texture instance

        :param texture: Texture ID of type int (get one via the loader.load_texture())
        :param position: 2D position on the screen [-1;1] (center of the screen is [0, 0])
        :param scale: Scale of the texture
        """
        self.__texture = texture
        self.__position = position
        self.__scale = scale

    def get_texture(self) -> int:
        return self.__texture

    def get_position(self) -> list[float]:
        return self.__position

    def set_position(self, pos: list[float]):
        self.__position = pos

    def get_scale(self) -> list[float]:
        return self.__scale

