from src.models.textured_model import TexturedModel


class Food:

    def __init__(self, model: TexturedModel, collider: TexturedModel, food: str):
        self.__model = model
        self.__alt_model = None
        self.__collider = collider
        self.__alt_collider = None
        self.__food = food

    def get_model(self) -> TexturedModel:
        return self.__model

    def get_collider(self) -> TexturedModel:
        return self.__collider

    def get_food(self) -> str:
        return self.__food

    def set_alt_model(self, model: TexturedModel) -> None:
        self.__alt_model = model

    def get_alt_model(self) -> TexturedModel:
        return self.__alt_model

    def set_alt_collider(self, collider: TexturedModel) -> None:
        self.__alt_collider = collider

    def get_alt_collider(self) -> TexturedModel:
        return self.__alt_collider
