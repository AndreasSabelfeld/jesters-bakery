from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.render_engine.loader import Loader
from src.toolbox.path import PATH


class KeyHints:
    """
    Handles the display of key hints in the GUI.
    """

    __hint = None

    def __init__(self, loader: Loader):
        """
        Initializes the KeyHints instance.

        :param loader: The loader instance
        """
        self.__loader = loader

        self.__prompt_font = FontType(self.__loader.load_texture("fnts/prompt_font"),
                                      f"{PATH}/res/fnts/prompt_font.fnt")
        KeyHints.__load_text(self.__prompt_font)

    @classmethod
    def __load_text(cls, font) -> None:
        """Loads the text for the key hint text object.

        :param font: The font to use for the text.
        """
        cls.__hint = GUIText(f"", 15, font, [0.7, 0.8], 0.3, False)
        cls.__hint.set_color(1, 1, 1)
        cls.__hint.set_border_width(0.7)
        cls.__hint.set_offset([0.003, 0.003])

    @classmethod
    def render(cls) -> None:
        """Renders the key hints on the screen."""
        TextMaster.render_specified([cls.__hint])

    @classmethod
    def set_text(cls, text: str) -> None:
        """Sets the text of the key hint.

        :param text: The string to be displayed as the hint.
        """
        cls.__hint.set_text_string(text)

    @classmethod
    def remove_text(cls) -> None:
        """Removes the displayed text from the key hint."""
        cls.__hint.set_text_string("")
