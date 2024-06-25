from src.models.textured_model import TexturedModel


class Food:
    SANDWICH = 0
    SIRSERLI = 1
    CROISSANT = 2
    CHOCOLATE_CROISSANT = 3
    ALMOND_CROISSANT = 4
    ERDBEERTOERTCHEN = 5
    COOKIE = 6
    SPITZBUB = 7
    LINZERLI = 8
    CARAC = 9
    WURSTWEGGE = 10
    SCHINKENGIPFEL = 11
    CHOCOLATE_CAKE = 12
    PASSIONFRUIT_CAKE = 13
    CARROT_CAKE = 14
    CITRON_CAKE = 15

    def __init__(self, model: TexturedModel, collider: TexturedModel, food: int):
        self.__model = model
        self.__collider = collider
        self.__food = food

    def get_model(self) -> TexturedModel:
        return self.__model

    def get_collider(self) -> TexturedModel:
        return self.__collider

    def get_food(self) -> int:
        return self.__food
