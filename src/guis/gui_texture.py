
class GuiTexture:

    def __init__(self, texture: int, position: list[float], scale: list[float]):
        self.__texture = texture
        self.__position = position
        self.__scale = scale

    def get_texture(self) -> int:
        return self.__texture

    def get_position(self) -> list[float]:
        return self.__position

    def get_scale(self) -> list[float]:
        return self.__scale

