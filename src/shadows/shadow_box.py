from math import radians, tan

from src.pycgtypes import vec4, mat4, vec3
from src.render_engine.display_manager import DisplayManager
import src.render_engine.master_renderer as master_renderer


class ShadowBox:
    """
    Represents the 3D cuboidal area of the world in which objects will cast
    shadows (basically represents the orthographic projection area for the shadow
    render pass). It is updated each frame to optimise the area, making it as
    small as possible (to allow for optimal shadow map resolution) while not
    being too small to avoid objects not having shadows when they should.
    Everything inside the cuboidal area represented by this object will be
    rendered to the shadow map in the shadow render pass. Everything outside the
    area won't be.
    """
    __OFFSET = 15
    __UP = vec4(0, 1, 0, 0)
    __FORWARD = vec4(0, 0, -1, 0)
    __SHADOW_DISTANCE = 150

    def __init__(self, light_view_matrix: mat4, camera):
        """
        Creates a new shadow box and calculates some initial values relating to
        the camera's view frustum, namely the width and height of the near plane
        and (possibly adjusted) far plane.

        :param light_view_matrix:
        basically the "view matrix" of the light. Can be used to transform a point from world space into "light" space
        (i.e. changes a point's coordinates from being in relation to the world's axis to being in terms of the light's
        local axis).

        :param camera:
        the in-game camera.
        """

        self.__light_view_matrix = light_view_matrix
        self.__cam = camera

        self.__min_x = None
        self.__max_x = None
        self.__min_y = None
        self.__max_y = None
        self.__min_z = None
        self.__max_z = None

        self.__far_height = None
        self.__far_width = None
        self.__near_height = None
        self.__near_width = None

        self.calculate_widths_and_heights()

    def update(self) -> None:
        """
        Updates the bounds of the shadow box based on the light direction and the
        camera's view frustum, to make sure that the box covers the smallest area
        possible while still ensuring that everything inside the camera's view
        (within a certain range) will cast shadows.
        :return:
        """

        rotation: mat4 = self.calculate_camera_rotation_matrix()
        forward_vector = rotation * self.__FORWARD
        forward_vector = vec3(forward_vector.x, forward_vector.y, forward_vector.z)

        to_far = forward_vector * self.__SHADOW_DISTANCE
        to_near = forward_vector * master_renderer.MasterRenderer.get_near_plane()
        center_near = to_near + vec3(self.__cam.get_position())
        center_far = to_far + vec3(self.__cam.get_position())

        points: list[vec4] = self.calculate_frustum_vertices(rotation, forward_vector, center_near, center_far)

        first = True
        for point in points:
            if first:
                self.__min_x = point.x
                self.__max_x = point.x
                self.__min_y = point.y
                self.__max_y = point.y
                self.__min_z = point.z
                self.__max_z = point.z
                first = False
                continue

            if point.x > self.__max_x:
                self.__max_x = point.x
            elif point.x < self.__min_x:
                self.__min_x = point.x

            if point.y > self.__max_y:
                self.__max_y = point.y
            elif point.y < self.__min_y:
                self.__min_y = point.y

            if point.z > self.__max_z:
                self.__max_z = point.z
            elif point.z < self.__min_z:
                self.__min_z = point.z
        self.__max_z += self.__OFFSET

    def get_center(self) -> vec3:
        """
        Calculates the center of the "view cuboid" in light space first, and then
        Converts this to world space using the inverse light's view matrix.
        :return:
        The center of the "view cuboid" in world space.
        """
        x = (self.__min_x + self.__max_x) / 2.0
        y = (self.__min_y + self.__max_y) / 2.0
        z = (self.__min_z + self.__max_z) / 2.0
        cen = vec4(x, y, z, 1)
        inverted_light = self.__light_view_matrix.inverse()
        center = inverted_light * cen
        return vec3(center.x, center.y, center.z)

    def calculate_frustum_vertices(self, rotation: mat4, forward_vector: vec3, center_near: vec3,
                                   center_far: vec3) -> list[vec4]:
        """
        Calculates the position of the vertex at each corner of the view frustum
        in light space (8 vertices in total, so this returns 8 positions).
        :param rotation: camera's rotation.
        :param forward_vector: the direction that the camera is aiming, and thus the direction of the frustum.
        :param center_near: the center point of the frustum's near plane.
        :param center_far: the center point of the frustum's (possibly adjusted) far plane.
        :return: The positions of the vertices of the frustum in light space.
        """
        up_vector = rotation * self.__UP
        up_vector = vec3(up_vector.x, up_vector.y, up_vector.z)
        right_vector = forward_vector.cross(up_vector)
        down_vector = -up_vector
        left_vector = -right_vector
        far_top = center_far + up_vector * self.__far_height
        far_bottom = center_far + down_vector * self.__far_height
        near_top = center_near + up_vector * self.__near_height
        near_bottom = center_near + down_vector * self.__near_height
        points = [vec4()] * 8
        points[0] = self.calculate_light_space_frustum_corner(far_top, right_vector, self.__far_width)
        points[1] = self.calculate_light_space_frustum_corner(far_top, left_vector, self.__far_width)
        points[2] = self.calculate_light_space_frustum_corner(far_bottom, right_vector, self.__far_width)
        points[3] = self.calculate_light_space_frustum_corner(far_bottom, left_vector, self.__far_width)
        points[4] = self.calculate_light_space_frustum_corner(near_top, right_vector, self.__near_width)
        points[5] = self.calculate_light_space_frustum_corner(near_top, left_vector, self.__near_width)
        points[6] = self.calculate_light_space_frustum_corner(near_bottom, right_vector, self.__near_width)
        points[7] = self.calculate_light_space_frustum_corner(near_bottom, left_vector, self.__near_width)
        return points

    def calculate_light_space_frustum_corner(self, start_point: vec3, direction: vec3, width: float) -> vec4:
        """
        Calculates one of the corner vertices of the view frustum in world space
        and converts it to light space.
        :param start_point: the starting center point on the view frustum.
        :param direction: the direction of the corner from the start point.
        :param width: the distance of the corner from the start point.
        :return: The relevant corner vertex of the view frustum in light space.
        """
        point = start_point + (direction * width)
        point4f = vec4(point.x, point.y, point.z, 1)
        point4f = self.__light_view_matrix * point4f
        return point4f

    def calculate_camera_rotation_matrix(self) -> mat4:
        """
        :return: The rotation of the camera represented as a matrix.
        """
        rotation = mat4(1)
        rotation = rotation.rotate(radians(-self.__cam.get_yaw()), vec3(0, 1, 0))
        rotation = rotation.rotate(radians(-self.__cam.get_pitch()), vec3(1, 0, 0))
        return rotation

    def calculate_widths_and_heights(self) -> None:
        """
        Calculates the width and height of the near and far planes of the
        camera's view frustum. However, this doesn't have to use the "actual" far
        plane of the view frustum. It can use a shortened view frustum if desired
        by bringing the far-plane closer, which would increase shadow resolution
        but means that distant objects wouldn't cast shadows.
        :return:
        """
        # to prevent circular import
        fov = master_renderer.MasterRenderer.get_fov()
        near_plane = master_renderer.MasterRenderer.get_near_plane()

        self.__far_width = self.__SHADOW_DISTANCE * tan(radians(fov))
        self.__near_width = near_plane * tan(radians(fov))
        self.__far_height = self.__far_width / self.get_aspect_ratio()
        self.__near_height = self.__near_width / self.get_aspect_ratio()

    @staticmethod
    def get_aspect_ratio() -> float:
        """
        :return: The aspect ratio of the display (width:height ratio).
        """
        return DisplayManager.get_width() / DisplayManager.get_height()

    def get_width(self) -> float:
        """
        :return: The width of the "view cuboid" (orthographic projection area).
        """
        return self.__max_x - self.__min_x

    def get_height(self) -> float:
        """
        :return: The height of the "view cuboid" (orthographic projection area).
        """
        return self.__max_y - self.__min_y

    def get_length(self) -> float:
        """
        :return: The length of the "view cuboid" (orthographic projection area).
        """
        return self.__max_z - self.__min_z

    def get_min_x(self) -> float:
        return self.__min_x

    def get_max_x(self) -> float:
        return self.__max_x

    def get_min_y(self) -> float:
        return self.__min_y

    def get_max_y(self) -> float:
        return self.__max_y

    def get_min_z(self) -> float:
        return self.__min_z

    def get_max_z(self) -> float:
        return self.__max_z

    @classmethod
    def get_shadow_distance(cls) -> float:
        return cls.__SHADOW_DISTANCE
