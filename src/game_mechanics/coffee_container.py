from src.audio.audio_master import AudioMaster
from src.audio.source import Source
from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.textures.model_texture import ModelTexture


class CoffeeContainer:
    ESPRESSO_CUP = 0
    SMALL_GLASS = 1
    COFFEE_CUP = 2
    CAPPUCCINO_CUP = 3
    BIG_GLASS = 4
    TEA_POT = 5
    BEER = 6
    PROSECCO = 7

    __loader = None
    __obj_loader = None

    def __init__(self, container_type: int, parent_entity: GameObject):
        self.__container_type = container_type
        self.__parent_entity = parent_entity
        self.__level = 0
        self.__overflown = False
        self.__content = list()
        self.__parent_entity.set_info(str(self.__content))
        self.__pour_sound = AudioMaster.load_sound("res/audio/pour.wav")
        self.__parent_entity.get_sfx_source().set_volume(3)

    @classmethod
    def add_loaders(cls, loader, obj_loader):
        cls.__loader = loader
        cls.__obj_loader = obj_loader

    def get_model(self, container_type: int, level: int, texture) -> TexturedModel:
        if level > 3:
            level = 3
            # if content is not a sublist of:
            if not {"Oat Milk", "Foam"} <= set(self.__content) and "Sprite" not in self.__content:
                self.toggle_overflown(texture)
        match container_type:
            case 0:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/espresso_cup_lvl_{level}", self.__loader), texture)
            case 1:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/small_glass_lvl_{level}", self.__loader), texture)
            case 2:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/small_coffee_cup_lvl_{level}", self.__loader), texture)
            case 3:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/big_coffee_cup_lvl_{level}", self.__loader), texture)
            case 4:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/big_glass_lvl_{level}", self.__loader), texture)
            case 5:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/tea_pot_lvl_{level}", self.__loader), texture)
            case 6:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/beer_lvl_{level}", self.__loader), texture)
            case 7:
                return TexturedModel(self.__obj_loader.load_obj_model(f"objs/cups/prosecco_glass_lvl_{level}", self.__loader), texture)

    def fill(self, texture: ModelTexture) -> None:
        self.__parent_entity.get_sfx_source().play(self.__pour_sound)
        self.__level += 1
        self.__parent_entity.set_child_0(Entity(self.get_model(self.__container_type, self.__level, texture),
                                                self.__parent_entity.get_position(), 0, 0, 0, 1))

    def set_level(self, level: int, texture) -> None:
        self.__parent_entity.get_sfx_source().play(self.__pour_sound)
        self.__level = level
        self.__parent_entity.set_child_0(Entity(self.get_model(self.__container_type, self.__level, texture),
                                                self.__parent_entity.get_position(), 0, 0, 0, 1))

    def get_level(self) -> int:
        return self.__level

    def set_texture(self, texture: ModelTexture) -> None:
        self.set_level(self.get_level(), texture)

    def get_container_type(self) -> int:
        return self.__container_type

    def toggle_overflown(self, texture) -> None:
        if not self.__overflown:
            self.__overflown = True
            self.__parent_entity.get_entity().get_model().set_texture(texture)

    def get_content(self) -> list:
        return self.__content

    def append_content(self, content: str | list) -> None:
        if isinstance(content, str):
            # if we have two halves, this makes one full
            if "half" in content and content in self.__content:
                self.__content.remove(content)
                self.__content.append(content.removesuffix(" half"))
            elif self.__content and self.__content[-1] == content:
                return
            else:
                self.__content.append(content)
        elif isinstance(content, list):
            self.__content.extend(content)

    def remove_content(self) -> list:
        c = self.__content.copy()
        self.__content = []
        return c
