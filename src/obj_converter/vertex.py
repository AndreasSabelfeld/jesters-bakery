from src.toolbox.maths import Maths


class Vertex:

    __NO_INDEX = -1

    def __init__(self, index: int, position: list[float]):
        """
        Initialize a vertex with a index and position.

        :params index: The index of the vertex.
        :params position: The position of the vertex as a list of floats.
        """
        self.__index = index
        self.__position = position
        self.__length = len(position)
        self.__texture_index = self.__NO_INDEX
        self.__normal_index = self.__NO_INDEX
        self.__duplicate_vertex: Vertex = None

    def get_index(self) -> int:
        """
        Get the index of the vertex.

        :return: The index of the vertex.
        """
        return self.__index

    def get_length(self) -> float:
        """
        Get the length of the position list.

        :return: The length of the position list.
        """
        return self.__length

    def is_set(self) -> bool:
        """
        Check if the texture and normal indices are set.

        :return: True if both indices are set, otherwise False.
        """
        return not (self.__texture_index == self.__NO_INDEX) and not (self.__normal_index == self.__NO_INDEX)

    def has_same_texture_and_normal(self, texture_index_other: int, normal_index_other: int) -> bool:
        """
        Check if the vertex has the same texture and normal indices.

        :params texture_index_other: The texture index to compare.
        :params normal_index_other: The normal index to compare.
        :return: True if both indices match, otherwise False.
        """
        return texture_index_other == self.__texture_index and normal_index_other == self.__normal_index

    def set_texture_index(self, texture_index: int):
        """
        Set the texture index for the vertex.

        :params texture_index: The texture index to set.
        """
        self.__texture_index = texture_index

    def set_normal_index(self, normal_index: int):
        """
        Set the normal index for the vertex.

        :params normal_index: The normal index to set.
        """
        self.__normal_index = normal_index

    def get_position(self) -> list[float]:
        """
        Get the position of the vertex.

        :return: The position of the vertex as a list of floats.
        """
        return self.__position

    def get_texture_index(self) -> int:
        """
        Get the texture index of the vertex.

        :return: The texture index of the vertex.
        """
        return self.__texture_index

    def get_normal_index(self) -> int:
        """
        Get the normal index of the vertex.

        :return: The normal index of the vertex.
        """
        return self.__normal_index

    def get_duplicate_vertex(self) -> 'Vertex':
        """
        Get the duplicate vertex, if it exists.

        :return: The duplicate vertex or None.
        """
        return self.__duplicate_vertex

    def set_duplicate_vertex(self, duplicate_vertex: 'Vertex'):
        """
        Set a duplicate vertex for the current vertex.

        :params duplicate_vertex: The vertex to set as a duplicate.
        """
        self.__duplicate_vertex = duplicate_vertex


class VertexNM(Vertex):

    def __init__(self, index: int, position: list[float]):
        """
        Initialize a normal-mapped vertex with a given index and position.

        :params index: The index of the vertex.
        :params position: The position of the vertex as a list of floats.
        """
        super().__init__(index, position)
        self.__tangents = []
        self.__averaged_tangent = [0, 0, 0]

    def add_tangent(self, tangent: list[float]):
        """
        Add a tangent to the vertex.

        :params tangent: The tangent to add as a list of floats.
        """
        self.__tangents.append(tangent)

    def duplicate(self, new_index: int) -> 'VertexNM':
        """
        Create a duplicate of the vertex with a new index.

        :params new_index: The index for the duplicate vertex.
        :return: The duplicated vertex.
        """
        vertex = VertexNM(new_index, self.get_position())
        vertex.__tangents = self.__tangents
        return vertex

    def average_tangents(self):
        """
        Average the tangents of the vertex.

        :return: None
        """
        if not self.__tangents:  # if list is empty
            return
        for tangent in self.__tangents:
            self.__averaged_tangent = [self.__averaged_tangent[0] + tangent[0],
                                       self.__averaged_tangent[1] + tangent[1],
                                       self.__averaged_tangent[2] + tangent[2]]
        self.__averaged_tangent = Maths.normalise(self.__averaged_tangent)

    def get_average_tangent(self) -> list[float]:
        """
        Get the averaged tangent of the vertex.

        :return: The averaged tangent as a list of floats.
        """
        return self.__averaged_tangent

