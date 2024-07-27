from src.shaders.static_shader import StaticShader
from src.shaders.outline_shader import OutlineShader
from src.terrain.terrain_shader import TerrainShader
from src.normal_mapping.normal_mapping_shader import NormalMappingShader
from src.skybox.skybox_renderer import SkyboxRenderer
from src.normal_mapping.normal_mapping_renderer import NormalMappingRenderer
from src.shadows.shadow_map_master_renderer import ShadowMapMasterRenderer
from src.shadows.shadow_box import ShadowBox
from src.game_mechanics.game_object import GameObject
from .entity_renderer import EntityRenderer
from .outline_renderer import OutlineRenderer
from .terrain_renderer import TerrainRenderer
from .display_manager import DisplayManager

import math
from src.pycgtypes import mat4
from OpenGL.GL import *


class MasterRenderer:

    __FOV = 70
    __NEAR_PLANE = 0.1
    __FAR_PLANE = 1000

    __fog_density = 0.007
    __fog_gradient = 1.5

    def __init__(self, loader, cam):
        self.enable_culling()

        self.__entity_shader = StaticShader()
        self.__outline_shader = OutlineShader()
        self.__terrain_shader = TerrainShader()
        self.__normal_map_shader = NormalMappingShader()
        self.__projection_matrix = self.create_projection_matrix()
        self.__entity_renderer = EntityRenderer(self.__entity_shader, self.__projection_matrix)
        self.__outline_renderer = OutlineRenderer(self.__outline_shader, self.__projection_matrix)
        self.__terrain_renderer = TerrainRenderer(self.__terrain_shader, self.__projection_matrix)
        self.__skybox_renderer = SkyboxRenderer(loader, self.__projection_matrix)
        self.__normal_map_renderer = NormalMappingRenderer(self.__projection_matrix, self.__normal_map_shader)
        self.__shadow_map_renderer = ShadowMapMasterRenderer(cam)

        self.__entities = dict()
        self.__normal_map_entities = dict()
        self.__terrains = []

    @staticmethod
    def enable_culling() -> None:
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    @staticmethod
    def disable_culling() -> None:
        glDisable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def render_scene(self, entities: list, normal_map_entities: list, terrains: list, lights: list,
                     camera, display, clip_plane: list[float] = (0, 0, 0, 0)) -> None:
        for terrain in terrains:
            self.process_terrain(terrain)
        for entity in entities:
            self.process_entity(entity)
        for entity in normal_map_entities:
            self.process_normal_map_entity(entity)
        self.render(display, lights, camera, clip_plane)

    def prepare(self) -> None:
        glActiveTexture(GL_TEXTURE5)
        glBindTexture(GL_TEXTURE_2D, self.get_shadow_map_texture())

    def render(self, display, lights: list, camera, clip_plane: list[float]) -> None:
        display.update_display()

        glDisable(GL_DEPTH_TEST)
        self.__skybox_renderer.render(camera, *display.get_backdrop_color())  # render the skybox behind everything else
        glEnable(GL_DEPTH_TEST)

        self.prepare()
        self.__entity_shader.start()
        self.__entity_shader.load_clip_plane(clip_plane)
        self.__entity_shader.load_sky_color(*display.get_backdrop_color())  # sky color
        self.__entity_shader.load_fog_density(self.get_fog_density())       # fog density
        self.__entity_shader.load_fog_gradient(self.get_fog_gradient())     # fog gradient
        self.__entity_shader.load_lights(lights)
        self.__entity_shader.load_view_matrix(camera)
        self.__entity_shader.load_to_shadow_space_matrix(self.__shadow_map_renderer.get_offset(),
                                                         self.__shadow_map_renderer.get_ortho_projection_matrix(),
                                                         self.__shadow_map_renderer.get_light_space_transform())
        self.__entity_shader.load_shadow_distance(ShadowBox.get_shadow_distance())
        self.__entity_shader.load_shadow_map_size(self.__shadow_map_renderer.get_shadow_map_size())
        self.__entity_renderer.render(self.__entities)
        self.__entity_shader.stop()

        self.__normal_map_shader.start()
        self.__normal_map_shader.load_fog_density(self.get_fog_density())    # fog density
        self.__normal_map_shader.load_fog_gradient(self.get_fog_gradient())  # fog gradient
        self.__normal_map_renderer.render(self.__normal_map_entities, clip_plane, lights, camera)
        self.__normal_map_shader.stop()

        self.__terrain_shader.start()
        self.__terrain_shader.load_clip_plane(clip_plane)
        self.__terrain_shader.load_sky_color(*display.get_backdrop_color())
        self.__terrain_shader.load_fog_density(self.get_fog_density())    # fog density
        self.__terrain_shader.load_fog_gradient(self.get_fog_gradient())  # fog gradient
        self.__terrain_shader.load_lights(lights)
        self.__terrain_shader.load_view_matrix(camera)
        self.__terrain_shader.load_to_shadow_space_matrix(self.__shadow_map_renderer.get_offset(),
                                                          self.__shadow_map_renderer.get_ortho_projection_matrix(),
                                                          self.__shadow_map_renderer.get_light_space_transform())
        self.__terrain_shader.load_shadow_distance(ShadowBox.get_shadow_distance())
        self.__terrain_shader.load_shadow_map_size(self.__shadow_map_renderer.get_shadow_map_size())
        self.__terrain_renderer.render(self.__terrains)
        self.__terrain_shader.stop()

        self.__terrains.clear()
        self.__entities.clear()
        self.__normal_map_entities.clear()

    def render_shadow_map(self, entity_list: list, sun) -> None:
        for entity in entity_list:
            self.process_entity(entity)
        self.__shadow_map_renderer.render(self.__entities, sun)
        self.__entities.clear()

    def render_outline(self, entity_list):
        for entity in entity_list:
            self.process_entity(entity)
        self.__outline_shader.start()
        self.__outline_renderer.render(self.__entities)
        self.__outline_shader.stop()
        self.__entities.clear()

    def process_terrain(self, terrain) -> None:
        self.__terrains.append(terrain)

    def process_entity(self, entity) -> None:
        if isinstance(entity, GameObject):
            if entity.has_child_0():
                self.process_entity(entity.get_child_0())
            if entity.has_child_1():
                self.process_entity(entity.get_child_1())
            entity = entity.get_entity()
        entity_model = entity.get_model()
        batch = self.__entities.get(entity_model)
        if batch is not None:
            batch.append(entity)
        else:
            self.__entities[entity_model] = [entity]

    def process_normal_map_entity(self, entity) -> None:
        if isinstance(entity, GameObject):
            if entity.has_child_0():
                self.process_entity(entity.get_child_0())
            if entity.has_child_1():
                self.process_entity(entity.get_child_1())
            entity = entity.get_entity()
        entity_model = entity.get_model()
        batch = self.__normal_map_entities.get(entity_model)
        if batch is not None:
            batch.append(entity)
        else:
            self.__normal_map_entities[entity_model] = [entity]

    def create_projection_matrix(self) -> list:
        projection_matrix = mat4()
        aspect_ratio = DisplayManager.get_width() / DisplayManager.get_height()
        y_scale = (1 / math.tan(math.radians(self.get_fov()/2)))
        x_scale = y_scale / aspect_ratio
        frustum_length = self.get_far_plane() - self.get_near_plane()

        projection_matrix[(0, 0)] = x_scale
        projection_matrix[(1, 1)] = y_scale
        projection_matrix[(2, 2)] = -((self.get_far_plane() + self.get_near_plane()) / frustum_length)
        projection_matrix[(3, 2)] = -1
        projection_matrix[(2, 3)] = -((2 * self.get_near_plane() * self.get_far_plane()) / frustum_length)
        projection_matrix[(3, 3)] = 0

        return list(projection_matrix)  # list so OpenGL can use the values

    def clean_up(self) -> None:
        self.__entity_shader.clean_up()
        self.__terrain_shader.clean_up()
        self.__normal_map_renderer.clean_up()
        self.__shadow_map_renderer.clean_up()

    def get_projection_matrix(self) -> list[list]:
        return self.__projection_matrix

    def get_shadow_map_texture(self) -> int:
        return self.__shadow_map_renderer.get_shadow_map()

    @classmethod
    def set_fog_density(cls, value) -> None:
        cls.__fog_density = value

    @classmethod
    def get_fog_density(cls) -> float:
        return cls.__fog_density

    @classmethod
    def set_fog_gradient(cls, value) -> None:
        cls.__fog_gradient = value

    @classmethod
    def get_fog_gradient(cls) -> float:
        return cls.__fog_gradient

    @classmethod
    def set_fov(cls, value) -> None:
        cls.__FOV = value

    @classmethod
    def get_fov(cls) -> float:
        return cls.__FOV

    @classmethod
    def set_near_plane(cls, value) -> None:
        cls.__NEAR_PLANE = value

    @classmethod
    def get_near_plane(cls) -> float:
        return cls.__NEAR_PLANE

    @classmethod
    def set_far_plane(cls, value) -> None:
        cls.__FAR_PLANE = value

    @classmethod
    def get_far_plane(cls) -> float:
        return cls.__FAR_PLANE
