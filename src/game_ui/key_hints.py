from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.render_engine.loader import Loader


class KeyHints:
    __hint = None

    def __init__(self, loader: Loader):
        self.__loader = loader

        self.__prompt_font = FontType(self.__loader.load_texture("fnts/prompt_font"), "res/fnts/prompt_font.fnt")
        KeyHints.__load_text(self.__prompt_font)

    @classmethod
    def __load_text(cls, font) -> None:
        cls.__hint = GUIText(f"", 15, font, [0.7, 0.8], 0.3, False)
        cls.__hint.set_color(1, 1, 1)
        cls.__hint.set_border_width(0.7)
        cls.__hint.set_offset([0.003, 0.003])

    @classmethod
    def render(cls) -> None:
        TextMaster.render_specified([cls.__hint])

    @classmethod
    def set_text(cls, text: str) -> None:
        cls.__hint.set_text_string(text)

    @classmethod
    def remove_text(cls) -> None:
        cls.__hint.set_text_string("")
