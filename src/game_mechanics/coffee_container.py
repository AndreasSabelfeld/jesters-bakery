from src.entities.entity import Entity
from src.models.textured_model import TexturedModel
from src.textures.model_texture import ModelTexture


class CoffeeContainer:
    ESPRESSO_CUP = 0
    SMALL_GLASS = 1
    COFFEE_CUP = 2
    CAPPUCCINO_CUP = 3
    BIG_GLASS = 4
    TEA_POT = 5

    __loader = None
    __obj_loader = None

    def __init__(self, container_type: int, parent_entity):
        self.__container_type = container_type
        self.__parent_entity = parent_entity
        self.__level = 0
        self.__overflown = False
        self.__content_name = "empty"

    @classmethod
    def add_loaders(cls, loader, obj_loader):
        cls.__loader = loader
        cls.__obj_loader = obj_loader

    def get_model(self, container_type: int, level: int, texture: str) -> TexturedModel:
        if level > 3:
            self.toggle_overflown()
            level = 3
        match container_type:
            case 0:
                ...
                # TODO
            case 1:
                return TexturedModel(self.__obj_loader.load_obj_model(f"small_glass_lvl_{level}", self.__loader), texture)
            case 2:
                return TexturedModel(self.__obj_loader.load_obj_model(f"small_coffee_cup_lvl_{level}", self.__loader), texture)
            case 3:
                return TexturedModel(self.__obj_loader.load_obj_model(f"big_coffee_cup_lvl_{level}", self.__loader), texture)
            case 4:
                return TexturedModel(self.__obj_loader.load_obj_model(f"big_glass_lvl_{level}", self.__loader), texture)
            case 5:
                return TexturedModel(self.__obj_loader.load_obj_model(f"tea_pot_lvl_{level}", self.__loader), texture)

    def fill(self, texture) -> None:
        self.__level += 1
        self.__parent_entity.set_child(Entity(self.get_model(self.__container_type, self.__level, texture),
                                              self.__parent_entity.get_position(), 0, 0, 0, 1))

    def set_level(self, level: int, texture) -> None:
        self.__level = level
        self.__parent_entity.set_child(Entity(self.get_model(self.__container_type, self.__level, texture),
                                              self.__parent_entity.get_position(), 0, 0, 0, 1))

    def get_level(self) -> int:
        return self.__level

    def get_container_type(self) -> int:
        return self.__container_type

    def toggle_overflown(self) -> None:
        overflown_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        if not self.__overflown:
            self.__overflown = True
            self.__parent_entity.get_entity().get_model().set_texture(overflown_texture)
