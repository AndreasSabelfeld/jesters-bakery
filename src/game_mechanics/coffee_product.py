from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.guis.gui_texture import GuiTexture
from src.game_mechanics.coffe_page import CoffeePage


class CoffeeProduct:
    """
    Product entry for the coffee machine. Each product has a name, icon, a brew length and a respective 'container',
    mug, glass etc.
    """

    ESPRESSO_CUP = 0
    COFFEE_CUP = 1
    CAPPUCCINO_CUP = 2
    SMALL_GLASS = 3
    BIG_GLASS = 4
    TEA_POT = 5

    ICON_SIZE = 128  # pixels

    all_texts = []

    def __init__(self, name: str, icon: GuiTexture, brew_length: float, container_type: int, allows_double: bool,
                 loader) -> None:
        """
        Creates a new CoffeeProduct instance

        :param name: The name of the product (e.g. 'Cappuccino')
        :param icon: The GUI object of the icon
        :param brew_length: The time it takes to brew the product [in seconds]
        :param container_type: The container the product needs to be brewed in (int from 0 to 5)
        """
        self.__name = name
        self.__icon = icon
        self.__brew_length = brew_length
        self.__container_type = container_type
        self.__allows_double = allows_double
        self.__loader = loader
        self.__font = FontType(self.__loader.load_texture("candara"), "res/candara.fnt")
        self.__icon_size = 0.125    # same as in CoffeeMachineOS class
        self.__text_offset = 0.04   # same as in CoffeeMachineOS class
        self.__text = GUIText(self.__name,
                              18,
                              self.__font,
                              [(self.__icon.get_position()[0] + 1) / 2 - self.__icon_size / 2,
                               (1 - self.__icon.get_position()[1]) / 2 + self.__text_offset],
                              self.__icon_size,
                              True)
        self.__text.set_color(1, 0, 0)
        self.__text.set_border_width(0.7)
        self.__text.set_border_edge(0.1)
        CoffeePage.add_product(self)
        CoffeeProduct.all_texts.append(self.__text)

    def get_name(self) -> str:
        return self.__name

    def get_icon(self) -> GuiTexture:
        return self.__icon

    def get_brew_length(self) -> float:
        return self.__brew_length

    def get_container_type(self) -> int:
        return self.__container_type

    def get_font(self) -> FontType:
        return self.__font

    def get_text(self) -> GUIText:
        return self.__text
