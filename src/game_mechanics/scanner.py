from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.guis.gui_texture import GuiTexture
from src.render_engine.gui_renderer import GuiRenderer
from src.toolbox.raycaster import ObjectRaycaster
from src.game_mechanics.game_object import GameObject
from src.toolbox.path import PATH


class Scanner:

    def __init__(self, object_picker: ObjectRaycaster, loader, gui_renderer: GuiRenderer):
        """
        Initializes the Scanner with object picker, loader, and GUI renderer.

        :param object_picker: An instance of ObjectRaycaster used to detect objects.
        :param loader: Loader instance
        :param gui_renderer: GuiRenderer instance.
        """
        self.__object_picker = object_picker
        self.__name = str()
        self.__prompt = str()
        self.__info = str()

        font = FontType(loader.load_texture("fnts/prompt_font"), f"{PATH}/res/fnts/prompt_font.fnt")
        self.__text = GUIText("", 15, font, [0.05, 0.8], 0.5, False)
        self.__text.set_color(1, 1, 1)
        self.__text.set_outline_color(0, 0, 0)
        self.__text.set_border_width(0.5)
        self.__text.set_border_edge(0.1)

        self.__gui_renderer = gui_renderer
        self.__interactable = False
        self.__crosshair = GuiTexture(loader.load_texture("pngs/ui/crosshair010"), [0, 0], [0.033, 0.06])
        self.__crosshair_interact = GuiTexture(loader.load_texture("pngs/ui/crosshair187"), [0, 0], [0.033, 0.06])

    def render_crosshair(self) -> None:
        """
        Renders the crosshair based on interactability.
        """
        if self.__interactable:
            self.__gui_renderer.render([self.__crosshair_interact])
        else:
            self.__gui_renderer.render([self.__crosshair])

    def update(self, collider_entities: list) -> None:
        """
        Updates the scanner by checking if any objects are in sight and returns information about them.

        :param collider_entities: List of entities that the scanner might detect.
        """
        look_at = self.__object_picker.update(collider_entities)
        self.__reset()
        if not isinstance(look_at, GameObject):
            self.__text.set_text_string("")
            return

        self.__interactable = True
        msg = ""
        if look_at.get_ext_name():
            self.__name = look_at.get_ext_name()
            msg += self.__name + ' \n'
        if look_at.get_prompt():
            self.__prompt = look_at.get_prompt()
            msg += self.__prompt + ' \n'
        if look_at.get_info():
            self.__info = "Content: " + str(look_at.get_info())
            msg += self.__info + ' \n'

        self.__text.set_text_string(msg)

    def get_text(self) -> GUIText:
        """
        Returns the GUIText object used to display information.

        :return: The GUIText object.
        """
        return self.__text

    def __reset(self) -> None:
        """
        Resets the scanner's name, prompt, info, and interactability.
        """
        self.__name = str()
        self.__prompt = str()
        self.__info = str()
        self.__interactable = False
