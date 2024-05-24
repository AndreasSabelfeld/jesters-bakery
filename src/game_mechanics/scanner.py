from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.toolbox.raycaster import ObjectRaycaster
from src.game_mechanics.game_object import GameObject


class Scanner:

    def __init__(self, object_picker: ObjectRaycaster, loader):
        self.__object_picker = object_picker
        self.__name = str()
        self.__prompt = str()
        self.__info = str()

        font = FontType(loader.load_texture("candara"), "res/candara.fnt")
        self.__text = GUIText("", 15, font, [0.5, 0.5], 0.5, False)
        self.__text.set_color(1, 1, 1)
        self.__text.set_outline_color(0, 0, 0)
        self.__text.set_border_width(0.5)
        self.__text.set_border_edge(0.1)

    def update(self, collider_entities: list):
        look_at = self.__object_picker.update(collider_entities)
        self.__reset()
        if not isinstance(look_at, GameObject):
            self.__text.set_text_string("")
            return

        if look_at.get_name():
            self.__name = look_at.get_name()
        if look_at.get_prompt():
            self.__prompt = look_at.get_prompt()
        if look_at.get_info():
            self.__info = look_at.get_info()

        msg = f"Name: {self.__name} \nAction: {self.__prompt} \nInfo: {self.__info}"
        self.__text.set_text_string(msg)

    def __reset(self):
        self.__name = str()
        self.__prompt = str()
        self.__info = str()
