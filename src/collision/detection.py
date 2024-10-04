from src.collision.collision_packet import CollisionPacket
from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.collision.utility import convert_to_ellipsoid_space
from src.pycgtypes import vec3, mat4


class Detection:
    """
    The Detection class is responsible for detecting collisions between objects and the player.
    """

    def __init__(self, ellipsoid_radius: vec3):
        """
        Initializes a Detection object.

        :param ellipsoid_radius: The radius of the ellipsoid used for collision detection.
        """
        self.__packet = CollisionPacket()
        self.__packet.e_radius = vec3(*ellipsoid_radius)
        self.__objects = dict()  # key: entity, value: tuple(vertices: list, position: vec3)
        self.__detected_entity = None

    def get_packet(self) -> CollisionPacket:
        """
        Returns the CollisionPacket used for collision detection.

        :return: CollisionPacket instance.
        """
        return self.__packet

    def get_all_tris(self, entity) -> list[vec3]:
        """
        Gets all triangles from the vertices of given entity.

        :param entity: The entity whose triangles are to be retrieved.
        :return: A list of vec3 vertices of the triangles of the entity.
        """
        # Check if entity's position has not changed, and return cached vertices
        if entity in self.__objects.keys():
            # cached values are used if object didn't move between the last check
            if self.__objects.get(entity)[1] == entity.get_position():
                return self.__objects.get(entity)[0]

        # Otherwise, compute the vertices from the model and transform them into world space
        raw_vertices = entity.get_model().get_raw_model().get_vertices().copy()
        vertices = []
        for i in range(len(raw_vertices)//3):
            # make list of vectors and also move the vertices into world position
            transformed_vertex = mat4(*entity.get_transformation_matrix()) * vec3(raw_vertices.pop(0), raw_vertices.pop(0), raw_vertices.pop(0))
            transformed_vertex = convert_to_ellipsoid_space(self.__packet.e_radius, transformed_vertex)
            vertices.append(transformed_vertex)

        # Cache the computed vertices for this entity
        self.__objects.update({entity: (vertices, entity.get_position())})
        return vertices

    def detect_object(self, entity) -> vec3 | None:
        """
        Checks if a collision occurs between the current entity and another entity.

        :param entity: The entity or object to check for collisions with the current player entity.
        :return: The point of collision (vec3) if a collision is detected, or None if no collision occurs.
        """
        if isinstance(entity, GameObject):
            # use entity collider instead of the normal model
            entity_collider = entity.get_collider()
            if not entity_collider:
                # if no collider is specified, skip this entity
                return
            vertices = self.get_all_tris(entity_collider)
            indices = entity_collider.get_model().get_raw_model().get_indices()

        else:
            vertices = self.get_all_tris(entity)
            indices = entity.get_model().get_raw_model().get_indices()

        for i in range(len(indices)//3):
            self.__packet.check_triangle(vertices[indices[3*i+0]],
                                         vertices[indices[3*i+1]],
                                         vertices[indices[3*i+2]])
            if self.__packet.found_collision:
                self.__detected_entity = entity
                return self.__packet.intersection_point

    def get_detected_entity(self) -> GameObject | Entity:
        """
        Returns the entity that was detected during the collision check.

        :return: The entity that was in a collision, or None if no collision was detected.
        """
        return self.__detected_entity
