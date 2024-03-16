import sys
from src.render_engine.loader import Loader
from src.models.cube import cube_vertices, cube_texture_coords, cube_normals, cube_indices


class OBJLoader:

    def __init__(self):
        self.vertices = []
        self.textures = []
        self.normals = []
        self.indices = []

        self.vertices_array = []
        self.textures_array = []
        self.normals_array = []
        self.indices_array = []

    def load_obj_model(self, file_name: str, loader: Loader):
        try:
            obj = open(f"{sys.path[0]}/res/{file_name}.obj", 'r')
        except Exception as e:
            print(e)
            return loader.load_to_vao(cube_vertices, cube_texture_coords, cube_normals, cube_indices)
        try:
            while True:
                line = obj.readline()
                current_line = line.split(" ")
                if line.startswith("v "):
                    self.vertices.append([current_line[1], current_line[2], current_line[3]])
                elif line.startswith("vt "):
                    self.textures.append([current_line[1], current_line[2]])
                elif line.startswith("vn "):
                    self.normals.append([current_line[1], current_line[2], current_line[3]])
                elif line.startswith("f "):
                    self.textures_array = [None] * len(self.vertices)*2
                    self.normals_array = [None] * len(self.vertices)*3
                    break

            while line != '':
                if not line.startswith("f "):
                    line = obj.readline()
                    continue
                current_line = line.split(" ")
                vertex1 = current_line[1].split("/")
                vertex2 = current_line[2].split("/")
                vertex3 = current_line[3].split("/")

                if len(current_line) == 5:      # .obj is saved as rectangles instead of triangles
                    vertex4 = current_line[4].split("/")
                    self.process_vertex(vertex1, self.textures, self.normals)
                    self.process_vertex(vertex3, self.textures, self.normals)
                    self.process_vertex(vertex4, self.textures, self.normals)
                    continue

                self.process_vertex(vertex1, self.textures, self.normals)
                self.process_vertex(vertex2, self.textures, self.normals)
                self.process_vertex(vertex3, self.textures, self.normals)

                line = obj.readline()

            obj.close()

        except Exception as e:
            print(e)
            raise SystemExit

        self.vertices_array = [float(item) for sublist in self.vertices for item in sublist]
        self.indices_array = self.indices

        self.vertices = []   # clear all lists with the 'old' information
        self.textures = []
        self.normals = []
        self.indices = []
        return loader.load_to_vao(self.vertices_array, self.textures_array, self.normals_array, self.indices_array)

    def process_vertex(self, vertex_data: list[str], textures: list[list], normals: list[list]):
        current_vertex_pointer = int(vertex_data[0]) - 1
        self.indices.append(current_vertex_pointer)

        current_tex = textures[int(vertex_data[1]) - 1]

        self.textures_array[current_vertex_pointer * 2] = float(current_tex[0])
        self.textures_array[current_vertex_pointer * 2 + 1] = 1 - float(current_tex[1])

        current_norm = normals[int(vertex_data[2]) - 1]

        self.normals_array[current_vertex_pointer * 3] = float(current_norm[0])
        self.normals_array[current_vertex_pointer * 3 + 1] = float(current_norm[1])
        self.normals_array[current_vertex_pointer * 3 + 2] = float(current_norm[2])
