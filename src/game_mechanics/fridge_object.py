

class FridgeObject:
    NORTH = 0
    EAST = 1

    def __init__(self, size: tuple[int, int],  entity, orientation: int = NORTH):
        self.__size = size
        self.__orientation = orientation
        self.__entity = entity

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def rotate(self) -> None:
        if self.__orientation:
            self.__orientation = self.NORTH
        else:
            self.__orientation = self.EAST

    def get_orientation(self) -> int:
        return self.__orientation
