

class TextMeshData:
    def __init__(self, vertex_positions: list[float], texture_coords: list[float]):
        self.__vertex_positions = vertex_positions
        self.__texture_coords = texture_coords

    def get_vertex_positions(self) -> list[float]:
        return self.__vertex_positions

    def get_texture_coords(self) -> list[float]:
        return self.__texture_coords

    def get_vertex_count(self) -> int:
        return len(self.__vertex_positions) // 2
