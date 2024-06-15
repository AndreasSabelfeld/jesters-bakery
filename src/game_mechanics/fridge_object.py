from src.textures.model_texture import ModelTexture


class FridgeObject:
    NORTH = 0
    EAST = 1

    def __init__(self, size: tuple[int, int],  entity, texture: ModelTexture, orientation: int = NORTH):
        self.__size = size
        self.__orientation = orientation
        self.__entity = entity
        self.__texture = texture

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def rotate(self) -> None:
        if self.__orientation:
            self.__orientation = self.NORTH
        else:
            self.__orientation = self.EAST

    def get_orientation(self) -> int:
        return self.__orientation

    def get_texture(self) -> ModelTexture:
        return self.__texture
