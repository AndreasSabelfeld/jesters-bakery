from src.pycgtypes import vec3, vec4, mat4
import math


class Maths:
    """
    Class for computing all the needed maths
    """

    @staticmethod
    def create_transformation_matrix(translation: list[float], rx: float, ry: float, rz: float, scale: float):
        """
        Creates a transformation matrix based on translation, rotation, and scale.

        :params translation: The translation vector.
        :params rx: Rotation angle around the x-axis.
        :params ry: Rotation angle around the y-axis.
        :params rz: Rotation angle around the z-axis.
        :params scale: Scaling factor.
        :return: The transformation matrix.
        """
        matrix = mat4(1.0)
        matrix = matrix.translate(vec3(translation))              # apply translation (position changes)
        if rx > 0: matrix = matrix.rotate(math.radians(rx), vec3(rx, ry, rz))   # apply rotation along the x-axis
        elif rx < 0: matrix.rotate(-math.radians(rx), vec3(rx, ry, rz))   # apply rotation along the x-axis
        if ry > 0: matrix = matrix.rotate(math.radians(ry), vec3(rx, ry, rz))   # apply rotation along the y-axis
        elif ry < 0: matrix.rotate(-math.radians(ry), vec3(rx, ry, rz))  # apply rotation along the x-axis
        if rz > 0: matrix = matrix.rotate(math.radians(rz), vec3(rx, ry, rz))   # apply rotation along the z-axis
        elif rz < 0: matrix.rotate(-math.radians(rz), vec3(rx, ry, rz))  # apply rotation along the x-axis
        matrix = matrix.scale(vec3(scale, scale, scale))          # apply scaling
        return list(matrix)                                       # list so OpenGL can use the values

    @staticmethod
    def create_2d_transformation_matrix(translation: list[float], scale: list[float]):
        """
        Creates a 2D transformation matrix based on translation and scale.

        :params translation: The translation vector.
        :params scale: The scaling vector.
        :return: The 2D transformation matrix.
        """
        matrix = mat4(1.0)
        matrix = matrix.translate(vec3(translation))
        matrix = matrix.scale(vec3(scale[0], scale[1], 1))
        return list(matrix)

    @staticmethod
    def create_view_matrix(camera):
        """
        Creates a view matrix based on the camera's position and orientation.

        :params camera: The camera object.
        :return: The view matrix.
        """
        view_matrix = mat4(1.0)
        view_matrix = view_matrix.rotate(math.radians(camera.get_pitch()), vec3([1, 0, 0]))
        view_matrix = view_matrix.rotate(math.radians(camera.get_yaw()), vec3([0, 1, 0]))
        view_matrix = view_matrix.rotate(math.radians(camera.get_roll()), vec3([0, 0, 1]))
        camera_pos = camera.get_position()
        negative_camera_pos = [-camera_pos[0], -camera_pos[1], -camera_pos[2]]
        view_matrix = view_matrix.translate(vec3(negative_camera_pos))
        return list(view_matrix)                                  # list so OpenGL can use the values

    @staticmethod
    def normalise(vector: list[float]):
        """
        Normalizes a 3D vector.

        :params vector: The vector to normalize.
        :return: The normalized vector.
        """
        vector_magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
        return [vector[0] / vector_magnitude, vector[1] / vector_magnitude, vector[2] / vector_magnitude]

    @staticmethod
    def barry_centric(p1: list[float], p2: list[float], p3: list[float], pos: list[float]):
        """
        Computes barycentric coordinates and interpolates value.

        :params p1: First point.
        :params p2: Second point.
        :params p3: Third point.
        :params pos: The position to evaluate.
        :return: Interpolated value.
        """
        det = (p2[2] - p3[2]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[2] - p3[2])
        l1 = (p2[2] - p3[2]) * (pos[0] - p3[0]) + (p3[0] - p2[0]) * (pos[1] - p3[2]) / det
        l2 = (p3[2] - p1[2]) * (pos[0] - p3[0]) + (p1[0] - p3[0]) * (pos[1] - p3[2]) / det
        l3 = 1.0 - l1 - l2
        return l1 * p1[1] + l2 * p2[1] + l3 * p3[1]

    @staticmethod
    def rotate_matrix_x_axis(matrix: list[list], angle: float):
        """
        Rotates a matrix around the x-axis.

        :params matrix: The matrix to rotate.
        :params angle: The rotation angle.
        :return: The rotated matrix.
        """
        matrix = mat4(*matrix)
        if angle > 0:
            matrix = matrix.rotate(math.radians(angle), vec3(angle, 0, 0))   # apply rotation along the x-axis
        elif angle < 0:
            matrix.rotate(-math.radians(angle), vec3(angle, 0, 0))           # apply rotation along the x-axis
        return list(matrix)

    @staticmethod
    def rotate_matrix_y_axis(matrix: list[list], angle: float):
        """
        Rotates a matrix around the y-axis.

        :params matrix: The matrix to rotate.
        :params angle: The rotation angle.
        :return: The rotated matrix.
        """
        matrix = mat4(*matrix)
        if angle > 0:
            matrix = matrix.rotate(math.radians(angle), vec3(0, angle, 0))  # apply rotation along the y-axis
        elif angle < 0:
            matrix.rotate(-math.radians(angle), vec3(0, angle, 0))          # apply rotation along the y-axis
        return list(matrix)

    @staticmethod
    def rotate_matrix_z_axis(matrix: list[list], angle: float):
        """
        Rotates a matrix around the z-axis.

        :params matrix: The matrix to rotate.
        :params angle: The rotation angle.
        :return: The rotated matrix.
        """
        matrix = mat4(*matrix)
        if angle > 0:
            matrix = matrix.rotate(math.radians(angle), vec3(0, 0, angle))  # apply rotation along the z-axis
        elif angle < 0:
            matrix.rotate(-math.radians(angle), vec3(0, 0, angle))  # apply rotation along the z-axis
        return list(matrix)

    @staticmethod
    def invert_matrix(matrix: list[list]):
        """
        Inverts a matrix.

        :params matrix: The matrix to invert.
        :return: The inverted matrix.
        """
        return list(mat4(*matrix).inverse())

    @staticmethod
    def transform_matrix(matrix: list[list], vector: list[float]):
        """
        Transforms a vector by a matrix.

        :params matrix: The matrix to transform with.
        :params vector: The vector to transform.
        :return: The transformed vector.
        """
        return list(mat4(*matrix) * vec4(vector))

    @staticmethod
    def transform_vector(vector: list[float], matrix: list[list]):
        """
        Transforms a vector by a matrix.

        :params vector: The vector to transform.
        :params matrix: The matrix to transform with.
        :return: The transformed vector.
        """
        return list(vec4(vector) * mat4(*matrix))

    @staticmethod
    def scale(matrix: list[list], vec: list[float]):
        """
        Scales a matrix by a vector.

        :params matrix: The matrix to scale.
        :params vec: The scaling vector.
        :return: The scaled matrix.
        """
        matrix = mat4(*matrix)
        vec = vec3(*vec)
        return list(matrix.scale(vec))
