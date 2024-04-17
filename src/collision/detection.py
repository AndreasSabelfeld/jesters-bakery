from src.collision.collision_packet import CollisionPacket
from src.game_mechanics.game_object import GameObject
from src.collision.utility import convert_to_ellipsoid_space
from src.pycgtypes import vec3, mat4
from functools import lru_cache


class Detection:

    def __init__(self, ellipsoid_radius: vec3):
        self.__packet = CollisionPacket()
        self.__packet.e_radius = vec3(*ellipsoid_radius)
        self.__objects = dict()  # key: entity, value: tuple(vertices: list, position: vec3)

    def get_packet(self) -> CollisionPacket:
        return self.__packet

    def get_all_tris(self, entity) -> list[vec3]:
        if entity in self.__objects.keys():
            # cached values are used if object didn't move between the last check
            if self.__objects.get(entity)[1] == entity.get_position():
                return self.__objects.get(entity)[0]
        raw_vertices = entity.get_model().get_raw_model().get_vertices().copy()
        vertices = []
        for i in range(len(raw_vertices)//3):
            # make list of vectors and also move the vertices into world position
            transformed_vertex = mat4(*entity.get_transformation_matrix()) * vec3(raw_vertices.pop(0), raw_vertices.pop(0), raw_vertices.pop(0))
            transformed_vertex = convert_to_ellipsoid_space(self.__packet.e_radius, transformed_vertex)
            vertices.append(transformed_vertex)
        self.__objects.update({entity: (vertices, entity.get_position())})
        return vertices

    def detect_object(self, entity) -> vec3 | None:
        if isinstance(entity, GameObject):
            if entity.has_child():
                self.detect_object(entity.get_child())
            entity = entity.get_entity()
        vertices = self.get_all_tris(entity)
        indices = entity.get_model().get_raw_model().get_indices()
        for i in range(len(indices)//3):
            self.__packet.check_triangle(vertices[indices[3*i+0]],
                                         vertices[indices[3*i+1]],
                                         vertices[indices[3*i+2]])
            if self.__packet.found_collision:
                return self.__packet.intersection_point
