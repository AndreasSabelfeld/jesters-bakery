from src.guis.gui_texture import GuiTexture


class CoffeeProduct:
    """
    Product entry for the coffee machine. Each product has a name, icon, a brew length and a respective 'container',
    mug, glass etc.
    """

    ESPRESSO_CUP = 0
    COFFEE_CUP = 1
    CAPPUCCINO_CUP = 2
    GLASS = 3

    ICON_SIZE = 128  # pixels

    def __init__(self, name: str, icon: GuiTexture, brew_length: float, container_type: int) -> None:
        """
        Creates a new CoffeeProduct instance

        :param name: The name of the product (e.g. 'Cappuccino')
        :param icon: The GUI object of the icon
        :param brew_length: The time it takes to brew the product [in seconds]
        :param container_type: The container the product needs to be brewed in (int from 0 to 3)
        """
        self.__name = name
        self.__icon = icon
        self.__brew_length = brew_length
        self.__container_type = container_type

    def get_name(self) -> str:
        return self.__name

    def get_icon(self) -> GuiTexture:
        return self.__icon

    def get_brew_length(self) -> float:
        return self.__brew_length

    def get_container_type(self) -> int:
        return self.__container_type
