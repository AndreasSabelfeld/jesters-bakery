from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.render_engine.time import Time


class MixerVessel:
    def __init__(self, vessel: GameObject, obj_loader, loader):
        self.__vessel = vessel
        self.__obj_loader = obj_loader
        self.__loader = loader
        self.__content = list()
        self.__lvl = 0
        self.__max_lvl = 3
        self.__fill_cooldown = 0

    def update(self):
        if self.__fill_cooldown > 0:
            self.__fill_cooldown -= Time.get_delta_time()
        else:
            self.__fill_cooldown = 0

    def get_model(self, level: int, texture) -> TexturedModel:
        return TexturedModel(self.__obj_loader.load_obj_model(f"mixer_vessel_lvl_{level}", self.__loader), texture)

    def fill(self, texture) -> None:
        if self.__fill_cooldown == 0 and self.__lvl < self.__max_lvl:
            self.__vessel.set_child_1(Entity(self.get_model(self.__lvl, texture),
                                             self.__vessel.get_position(),
                                             self.__vessel.get_rot_x(),
                                             self.__vessel.get_rot_y(),
                                             self.__vessel.get_rot_z(),
                                             self.__vessel.get_scale()))
            self.__lvl += 1
            self.__fill_cooldown = 1.5
