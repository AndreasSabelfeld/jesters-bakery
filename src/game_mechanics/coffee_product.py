from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.guis.gui_texture import GuiTexture
from src.game_mechanics.coffe_page import CoffeePage
from src.models.textured_model import TexturedModel
from src.textures.model_texture import ModelTexture
from src.toolbox.decorators import run_once


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

    ESSPRESSO_LVLS = ()
    COFFEE_LVLS = ()
    CAPPUCCINO_LVLS = ()
    SMALL_GLASS_LVLS = ()
    BIG_GLASS_LVLS = ()
    TEA_POT_LVLS = ()

    ICON_SIZE = 128  # pixels

    all_texts = []

    def __init__(self, name: str, icon: GuiTexture, brew_length: float, container_type: int, loader, obj_loader) -> None:
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
        self.__loader = loader
        self.__obj_loader = obj_loader
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
        self.__load_models()

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

    @run_once
    def __load_models(self) -> None:
        coffee_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        coffee_lvl_0 = TexturedModel(self.__obj_loader.load_obj_model("small_coffee_cup_lvl_0", self.__loader), coffee_texture)
        coffee_lvl_1 = TexturedModel(self.__obj_loader.load_obj_model("small_coffee_cup_lvl_1", self.__loader), coffee_texture)
        coffee_lvl_2 = TexturedModel(self.__obj_loader.load_obj_model("small_coffee_cup_lvl_2", self.__loader), coffee_texture)
        coffee_lvl_3 = TexturedModel(self.__obj_loader.load_obj_model("small_coffee_cup_lvl_3", self.__loader), coffee_texture)

        cappuccino_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        cappuccino_lvl_0 = TexturedModel(self.__obj_loader.load_obj_model("big_coffee_cup_lvl_0", self.__loader), cappuccino_texture)
        cappuccino_lvl_1 = TexturedModel(self.__obj_loader.load_obj_model("big_coffee_cup_lvl_1", self.__loader), cappuccino_texture)
        cappuccino_lvl_2 = TexturedModel(self.__obj_loader.load_obj_model("big_coffee_cup_lvl_2", self.__loader), cappuccino_texture)
        cappuccino_lvl_3 = TexturedModel(self.__obj_loader.load_obj_model("big_coffee_cup_lvl_3", self.__loader), cappuccino_texture)

        small_glass_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        small_glass_lvl_0 = TexturedModel(self.__obj_loader.load_obj_model("small_glass_lvl_0", self.__loader), small_glass_texture)
        small_glass_lvl_1 = TexturedModel(self.__obj_loader.load_obj_model("small_glass_lvl_1", self.__loader), small_glass_texture)
        small_glass_lvl_2 = TexturedModel(self.__obj_loader.load_obj_model("small_glass_lvl_2", self.__loader), small_glass_texture)
        small_glass_lvl_3 = TexturedModel(self.__obj_loader.load_obj_model("small_glass_lvl_3", self.__loader), small_glass_texture)

        big_glass_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        big_glass_lvl_0 = TexturedModel(self.__obj_loader.load_obj_model("big_glass_lvl_0", self.__loader), big_glass_texture)
        big_glass_lvl_1 = TexturedModel(self.__obj_loader.load_obj_model("big_glass_lvl_1", self.__loader), big_glass_texture)
        big_glass_lvl_2 = TexturedModel(self.__obj_loader.load_obj_model("big_glass_lvl_2", self.__loader), big_glass_texture)
        big_glass_lvl_3 = TexturedModel(self.__obj_loader.load_obj_model("big_glass_lvl_3", self.__loader), big_glass_texture)

        tea_texture = ModelTexture(self.__loader.load_texture("grass_block"))
        tea_lvl_0 = TexturedModel(self.__obj_loader.load_obj_model("tea_pot_lvl_0", self.__loader), tea_texture)
        tea_lvl_1 = TexturedModel(self.__obj_loader.load_obj_model("tea_pot_lvl_1", self.__loader), tea_texture)
        tea_lvl_2 = TexturedModel(self.__obj_loader.load_obj_model("tea_pot_lvl_2", self.__loader), tea_texture)
        tea_lvl_3 = TexturedModel(self.__obj_loader.load_obj_model("tea_pot_lvl_3", self.__loader), tea_texture)

        CoffeeProduct.COFFEE_LVLS       = (coffee_lvl_0, coffee_lvl_1, coffee_lvl_2, coffee_lvl_3)
        CoffeeProduct.CAPPUCCINO_LVLS   = (cappuccino_lvl_0, cappuccino_lvl_1, cappuccino_lvl_2, cappuccino_lvl_3)
        CoffeeProduct.SMALL_GLASS_LVLS  = (small_glass_lvl_0, small_glass_lvl_1, small_glass_lvl_2, small_glass_lvl_3)
        CoffeeProduct.BIG_GLASS_LVLS    = (big_glass_lvl_0, big_glass_lvl_1, big_glass_lvl_2, big_glass_lvl_3)
        CoffeeProduct.TEA_POT_LVLS      = (tea_lvl_0, tea_lvl_1, tea_lvl_2, tea_lvl_3)
