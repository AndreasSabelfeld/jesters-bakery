from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.guis.gui_texture import GuiTexture
from src.game_mechanics.coffee_page import CoffeePage, CoffeePageLactoseFree
from src.textures.model_texture import ModelTexture


class CoffeeProduct:
    """
    Product entry for the coffee machine. Each product has a name, icon, a brew length and a respective 'container',
    mug, glass etc.
    """

    ESPRESSO_CUP = 0
    SMALL_GLASS = 1
    COFFEE_CUP = 2
    CAPPUCCINO_CUP = 3
    BIG_GLASS = 4
    TEA_POT = 5

    ICON_SIZE = 128  # pixels

    all_texts = []

    def __init__(self, name: str, icon: GuiTexture, brew_length: float, container_type: int, allows_double: bool,
                 loader, texture: ModelTexture, content: list, add_to_coffee_page: bool = True,
                 lactose_free: bool = False) -> None:
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
        self.__texture = texture
        self.__content = content
        self.__lactose_free = lactose_free
        self.__font = FontType(self.__loader.load_texture("fnts/arial"), "res/fnts/arial.fnt")
        self.__icon_size = 0.125    # same as in CoffeeMachineOS class
        self.__text_offset = 0.04   # same as in CoffeeMachineOS class
        self.__text = GUIText(self.__name,
                              14,
                              self.__font,
                              [(self.__icon.get_position()[0] + 1) / 2 - self.__icon_size / 2,
                               (1 - self.__icon.get_position()[1]) / 2 + self.__text_offset],
                              self.__icon_size,
                              True)
        self.__text.set_color(1, 1, 1)
        self.__text.set_outline_color(0, 0, 0)
        self.__text.set_border_width(0.9)
        self.__text.set_border_edge(0.1)
        if add_to_coffee_page:
            if not lactose_free:
                CoffeePage.add_product(self)
            else:
                CoffeePageLactoseFree.add_product(self)
        if not lactose_free:
            CoffeeProduct.all_texts.append(self.__text)
        else:
            CoffeeProductLactoseFree.all_texts.append(self.__text)

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

    def is_allow_double(self) -> bool:
        return self.__allows_double

    def get_texture(self) -> ModelTexture:
        return self.__texture

    def get_content(self) -> list:
        return self.__content

    def is_lactose_free(self) -> bool:
        return self.__lactose_free


class CoffeeProductLactoseFree(CoffeeProduct):
    """
    Product entry for the lactose free coffee machine. Each product has a name, icon, a brew length and a respective
    'container', mug, glass etc.
    """

    all_texts = []

    def __init__(self, name: str, icon: GuiTexture, brew_length: float, container_type: int, allows_double: bool,
             loader, texture, content: list, add_to_coffee_page: bool = True) -> None:
        """
        Creates a new CoffeeProduct instance

        :param name: The name of the product (e.g. 'Cappuccino')
        :param icon: The GUI object of the icon
        :param brew_length: The time it takes to brew the product [in seconds]
        :param container_type: The container the product needs to be brewed in (int from 0 to 5)
        """
        super().__init__(name, icon, brew_length, container_type, allows_double, loader, texture, content,
                         add_to_coffee_page, lactose_free=True)
