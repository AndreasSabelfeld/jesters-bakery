from src.models.textured_model import TexturedModel


class CoffeeContainer:
    ESPRESSO_CUP = 0
    COFFEE_CUP = 1
    CAPPUCCINO_CUP = 2
    SMALL_GLASS = 3
    BIG_GLASS = 4
    TEA_POT = 5

    def __init__(self, cup_container: int, loader, obj_loader):
        self.__cup_container = cup_container
        self.__level = 0
        self.__loader = loader
        self.__obj_loader = obj_loader

    def get_model(self, container_type: int, level: int, texture: str) -> TexturedModel:
        match container_type:
            case 0:
                ...
            case 1:
                return TexturedModel(self.__obj_loader.load_obj_model(f"small_coffee_cup_lvl_{level}", self.__loader), texture)
            case 2:
                return TexturedModel(self.__obj_loader.load_obj_model(f"big_coffee_cup_lvl_{level}", self.__loader), texture)
            case 3:
                return TexturedModel(self.__obj_loader.load_obj_model(f"small_glass_lvl_{level}", self.__loader), texture)
            case 4:
                return TexturedModel(self.__obj_loader.load_obj_model(f"big_glass_lvl_{level}", self.__loader), texture)
            case 5:
                return TexturedModel(self.__obj_loader.load_obj_model(f"tea_pot_lvl_{level}", self.__loader), texture)

