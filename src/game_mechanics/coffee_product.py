

class CoffeeProduct:

    ESPRESSO_CUP = 0
    COFFEE_CUP = 1
    CAPPUCCINO_CUP = 2
    GLASS = 3

    def __init__(self, name: str, icon, brew_length: float, container: int) -> None:
        self.__name = name
        self.__icon = icon
        self.__brew_length = brew_length
        self.__container = container
