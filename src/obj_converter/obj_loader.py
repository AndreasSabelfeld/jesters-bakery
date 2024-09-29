from src.toolbox.path import PATH
from src.render_engine.loader import Loader
from src.models.cube import cube_vertices, cube_texture_coords, cube_normals, cube_indices
from src.obj_converter.vertex import Vertex, VertexNM


class OBJLoader:

    def __init__(self):
        self._vertices = []
        self._textures = []
        self._normals = []
        self._indices = []

        self._vertices_array = []
        self._textures_array = []
        self._normals_array = []
        self._indices_array = []

    def load_obj_model(self, file_name: str, loader: Loader):
        try:
            obj = open(f"{PATH}/res/{file_name}.obj", 'r')
        except Exception as e:
            print(e)
            return loader.load_to_vao(cube_vertices, cube_texture_coords, cube_normals, cube_indices)

        while True:
            line = obj.readline()
            current_line = line.split(" ")
            if line.startswith("v "):
                vertex = [float(current_line[1]), float(current_line[2]), float(current_line[3])]
                new_vertex = Vertex(len(self._vertices), vertex)
                self._vertices.append(new_vertex)
            elif line.startswith("vt "):
                self._textures.append([current_line[1], current_line[2]])
            elif line.startswith("vn "):
                self._normals.append([current_line[1], current_line[2], current_line[3]])
            elif line.startswith("f "):
                break
        while line != '':
            if not line.startswith("f "):
                line = obj.readline()
                continue
            current_line = line.split(" ")
            vertex1 = current_line[1].split("/")
            vertex2 = current_line[2].split("/")
            vertex3 = current_line[3].split("/")
            self.process_vertex(vertex1)
            self.process_vertex(vertex2)
            self.process_vertex(vertex3)
            line = obj.readline()
        obj.close()

        self.remove_unused_vertices(self._vertices)
        self._vertices_array = [0.0] * len(self._vertices) * 3
        self._textures_array = [0.0] * len(self._vertices) * 2
        self._normals_array = [0.0] * len(self._vertices) * 3
        self._indices_array = self._indices  # [0] * len(self._vertices) * 3
        self.convert_data_to_arrays()

        self._vertices = []   # clear all lists with the 'old' information
        self._textures = []
        self._normals = []
        self._indices = []

        return loader.load_to_vao(self._vertices_array, self._textures_array, self._normals_array, self._indices_array)

    def process_vertex(self, vertex: list[str]):
        index = int(vertex[0]) - 1
        current_vertex = self._vertices[index]
        texture_index = int(vertex[1]) - 1
        normal_index = int(vertex[2]) - 1
        if not current_vertex.is_set():
            current_vertex.set_texture_index(texture_index)
            current_vertex.set_normal_index(normal_index)
            self._indices.append(index)
        else:
            self.deal_with_already_processed_vertex(current_vertex, texture_index, normal_index)

    def convert_data_to_arrays(self):
        for i in range(len(self._vertices)):
            current_vertex = self._vertices[i]
            position = current_vertex.get_position()
            texture_coord = self._textures[current_vertex.get_texture_index()]
            normal_vector = self._normals[current_vertex.get_normal_index()]
            self._vertices_array[i * 3 + 0] = float(position[0])
            self._vertices_array[i * 3 + 1] = float(position[1])
            self._vertices_array[i * 3 + 2] = float(position[2])
            self._textures_array[i * 2 + 0] = float(texture_coord[0])
            self._textures_array[i * 2 + 1] = 1 - float(texture_coord[1])
            self._normals_array[i * 3 + 0] = float(normal_vector[0])
            self._normals_array[i * 3 + 1] = float(normal_vector[1])
            self._normals_array[i * 3 + 2] = float(normal_vector[2])

    def deal_with_already_processed_vertex(self, previous_vertex: Vertex, new_texture_index: int, new_normal_index: int):
        if previous_vertex.has_same_texture_and_normal(new_texture_index, new_normal_index):
            self._indices.append(previous_vertex.get_index())
        else:
            another_vertex = previous_vertex.get_duplicate_vertex()
            if another_vertex is not None:
                self.deal_with_already_processed_vertex(another_vertex, new_texture_index, new_normal_index)
            else:
                duplicate_vertex = Vertex(len(self._vertices), previous_vertex.get_position())
                duplicate_vertex.set_texture_index(new_texture_index)
                duplicate_vertex.set_normal_index(new_normal_index)
                previous_vertex.set_duplicate_vertex(duplicate_vertex)
                self._vertices.append(duplicate_vertex)
                self._indices.append(duplicate_vertex.get_index())

    @staticmethod
    def remove_unused_vertices(vertices: list[Vertex]):
        for vertex in vertices:
            if not vertex.is_set():
                vertex.set_texture_index(0)
                vertex.set_normal_index(0)


