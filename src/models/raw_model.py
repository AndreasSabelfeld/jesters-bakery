
class RawModel:
    """
    This class creates a raw model object, which saves the ID of the vao, the vertex count and the individual vertices
    """
    def __init__(self, vao_id: int, vertex_count: int, vertices: list[float] = None, indices: list[float] = None):
        self.__vao_id = vao_id
        self.__vertex_count = vertex_count
        self.__vertices = vertices
        self.__indices = indices

    def get_vao_id(self) -> int:
        return self.__vao_id

    def get_vertex_count(self) -> int:
        return self.__vertex_count

    def get_vertices(self) -> list[float]:
        if self.__vertices is not None:
            return self.__vertices
        else:
            print("No vertices given!")

    def get_indices(self) -> list[float]:
        if self.__indices is not None:
            return self.__indices
        else:
            print("No indices given!")
