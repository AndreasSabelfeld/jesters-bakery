from PIL import Image
import sys
from src.render_engine.loader import Loader
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack
from src.toolbox.maths import Maths
from math import floor


class Terrain:
    __size = 800
    __vertex_count = 128
    __max_height = 40
    __MAX_PIXEL_COLOR = 255
    __existing_terrains = dict()

    def __init__(self, grid_x: float, grid_y: float, loader, texture_pack, blend_map=None, height_map: str = ""):
        self.__heights = None
        self.__x = grid_x * self.__size
        self.__z = grid_y * self.__size
        self.__existing_terrains.update({(grid_x, grid_y): self})

        self.__model = self.generate_terrain(loader, height_map)

        if blend_map is None:
            self.__texture_pack = TerrainTexturePack(TerrainTexture(texture_pack), TerrainTexture(texture_pack),
                                                     TerrainTexture(texture_pack), TerrainTexture(texture_pack))
            black = Image.new(mode="RGB", size=(2, 2), color=(0, 0, 0))
            black.save(f"{sys.path[0]}/res/black.png", 'PNG')
            self.__blend_map = TerrainTexture(Loader.load_texture("black"))
        else:
            self.__texture_pack = texture_pack
            self.__blend_map = blend_map

    def generate_terrain(self, loader, height_map: str):
        try:
            img = Image.open(f"{sys.path[0]}/res/{height_map}.png").convert('L')  # greyscale
            img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip image upside down
        except Exception as e:
            print(e)
            white = Image.new(mode="L", size=(256, 256), color=255)
            white.save(f"{sys.path[0]}/res/white.png", 'PNG')
            img = Image.open(f"{sys.path[0]}/res/white.png").convert('L')
            self.__max_height = 0
        self.__vertex_count = img.height
        self.__heights = [[0.0 for _ in range(self.__vertex_count)] for _ in range(self.__vertex_count)]
        count = self.__vertex_count ** 2
        vertices: list[float] = [0.0] * count * 3
        normals: list[float] = [0.0] * count * 3
        texture_coords: list[float] = [0.0] * count * 2
        indices: list[int] = [0] * 6 * (self.__vertex_count - 1) ** 2
        vertex_pointer = 0
        for i in range(self.__vertex_count):
            for j in range(self.__vertex_count):
                vertices[vertex_pointer*3+0] = j / (self.__vertex_count - 1) * self.__size    # process X-coordinate
                height = self.get_height(j, i, img)
                self.__heights[j][i] = height
                vertices[vertex_pointer*3+1] = height                                       # process Y-coordinate
                vertices[vertex_pointer*3+2] = i / (self.__vertex_count - 1) * self.__size    # process Z-coordinate
                normal = self.calculate_normal(j, i, img)
                normals[vertex_pointer*3+0] = normal[0]     # x
                normals[vertex_pointer*3+1] = normal[1]     # y
                normals[vertex_pointer*3+2] = normal[2]     # z
                texture_coords[vertex_pointer*2+0] = j / (self.__vertex_count - 1)
                texture_coords[vertex_pointer*2+1] = i / (self.__vertex_count - 1)
                vertex_pointer += 1
        pointer = 0
        for gz in range(self.__vertex_count - 1):
            for gx in range(self.__vertex_count - 1):
                top_left = int((gz * self.__vertex_count) + gx)
                top_right = int(top_left + 1)
                bottom_left = int(((gz+1) * self.__vertex_count) + gx)
                bottom_right = int(bottom_left + 1)

                indices[pointer] = top_left
                pointer += 1
                indices[pointer] = bottom_left
                pointer += 1
                indices[pointer] = top_right
                pointer += 1
                indices[pointer] = top_right
                pointer += 1
                indices[pointer] = bottom_left
                pointer += 1
                indices[pointer] = bottom_right
                pointer += 1
        return loader.load_to_vao(vertices, texture_coords, normals, indices)

    def get_x(self):
        return self.__x

    def get_z(self):
        return self.__z

    @classmethod
    def get_existing_terrains(cls) -> dict:
        return cls.__existing_terrains

    @classmethod
    def get_size(cls):
        return cls.__size

    def get_model(self):
        return self.__model

    def get_texture_pack(self):
        return self.__texture_pack

    def get_blend_map(self):
        return self.__blend_map

    def calculate_normal(self, x: int, z: int, image) -> list[float]:
        height_l = self.get_height(x-1, z, image)
        height_r = self.get_height(x+1, z, image)
        height_d = self.get_height(x, z-1, image)
        height_u = self.get_height(x, z+1, image)

        normal = [height_l-height_r, 2, height_d-height_u]
        return Maths.normalise(normal)

    def get_height(self, x: int, z: int, image) -> float:
        if x < 0 or x >= image.height or z < 0 or z >= image.height:
            return 0
        height = -1 * image.getpixel((x, z))            # greyscale color
        height += self.__MAX_PIXEL_COLOR / 2
        height /= self.__MAX_PIXEL_COLOR / 2
        height *= self.__max_height

        return height * -1

    def get_height_of_terrain(self, world_x, world_z) -> float:
        terrain_x = world_x - self.__x
        terrain_z = world_z - self.__z
        grid_square_size = self.__size / (len(self.__heights) - 1)
        grid_x = floor(terrain_x / grid_square_size)
        grid_z = floor(terrain_z / grid_square_size)
        if grid_x >= len(self.__heights)-1 or grid_z >= len(self.__heights)-1 or grid_x < 0 or grid_z < 0:
            return 0
        x_coord = (terrain_x % grid_square_size) / grid_square_size
        z_coord = (terrain_z % grid_square_size) / grid_square_size

        if x_coord <= (1-z_coord):
            answer = Maths.barry_centric([0, self.__heights[grid_x][grid_z], 0],
                                         [1, self.__heights[grid_x + 1][grid_z], 0],
                                         [0, self.__heights[grid_x][grid_z + 1], 1],
                                         [x_coord, z_coord])
        else:
            answer = Maths.barry_centric([1, self.__heights[grid_x + 1][grid_z], 0],
                                         [1, self.__heights[grid_x + 1][grid_z + 1], 1],
                                         [0, self.__heights[grid_x][grid_z + 1], 1],
                                         [x_coord, z_coord])
        return answer

    @classmethod
    def set_size(cls, size: float) -> None:
        """Sets the class variable 'size' to any given float value.
           (Call this method before creating a terrain)"""
        cls.__size = size
