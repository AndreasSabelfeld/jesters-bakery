from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject


class FridgeObject:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, size: tuple[int, int], orientation: int = NORTH):
        self.__size = size
        self.__orientation = orientation

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def rotate_clockwise(self) -> None:
        self.__orientation = (self.__orientation + 1) % 4

    def rotate_counter_clockwise(self) -> None:
        self.__orientation = (self.__orientation - 1) % 4
