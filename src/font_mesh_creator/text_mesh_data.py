class TextMeshData:
    """
    Represents the data for a text mesh, including vertex positions and texture coordinates
    """

    def __init__(self, vertex_positions: list[float], texture_coords: list[float]):
        """
        Initializes the TextMeshData with the provided vertex positions and texture coordinates.

        :param vertex_positions: A list of vertex positions for the text mesh.
        :param texture_coords: A list of texture coordinates for the text mesh.
        """
        self.__vertex_positions = vertex_positions
        self.__texture_coords = texture_coords

    def get_vertex_positions(self) -> list[float]:
        """
        Gets the vertex positions of the text mesh.

        :return: A list of vertex positions.
        """
        return self.__vertex_positions

    def get_texture_coords(self) -> list[float]:
        """
        returns the texture coordinates of the text mesh.

        :return: A list of texture coordinates.
        """
        return self.__texture_coords

    def get_vertex_count(self) -> int:
        """
        Returns the number of vertices in the text mesh.

        :return: The count of vertex positions divided by 2 (since each vertex has x and y coordinates).
        """
        return len(self.__vertex_positions) // 2
