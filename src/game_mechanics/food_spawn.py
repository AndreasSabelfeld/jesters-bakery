from src.entities.entity import Entity
from src.game_mechanics.food import Food
from src.game_mechanics.game_object import GameObject
from src.render_engine.input_controller import Binds


class FoodSpawn:
    """
    Handles the spawning of food objects in the game
    """

    def __init__(self, food: Food, pos: list[float], rot: list[float], size: float, entity_list: list,
                 collider_list: list):
        """
        Initializes the FoodSpawn object and spawns the food entity and its collider to the game.

        :param food: The food object contining models and details for the spawn.
        :param pos: The position in the game world to spawn the food.
        :param rot: The rotation of the food object in the game world.
        :param size: The size scale of the food object.
        :param entity_list: A list to which the spawned game object will be appended.
        :param collider_list: A list to which the spawned collider will be appended.
        """
        self.__food = food
        self.__pos = pos
        self.__rot = rot
        self.__size = size
        self.__entity_list = entity_list
        self.__collider_list = collider_list

        entity = Entity(food.get_model(), pos, *rot, size)
        collider = Entity(food.get_collider(), pos, *rot, size)
        self.__game_object = GameObject(entity, collider=collider, int_name="FOOD")
        self.__game_object.set_ext_name(food.get_food())
        self.__game_object.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to pick up.")
        self.__game_object.set_attachment(self)
        self.__entity_list.append(self.__game_object)
        self.__collider_list.append(self.__game_object)

    def get_game_object(self) -> GameObject:
        """
        Returns the GameObject of the spawned food.

        :return: The food GameObject.
        """
        return self.__game_object

    def spawn(self) -> GameObject:
        """
        Spawns the food, using an alternate model and collider if available, or the default if not.

        :return: The newly spawned GameObject.
        """
        if self.__food.get_alt_model():
            model = self.__food.get_alt_model()
            collider = self.__food.get_alt_collider()
        else:
            model = self.__food.get_model()
            collider = self.__food.get_collider()

        food_name = self.__food.get_food()
        entity = Entity(model, self.__pos, *self.__rot, self.__size)
        collider = Entity(collider, self.__pos, *self.__rot, self.__size)
        game_object = GameObject(entity, collider=collider, int_name="FOOD")
        game_object.set_attachment(self.__food)
        game_object.set_ext_name(food_name)
        game_object.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to pick up.")
        self.__entity_list.append(game_object)
        self.__collider_list.append(game_object)

        return game_object
