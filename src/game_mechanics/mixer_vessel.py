from src.entities.entity import Entity
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.render_engine.time import Time
from src.textures.model_texture import ModelTexture


class MixerVessel:
    def __init__(self, vessel: GameObject, obj_loader, loader):
        self.__vessel = vessel
        self.__obj_loader = obj_loader
        self.__loader = loader
        self.__content = list()
        self.__lvl = 0
        self.__max_lvl = 3
        self.__fill_cooldown = 0
        self.__content = []
        self.__texture = None

    def update(self):
        if self.__fill_cooldown > 0:
            self.__fill_cooldown -= Time.get_delta_time()
        else:
            self.__fill_cooldown = 0

    def get_model(self, level: int, texture) -> TexturedModel:
        return TexturedModel(self.__obj_loader.load_obj_model(f"objs/machinery/mixer_vessel_lvl_{level}", self.__loader), texture)

    def get_level(self) -> int:
        return self.__lvl

    def set_level(self, level: int, texture) -> None:
        self.__lvl = level
        self.__vessel.set_child_0(Entity(self.get_model(self.__lvl, texture), self.__vessel.get_position(), 0, 0, 0,
                                         self.__vessel.get_scale()))
        self.__texture = texture

    def set_texture(self, texture: ModelTexture) -> None:
        self.set_level(self.get_level(), texture)

    @staticmethod
    def get_container_type() -> int:
        return CoffeeContainer.BIG_GLASS

    def fill(self, texture) -> None:
        if self.__fill_cooldown == 0 and self.__lvl < self.__max_lvl:
            self.__vessel.set_child_0(Entity(self.get_model(self.__lvl, texture),
                                             self.__vessel.get_position(),
                                             self.__vessel.get_rot_x(),
                                             self.__vessel.get_rot_y(),
                                             self.__vessel.get_rot_z(),
                                             self.__vessel.get_scale()))
            self.__lvl += 1
            self.__fill_cooldown = 1.5
            self.__texture = texture

    def empty(self) -> None:
        self.__vessel.remove_child_0()
        self.remove_content()
        self.__lvl = 0

    def append_content(self, content: str | list) -> None:
        if self.__content and self.__content[-1] == content:
            return
        if isinstance(content, str):
            self.__content.append(content)
        elif isinstance(content, list):
            self.__content.extend(content)

    def remove_content(self) -> list:
        c = self.__content.copy()
        self.__content.clear()
        return c

    def get_content(self) -> list:
        return self.__content

    def get_texture(self):
        return self.__texture

    def get_fill_lvl(self) -> int:
        return self.__lvl
