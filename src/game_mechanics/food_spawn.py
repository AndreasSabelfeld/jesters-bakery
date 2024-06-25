from src.entities.entity import Entity
from src.game_mechanics.food import Food
from src.game_mechanics.game_object import GameObject


class FoodSpawn:
    def __init__(self, food: Food, pos: list[float], rot: list[float], size: float, entity_list: list, collider_list: list):
        self.__food = food
        self.__pos = pos
        self.__rot = rot
        self.__size = size
        self.__entity_list = entity_list
        self.__collider_list = collider_list

        entity = Entity(food.get_model(), pos, *rot, size)
        collider = Entity(food.get_collider(), pos, *rot, size)
        self.__game_object = GameObject(entity, collider=collider, int_name="FOOD")
        self.__game_object.set_attachment(self)
        self.__entity_list.append(self.__game_object)
        self.__collider_list.append(self.__game_object)

    def get_game_object(self) -> GameObject:
        return self.__game_object

    def spawn(self) -> None:
        self.__game_object.set_attachment(None)
        entity = Entity(self.__food.get_model(), self.__pos, *self.__rot, self.__size)
        collider = Entity(self.__food.get_collider(), self.__pos, *self.__rot, self.__size)
        self.__game_object = GameObject(entity, collider=collider, int_name="FOOD")
        self.__game_object.set_attachment(self)
        self.__entity_list.append(self.__game_object)
        self.__collider_list.append(self.__game_object)
