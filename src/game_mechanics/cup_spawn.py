from src.game_mechanics.game_object import GameObject
from src.game_mechanics.coffee_container import CoffeeContainer
from src.obj_converter.obj_loader import OBJLoader
from src.render_engine.loader import Loader


class CupSpawn:

    def __init__(self, container_type: int, pos: list[float], rot: list[float], size: float, loader: Loader, obj_loader: OBJLoader,
                 entities: list, colliders: list):
        self.__container_type = container_type
        self.__pos = pos
        self.__rot = rot
        self.__size = size
        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__entities = entities
        self.__colliders = colliders

    def spawn(self) -> GameObject:
        import src.master.prefabs as prefabs

        match self.__container_type:
            case CoffeeContainer.ESPRESSO_CUP:
                game_object = prefabs.espresso_cup(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.SMALL_GLASS:
                game_object = prefabs.small_glass(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.COFFEE_CUP:
                game_object = prefabs.coffee_cup(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.CAPPUCCINO_CUP:
                game_object = prefabs.cappuccino_cup(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.BIG_GLASS:
                game_object = prefabs.big_glass(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.TEA_POT:
                game_object = prefabs.tea(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.BEER:
                game_object = prefabs.beer(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case CoffeeContainer.PROSECCO:
                game_object = prefabs.prosecco_glass(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)
            case _:
                game_object = prefabs.plate(self.__pos, self.__rot, self.__size, self.__loader, self.__obj_loader)

        self.__entities.append(game_object)
        self.__colliders.append(game_object)
        return game_object
