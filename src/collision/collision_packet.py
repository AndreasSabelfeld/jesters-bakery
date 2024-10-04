import ctypes

from src.collision.plane import Plane
from src.collision.utility import dot, check_point_in_triangle, get_lowest_root
from src.pycgtypes.vec3 import vec3


class CollisionPacket:
    """
    A collision detection packet used to track movement and collisions in a 3D space.
    Contains information about the moving object in 3D space and ellipsoid space.
    """

    def __init__(self):
        """
        Initializes a CollisionPacket object.
        """
        self.e_radius: vec3 = None

        # Information about the move being requested: (in R3)
        self.r3_velocity: vec3 = None
        self.r3_position: vec3 = None
        # Information about the move being requested: (in eSpace)
        self.velocity: vec3 = None
        self.normalized_velocity: vec3 = None
        self.base_point: vec3 = None
        # hit information
        self.found_collision = False
        self.nearest_distance = 999
        self.intersection_point = None

    def check_triangle(self, p1: vec3, p2: vec3, p3: vec3) -> None:
        """
        Checks for collisions between the moving object and a triangle defined by three points

        :param p1: The first point of the triangle.
        :param p2: The second point of the triangle.
        :param p3: The third point of the triangle.
        """
        triangle_plane = Plane.from_triangle(p1, p2, p3)

        if triangle_plane.is_front_facing_to(self.normalized_velocity):
            embedded_in_plane = False
            # Calculate the signed distance from sphere
            signed_distance_to_triangle_plane = triangle_plane.signed_distance_to(self.base_point)
            normal_dot_velocity = dot(triangle_plane.normal, self.velocity)

            if -0.1 < normal_dot_velocity < 0.1:
                if abs(signed_distance_to_triangle_plane) >= 1.0:
                    # sphere is not embedded in plane
                    # no collision possible
                    return
                else:
                    # sphere is embedded in plane it intersects in the whole range [0..1]
                    embedded_in_plane = True
                    t0, t1 = 0.0, 1.0
            else:
                t0 = (-1.0 - signed_distance_to_triangle_plane) / normal_dot_velocity
                t1 = ( 1.0 - signed_distance_to_triangle_plane) / normal_dot_velocity

                # swap so t0 < t1
                if t0 > t1:
                    t0, t1 = t1, t0

                if t0 > 1.0 or t1 < 0.0:
                    # both values outside
                    return

                # Clamp to [0,1]
                t0 = max(0.0, min(t0, 1.0))
                t1 = max(0.0, min(t1, 1.0))

            collision_point = vec3()
            found_collision = False
            t = 1.0

            # check for collision inside the triangle
            # doesn't work
            """if not embedded_in_plane:
                plane_intersection_point = (self.base_point - triangle_plane.normal) + t0*self.velocity

                if check_point_in_triangle(plane_intersection_point, p1, p2, p3):
                    found_collision = True
                    t = t0
                    collision_point = plane_intersection_point"""

            # if we haven’t found a collision already we’ll have to
            # sweep sphere against points and edges of the triangle.
            if not found_collision:
                # For each vertex or edge a quadratic equation have to
                # be solved. We parameterize this equation as
                # a*t^2 + b*t + c = 0 and below we calculate the
                # parameters a,b and c for each test.
                new_t = ctypes.c_float(0)
                ptr = ctypes.pointer(new_t)

                a = self.velocity.length() ** 2
                for point in (p1, p2, p3):
                    b = 2.0 * dot(self.velocity, self.base_point - point)
                    c = (point - self.base_point).length() ** 2 - 1.0
                    if get_lowest_root(a, b, c, t, ptr):
                        t = new_t.value
                        found_collision = True
                        collision_point = point

                points = (p1, p2, p3)
                for i in range(3):
                    # p2 - p1
                    # p3 - p2
                    # p1 - p3
                    edge = points[(i+1) % 3] - points[i]
                    base_to_vertex = points[i] - self.base_point
                    edge_squared_length = edge.length() ** 2
                    edge_dot_velocity = dot(edge, self.velocity)
                    edge_dot_base_to_vertex = dot(edge, base_to_vertex)

                    a = edge_squared_length * -self.velocity.length() ** 2 + edge_dot_velocity ** 2
                    b = edge_squared_length * (2 * dot(self.velocity,
                                                       base_to_vertex)) - 2.0 * edge_dot_velocity * edge_dot_base_to_vertex
                    c = edge_squared_length * (1 - base_to_vertex.length() ** 2) + edge_dot_base_to_vertex ** 2

                    # Does the swept sphere collide against infinite edge?
                    if get_lowest_root(a, b, c, t, ptr):
                        # Check if intersection is within line segment:
                        f = (edge_dot_velocity * new_t.value - edge_dot_base_to_vertex) / edge_squared_length
                        if 0.0 <= f <= 1.0:
                            #  intersection took place within segment.
                            t = new_t.value
                            found_collision = True
                            collision_point = points[i] + f * edge

            if found_collision:
                # distance to collision: ’t’ is time of collision
                dist_to_collision = t * self.velocity.length()
                # Does this triangle qualify for the closest hit?
                if not self.found_collision or dist_to_collision < self.nearest_distance:
                    self.nearest_distance = dist_to_collision
                    self.intersection_point = collision_point
                    self.found_collision = True
