from src.toolbox.maths import Maths


class Vertex:

    __NO_INDEX = -1

    def __init__(self, index: int, position: list[float]):
        self.__index = index
        self.__position = position
        self.__length = len(position)
        self.__texture_index = self.__NO_INDEX
        self.__normal_index = self.__NO_INDEX
        self.__duplicate_vertex: Vertex = None

    def get_index(self) -> int:
        return self.__index

    def get_length(self) -> float:
        return self.__length

    def is_set(self) -> bool:
        return not(self.__texture_index == self.__NO_INDEX) and not(self.__normal_index == self.__NO_INDEX)

    def has_same_texture_and_normal(self, texture_index_other: int, normal_index_other: int):
        return texture_index_other == self.__texture_index and normal_index_other == self.__normal_index

    def set_texture_index(self, texture_index: int):
        self.__texture_index = texture_index

    def set_normal_index(self, normal_index: int):
        self.__normal_index = normal_index

    def get_position(self) -> list[float]:
        return self.__position

    def get_texture_index(self) -> int:
        return self.__texture_index

    def get_normal_index(self) -> int:
        return self.__normal_index

    def get_duplicate_vertex(self) -> 'Vertex':
        return self.__duplicate_vertex

    def set_duplicate_vertex(self, duplicate_vertex: 'Vertex'):
        self.__duplicate_vertex = duplicate_vertex


class VertexNM(Vertex):

    def __init__(self, index: int, position: list[float]):
        super().__init__(index, position)
        self.__tangents = []
        self.__averaged_tangent = [0, 0, 0]

    def add_tangent(self, tangent: list[float]):
        self.__tangents.append(tangent)

    def duplicate(self, new_index: int) -> 'VertexNM':
        vertex = VertexNM(new_index, self.get_position())
        vertex.__tangents = self.__tangents
        return vertex

    def average_tangents(self):
        if not self.__tangents:  # if list is empty
            return
        for tangent in self.__tangents:
            self.__averaged_tangent = [self.__averaged_tangent[0] + tangent[0],
                                       self.__averaged_tangent[1] + tangent[1],
                                       self.__averaged_tangent[2] + tangent[2]]
        self.__averaged_tangent = Maths.normalise(self.__averaged_tangent)

    def get_average_tangent(self) -> list[float]:
        return self.__averaged_tangent

