from src.textures.model_texture import ModelTexture


class FridgeObject:
    NORTH = 0
    EAST = 1

    def __init__(self, size: tuple[int, int], entity, texture: ModelTexture, content: str | list, orientation: int = NORTH):
        """
        Initializes a FridgeObject with a size, entity, texture, content, and orientation.

        :param size: The size of the fridge object as a tuple (width, height).
        :param entity: The entity connected with this fridge object.
        :param texture: The texture applied to the fridge object.
        :param content: The content stored within the fridge object, represented as a string or a list.
        :param orientation: The initial orientation of the object, defaulting to NORTH.
        """
        self.__size = size
        self.__orientation = orientation
        self.__entity = entity
        self.__texture = texture
        self.__content = content

    def get_size(self) -> tuple[int, int]:
        """
        Returns the size of the fridge object as a tuple of width and height.
        """
        return self.__size

    def rotate(self) -> None:
        """
        Rotates the fridge object between the NORTH and EAST orientations.
        """
        if self.__orientation:
            self.__orientation = self.NORTH
        else:
            self.__orientation = self.EAST

    def get_orientation(self) -> int:
        """
        Returns the current orientation of the fridge object.
        """
        return self.__orientation

    def get_texture(self) -> ModelTexture:
        """
        Returns the texture applied to the fridge object.
        """
        return self.__texture

    def get_content(self) -> str:
        """
        Returns the content stored within the fridge object.
        """
        return self.__content
