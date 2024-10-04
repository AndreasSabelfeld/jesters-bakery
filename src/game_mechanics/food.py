from src.models.textured_model import TexturedModel


class Food:
    """
    Represents a food item with a primary model, an optional alternate model, and their respective colliders.
    """

    def __init__(self, model: TexturedModel, collider: TexturedModel, food: str):
        """
        Initializes the Food object with a primary model, collider, and the food name.

        :param model: The main textured model of the food item.
        :param collider: The collider connected with the main model.
        :param food: The name of the food item.
        """
        self.__model = model
        self.__alt_model = None
        self.__collider = collider
        self.__alt_collider = None
        self.__food = food

    def get_model(self) -> TexturedModel:
        """
        Returns the primary textured model of the food.

        :return: The main textured model.
        """
        return self.__model

    def get_collider(self) -> TexturedModel:
        """
        Returns the primary collider connected with the food model.

        :return: The main collider.
        """
        return self.__collider

    def get_food(self) -> str:
        """
        Returns the name of the food item.

        :return: The name of the food as a string.
        """
        return self.__food

    def set_alt_model(self, model: TexturedModel) -> None:
        """
        Sets an alternate model for the food item.

        :param model: The alternate textured model to be set.
        """
        self.__alt_model = model

    def get_alt_model(self) -> TexturedModel:
        """
        Returns the alternate textured model of the food, if one is set.

        :return: The alternate textured model or None if not set.
        """
        return self.__alt_model

    def set_alt_collider(self, collider: TexturedModel) -> None:
        """
        Sets an alternate collider for the food item.

        :param collider: The alternate collider to be set.
        """
        self.__alt_collider = collider

    def get_alt_collider(self) -> TexturedModel:
        """
        Returns the alternate collider connected with the alternate model, if one is set.

        :return: The alternate collider or None if not set.
        """
        return self.__alt_collider