class NormalMappedOBJLoader(OBJLoader):

    def __init__(self):
        super().__init__()
        self._tangents_array = []

    def load_obj_model(self, file_name: str, loader: Loader):
        try:
            obj = open(f"{PATH}/res/{file_name}.obj", 'r')
        except Exception as e:
            print(e)
            return loader.load_to_vao(cube_vertices, cube_texture_coords, cube_normals, cube_indices)

        while True:
            line = obj.readline()
            current_line = line.split(" ")
            if line.startswith("v "):
                vertex = [float(current_line[1]), float(current_line[2]), float(current_line[3])]
                new_vertex = VertexNM(len(self._vertices), vertex)
                self._vertices.append(new_vertex)
            elif line.startswith("vt "):
                self._textures.append([current_line[1], current_line[2]])
            elif line.startswith("vn "):
                self._normals.append([current_line[1], current_line[2], current_line[3]])
            elif line.startswith("f "):
                break
        while line != '':
            if not line.startswith("f "):
                line = obj.readline()
                continue
            current_line = line.split(" ")
            vertex1 = current_line[1].split("/")
            vertex2 = current_line[2].split("/")
            vertex3 = current_line[3].split("/")
            v0 = self.process_vertex(vertex1)
            v1 = self.process_vertex(vertex2)
            v2 = self.process_vertex(vertex3)
            self.calculate_tangents(v0, v1, v2)
            line = obj.readline()
        obj.close()

        self.remove_unused_vertices(self._vertices)
        self._vertices_array = [0.0] * len(self._vertices) * 3
        self._textures_array = [0.0] * len(self._vertices) * 2
        self._normals_array = [0.0] * len(self._vertices) * 3
        self._tangents_array = [0.0] * len(self._vertices) * 3
        self._indices_array = self._indices
        self.convert_data_to_arrays()

        self._vertices = []   # clear all lists with the 'old' information
        self._textures = []
        self._normals = []
        self._indices = []
        return loader.load_tangents_to_vao(self._vertices_array, self._textures_array, self._normals_array,
                                           self._tangents_array, self._indices_array)

    def calculate_tangents(self, v0: VertexNM, v1: VertexNM, v2: VertexNM):
        delta_pos_1 = [v1.get_position()[0] - v0.get_position()[0],
                       v1.get_position()[1] - v0.get_position()[1],
                       v1.get_position()[2] - v0.get_position()[2]]
        delta_pos_2 = [v2.get_position()[0] - v0.get_position()[0],
                       v2.get_position()[1] - v0.get_position()[1],
                       v2.get_position()[2] - v0.get_position()[2]]
        uv0 = self._textures[v0.get_texture_index()]
        uv1 = self._textures[v1.get_texture_index()]
        uv2 = self._textures[v2.get_texture_index()]
        delta_uv_1 = [float(uv1[0]) - float(uv0[0]),
                      float(uv1[1]) - float(uv0[1])]
        delta_uv_2 = [float(uv2[0]) - float(uv0[0]),
                      float(uv2[1]) - float(uv0[1])]

        r = 1.0 / (delta_uv_1[0] * delta_uv_2[1] - delta_uv_1[1] * delta_uv_2[0])
        delta_pos_1 = [delta_pos_1[0] * delta_uv_2[1],
                       delta_pos_1[1] * delta_uv_2[1],
                       delta_pos_1[2] * delta_uv_2[1]]
        delta_pos_2 = [delta_pos_2[0] * delta_uv_1[1],
                       delta_pos_2[1] * delta_uv_1[1],
                       delta_pos_2[2] * delta_uv_1[1]]
        tangent = [delta_pos_1[0] - delta_pos_2[0],
                   delta_pos_1[1] - delta_pos_2[1],
                   delta_pos_1[2] - delta_pos_2[2]]
        tangent = [tangent[0] * r,
                   tangent[1] * r,
                   tangent[2] * r]
        v0.add_tangent(tangent)
        v1.add_tangent(tangent)
        v2.add_tangent(tangent)

    def process_vertex(self, vertex: list[str]):
        index = int(vertex[0]) - 1
        current_vertex = self._vertices[index]
        texture_index = int(vertex[1]) - 1
        normal_index = int(vertex[2]) - 1
        if not current_vertex.is_set():
            current_vertex.set_texture_index(texture_index)
            current_vertex.set_normal_index(normal_index)
            self._indices.append(index)
            return current_vertex
        else:
            return self.deal_with_already_processed_vertex(current_vertex, texture_index, normal_index)

    def convert_data_to_arrays(self):
        for i in range(len(self._vertices)):
            current_vertex = self._vertices[i]
            position = current_vertex.get_position()
            texture_coord = self._textures[current_vertex.get_texture_index()]
            normal_vector = self._normals[current_vertex.get_normal_index()]
            tangent = current_vertex.get_average_tangent()
            self._vertices_array[i * 3 + 0] = float(position[0])
            self._vertices_array[i * 3 + 1] = float(position[1])
            self._vertices_array[i * 3 + 2] = float(position[2])
            self._textures_array[i * 2 + 0] = float(texture_coord[0])
            self._textures_array[i * 2 + 1] = 1 - float(texture_coord[1])
            self._normals_array[i * 3 + 0] = float(normal_vector[0])
            self._normals_array[i * 3 + 1] = float(normal_vector[1])
            self._normals_array[i * 3 + 2] = float(normal_vector[2])
            self._tangents_array[i * 3 + 0] = float(tangent[0])
            self._tangents_array[i * 3 + 1] = float(tangent[1])
            self._tangents_array[i * 3 + 2] = float(tangent[2])

    def deal_with_already_processed_vertex(self, previous_vertex: VertexNM, new_texture_index: int, new_normal_index: int):
        if previous_vertex.has_same_texture_and_normal(new_texture_index, new_normal_index):
            self._indices.append(previous_vertex.get_index())
            return previous_vertex
        else:
            another_vertex = previous_vertex.get_duplicate_vertex()
            if another_vertex is not None:
                return self.deal_with_already_processed_vertex(another_vertex, new_texture_index, new_normal_index)
            else:
                duplicate_vertex = previous_vertex.duplicate(len(self._vertices))
                duplicate_vertex.set_texture_index(new_texture_index)
                duplicate_vertex.set_normal_index(new_normal_index)
                previous_vertex.set_duplicate_vertex(duplicate_vertex)
                self._vertices.append(duplicate_vertex)
                self._indices.append(duplicate_vertex.get_index())
                return duplicate_vertex

    @staticmethod
    def remove_unused_vertices(vertices: list[VertexNM]):
        for vertex in vertices:
            vertex.average_tangents()
            if not vertex.is_set():
                vertex.set_texture_index(0)
                vertex.set_normal_index(0)
