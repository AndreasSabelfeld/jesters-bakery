from .maths import Maths
from src.render_engine.input_controller import KeyboardInput
from src.render_engine.display_manager import DisplayManager
from src.terrain.terrain import Terrain
from src.collision.detection import Detection
from src.collision.utility import convert_to_ellipsoid_space, convert_to_r3_space
from src.pycgtypes import vec3
from math import sqrt


class Raycaster:
    """Class calculating a ray from the position of the mouse into the world"""
    def __init__(self, camera, projection_matrix: list[list]):
        self.__camera = camera
        self.__projection_matrix = projection_matrix
        self.__view_matrix = Maths.create_view_matrix(self.__camera)
        self.__current_ray = [0, 0, 0]

    def update(self, *args):
        self.__view_matrix = Maths.create_view_matrix(self.__camera)
        self.__current_ray = self.calculate_mouse_ray()

    def calculate_mouse_ray(self):
        mouse_x, mouse_y = KeyboardInput.get_mouse_pos()
        normalized_coords = self.get_normalized_device_coords(mouse_x, mouse_y)
        clip_coords = [normalized_coords[0], normalized_coords[1], 1, 1]
        eye_coords = self.to_eye_coords(clip_coords)
        world_ray = self.to_world_coords(eye_coords)
        return world_ray

    def to_world_coords(self, eye_coords: list[float]):
        inverted_view = Maths.invert_matrix(self.__view_matrix)
        ray_world = Maths.transform_matrix(inverted_view, eye_coords)
        mouse_ray = [ray_world[0], ray_world[1], ray_world[2]]
        mouse_ray = Maths.normalise(mouse_ray)
        return mouse_ray

    def to_eye_coords(self, clip_coords: list[float]):
        inverted_projection = Maths.invert_matrix(self.__projection_matrix)     # inverse matrix gets calculated correctly
        eye_coords = Maths.transform_matrix(inverted_projection, clip_coords)
        return [eye_coords[0], eye_coords[1], -1, 0]

    @staticmethod
    def get_normalized_device_coords(mouse_x, mouse_y):
        x = (2 * mouse_x) / DisplayManager.get_width() - 1
        y = (2 * mouse_y) / DisplayManager.get_height() - 1
        return [x, y]

    def get_current_ray(self):
        return self.__current_ray

    def get_camera(self):
        return self.__camera


class TerrainRaycaster(Raycaster):

    __RECURSION_COUNT = 200
    __RAY_RANGE = 20

    def __init__(self, camera, projection_matrix: list[list]):
        super().__init__(camera, projection_matrix)
        self.__current_terrain_point = None

    def update(self):
        super().update()
        if self.intersection_in_range(0, self.__RAY_RANGE, self.get_current_ray()):
            self.__current_terrain_point = self.binary_search(0, 0, self.__RAY_RANGE, self.get_current_ray())
        else:
            self.__current_terrain_point = None

    def get_point_on_ray(self, ray: list[float], distance: float):
        cam_pos = self.get_camera().get_position()
        start = [cam_pos[0], cam_pos[1], cam_pos[2]]
        scaled_ray = [ray[0] * distance, ray[1] * distance, ray[2] * distance]
        return [start[0] + scaled_ray[0], start[1] + scaled_ray[1], start[2] + scaled_ray[2]]

    def binary_search(self, count: int, start: float, finish: float, ray: list[float]):
        half = start + ((finish - start) / 2)
        if count >= self.__RECURSION_COUNT:
            end_point = self.get_point_on_ray(ray, half)
            terrain = self.get_terrain(end_point[0], end_point[2])
            if terrain is not None:
                return end_point
            else:
                return None
        if self.intersection_in_range(start, half, ray):
            return self.binary_search(count+1, start, half, ray)
        else:
            return self.binary_search(count+1, half, finish, ray)

    def intersection_in_range(self, start: float, finish: float, ray: list[float]):
        start_point = self.get_point_on_ray(ray, start)
        end_point = self.get_point_on_ray(ray, finish)
        if not self.is_under_ground(start_point) and self.is_under_ground(end_point):
            return True
        else:
            return False

    def is_under_ground(self, test_point: list[float]):
        terrain = self.get_terrain(test_point[0], test_point[2])
        height = 0
        if terrain is not None:
            height = terrain.get_height_of_terrain(test_point[0], test_point[2])
        if test_point[1] < height:
            return True
        else:
            return False

    @staticmethod
    def get_terrain(world_x: float, world_z: float):
        return Terrain.get_existing_terrains().get((world_x // Terrain.get_size(), world_z // Terrain.get_size()))

    def get_current_terrain_point(self):
        return self.__current_terrain_point


class ObjectRaycaster(Raycaster):
    __RAY_RANGE = 20

    def __init__(self, camera, projection_matrix: list[list]):
        super().__init__(camera, projection_matrix)
        self.__collision_detection = Detection(vec3(1))
        self.__current_object_point = None

    def update(self, collider_entities: list):
        super().update()
        self.__collision_detection.get_packet().r3_position = vec3(self.get_camera().get_position())
        ray = vec3(self.get_current_ray()).normalize() * self.__RAY_RANGE
        self.__collision_detection.get_packet().r3_velocity = ray

        e_space_position = convert_to_ellipsoid_space(vec3(1),
                                                      self.__collision_detection.get_packet().r3_position)
        e_space_velocity = convert_to_ellipsoid_space(vec3(1),
                                                      self.__collision_detection.get_packet().r3_velocity)

        self.__collision_detection.get_packet().velocity = e_space_velocity
        self.__collision_detection.get_packet().normalized_velocity = e_space_velocity.normalize()
        self.__collision_detection.get_packet().base_point = e_space_position
        self.__collision_detection.get_packet().found_collision = False
        self.__collision_detection.get_packet().nearest_distance = 999

        self.__sort_list(collider_entities)
        for entity in collider_entities:
            self.__collision_detection.detect_object(entity)
            if self.__collision_detection.get_packet().found_collision:
                self.__current_object_point = list(self.__collision_detection.get_packet().intersection_point)
                return entity

    def __sort_list(self, collider_entities: list) -> None:
        collider_entities.sort(key=lambda x: abs(sqrt((x.get_position()[0] - self.get_camera().get_position()[0])**2 +
                                                      (x.get_position()[1] - self.get_camera().get_position()[1])**2 +
                                                      (x.get_position()[2] - self.get_camera().get_position()[2])**2)))

    def get_current_object_point(self) -> list[float]:
        return self.__current_object_point
