from OpenGL.GL import *
import math

from src.shadows.shadow_shader import ShadowShader
from src.shadows.shadow_box import ShadowBox
from src.shadows.shadow_frame_buffer import ShadowFrameBuffer
from src.shadows.shadow_map_entity_renderer import ShadowMapEntityRenderer
from src.pycgtypes import mat4, vec3


class ShadowMapMasterRenderer:
    """
    This class is in charge of using all the classes in the shadows package to
    carry out the shadow render pass, i.e. rendering the scene to the shadow map
    texture. This is the only class in the shadows package which needs to be
    referenced from outside the shadows package.
    """

    __SHADOW_MAP_SIZE = 2 ** 13

    def __init__(self, camera):
        """
        Creates instances of the important objects needed for rendering the scene
        to the shadow map. This includes the ShadowBox which calculates
        the position and size of the "view cuboid", the simple renderer and
        shader program that are used to render objects to the shadow map, and the
        ShadowFrameBuffer to which the scene is rendered. The size of the
        shadow map is determined here.
        :param camera: the camera being used in the scene.
        """
        self.__projection_matrix = mat4(1)
        self.__light_view_matrix = mat4(1)
        self.__offset = self.__create_offset()

        self.__shader = ShadowShader()
        self.__shadow_box = ShadowBox(self.__light_view_matrix, camera)
        self.__shadow_fbo = ShadowFrameBuffer(self.__SHADOW_MAP_SIZE, self.__SHADOW_MAP_SIZE)
        self.__entity_renderer = ShadowMapEntityRenderer(self.__shader)

    def render(self, entities: dict, sun) -> None:
        """
        Carries out the shadow render pass. This renders the entities to the
        shadow map. First the shadow box is updated to calculate the size and
        position of the "view cuboid". The light direction is assumed to be
        "-lightPosition" which will be fairly accurate assuming that the light is
        very far from the scene. It then prepares to render, renders the entities
        to the shadow map, and finishes rendering.
        :param entities:
        the lists of entities to be rendered. Each list is
        connected with the {@link TexturedModel} that all the
        entities in that list use.
        :param sun: the light acting as the sun in the scene.
        :return:
        """
        self.__shadow_box.update()
        sun_position = vec3(sun.get_position())
        light_direction = -sun_position
        self.prepare(light_direction, self.__shadow_box)
        self.__entity_renderer.render(entities)
        self.finish()

    def clean_up(self) -> None:
        """
        Clean up the shader and FBO on closing.
        :return:
        """
        self.__shader.clean_up()
        self.__shadow_fbo.clean_up()

    def get_shadow_map(self) -> int:
        """
        :return:
        The ID of the shadow map texture. The ID will always stay the
        same, even when the contents of the shadow map texture change
        each frame.
        """
        return self.__shadow_fbo.get_shadow_map()

    def prepare(self, light_direction: vec3, box: ShadowBox) -> None:
        """
        Prepare for the shadow render pass. This first updates the dimensions of
        the orthographic "view cuboid" based on the information that was
        calculated in the ShadowBox class. The light's "view" matrix is
        also calculated based on the light's direction and the center position of
        the "view cuboid" which was also calculated in the ShadowBox
        class. These two matrices are multiplied together to create the
        projection-view matrix. This matrix determines the size, position, and
        orientation of the "view cuboid" in the world. This method also binds the
        shadows FBO so that everything rendered after this gets rendered to the
        FBO. It also enables depth testing, and clears any data that is in the
        FBOs depth attachment from last frame. The simple shader program is also
        started.
        :param light_direction: the direction of the light rays coming from the sun.
        :param box: the shadow box, which contains all the info about the "view cuboid".
        :return:
        """
        self.__shader.start()
        self.update_ortho_projection_matrix(box.get_width(), box.get_height(), box.get_length())
        self.update_light_view_matrix(light_direction, box.get_center())
        self.__shadow_fbo.bind_frame_buffer()
        glEnable(GL_DEPTH_TEST)
        glClear(GL_DEPTH_BUFFER_BIT)

    def finish(self) -> None:
        """
        Finish the shadow render pass. Stops the shader and unbinds the shadow
        FBO, so everything rendered after this point is rendered to the screen,
        rather than to the shadow FBO.
        :return:
        """
        self.__shader.stop()
        self.__shadow_fbo.unbind_frame_buffer()

    def update_light_view_matrix(self, direction: vec3, center: vec3) -> None:
        """
        Updates the "view" matrix of the light. This creates a view matrix which
        will line up the direction of the "view cuboid" with the direction of the
        light. The light itself has no position, so the "view" matrix is centered
        at the center of the "view cuboid". The created view matrix determines
        where and how the "view cuboid" is positioned in the world. The size of
        the view cuboid, however, is determined by the projection matrix.
        :param direction: the light direction, and therefore the direction that the "view cuboid" should be pointing.
        :param center: the center of the "view cuboid" in world space.
        :return:
        """
        direction = direction.normalize()
        self.__light_view_matrix = mat4().identity()
        pitch = math.acos(math.sqrt(direction.x**2 + direction.z**2))
        self.__light_view_matrix = self.__light_view_matrix.rotate(pitch, vec3(1, 0, 0))
        yaw = math.degrees(math.atan(direction.x / direction.z))
        yaw = yaw - 180 if direction.z > 0 else yaw
        self.__light_view_matrix = self.__light_view_matrix.rotate(-math.radians(yaw), vec3(0, 1, 0))
        self.__light_view_matrix = self.__light_view_matrix.translate(-center)
        self.__shader.load_light_view_matrix(self.__light_view_matrix.toList())

    def update_ortho_projection_matrix(self, width: float, height: float, length: float) -> None:
        """
        Creates the orthographic projection matrix. This projection matrix
        basically sets the width, length and height of the "view cuboid", based
        on the values that were calculated in the ShadowBox class.
        :param width: shadow box width.
        :param height: shadow box height.
        :param length: shadow box length.
        :return:
        """
        self.__projection_matrix = mat4()
        self.__projection_matrix[(0, 0)] = 2.0 / width
        self.__projection_matrix[(1, 1)] = 2.0 / height
        self.__projection_matrix[(2, 2)] = -2.0 / length
        self.__projection_matrix[(3, 3)] = 1
        self.__shader.load_projection_matrix(self.__projection_matrix.toList())

    @staticmethod
    def __create_offset() -> mat4:
        """
        Create the offset for part of the conversion to shadow map space. This
        conversion is necessary to convert from one coordinate system to the
        coordinate system that we can use to sample to shadow map.
        :return: The offset as a matrix (so that it's easy to apply to other matrices).
        """
        offset = mat4(1)
        offset[(0, 3)] = 0.5
        offset[(1, 3)] = 0.5
        offset[(2, 3)] = 0.5
        offset[(0, 0)] = 0.5
        offset[(1, 1)] = 0.5
        offset[(2, 2)] = 0.5
        return offset

    def get_offset(self) -> list:
        return list(self.__offset)

    def get_ortho_projection_matrix(self) -> list:
        return list(self.__projection_matrix)

    def get_light_space_transform(self) -> list:
        """
        :return: The light's "view" matrix.
        """
        return list(self.__light_view_matrix)

    @classmethod
    def get_shadow_map_size(cls) -> float:
        return cls.__SHADOW_MAP_SIZE
