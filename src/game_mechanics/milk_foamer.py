from src.entities.entity import Entity
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.game_object import GameObject
from src.guis.gui_texture import GuiTexture
from src.models.textured_model import TexturedModel
from src.render_engine.input_controller import KeyboardInputListener, UniversalInputListener
from src.render_engine.time import Time
from src.textures.model_texture import ModelTexture
from src.toolbox.path import PATH


class MilkFoamer:

    def __init__(self, milk_foamer: GameObject, render_target, loader, obj_loader, fbo, gui_renderer, object_picker):
        """
        Initializes the MilkFoamer with the necessary parameters for rendering and stuff.

        :param milk_foamer: The GameObject of the milk foamer.
        :param render_target: The render target for displaying the milk foamer's output.
        :param loader: The Loader instance
        :param obj_loader: The object loader
        :param fbo: The frame buffer object for rendering textures
        :param gui_renderer: The GUI renderer
        :param object_picker: The object picker for detecting interactions with the milk foamer.
        """
        self.__milk_foamer = milk_foamer
        self.__milk_foamer_vessel = self.__milk_foamer.get_child_1()
        self.__render_target = render_target
        self.__interaction_key = b'f'
        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__fbo = fbo
        self.__gui_renderer = gui_renderer
        self.__object_picker = object_picker

        self.__text = GUIText("", 132, FontType(self.__loader.load_texture("fnts/clock"), f"{PATH}/res/fnts/clock.fnt"), [0, 0.2], 1, True)
        self.__black_texture = GuiTexture(self.__loader.load_texture("pngs/machinery/black"), [0, 0], [1920, 1080])
        self.__text.set_color(1, 1, 1)
        self.__text.set_border_width(0.7)
        self.__text.set_border_edge(0.1)
        self.__lid_closed = True
        self.__cup_placed = True
        self.__is_brewing = False
        self.__is_finished = False
        self.__fill_lvl = 0
        self.__max_fill_lvl = 3
        self.__fill_cooldown = 0.0
        self.__brewing_time = 30.0
        self.__processed_fill_texture = ModelTexture(loader.load_texture("pngs/cups/milk_foam_filling_tex"))
        self.__content = list()

        self.__listener = UniversalInputListener()

    def update(self) -> None:
        """
        Updates the state of the milk foamer, handling interactions, brewing time,
        and displaying the current status.
        """
        self.interact()
        self.display()
        if self.__fill_cooldown > 0.0:
            self.__fill_cooldown -= Time.get_delta_time()
        else:
            self.__fill_cooldown = 0.0
        if self.__is_brewing:
            if self.__brewing_time > 0.0:
                self.__brewing_time -= Time.get_delta_time()
            else:
                self.__brewing_time = 0.0
                self.__is_brewing = False
                self.__finished()
            self.__text.set_text_string(f"{self.__brewing_time:.2f}")

    def interact(self) -> None:
        """
        Handles user interaction with the milk foamer.
        """
        if self.__listener.get_interact() and not self.__is_finished and not self.__is_brewing:
            collision = self.__object_picker.update([self.__milk_foamer])
            if collision == self.__milk_foamer and self.__fill_lvl == self.__max_fill_lvl:
                if self.__cup_placed and self.__lid_closed:
                    self.__is_brewing = True
                    self.__brewing_time = 30.0

    def fill(self, texture: ModelTexture) -> None:
        """
        Fills the milk foamer vessel with the specified texture. Increments the fill level
        and sets a cooldown for the next fill operation.

        :param texture: The texture to be used for filling the vessel.
        """
        if self.__fill_cooldown == 0.0 and self.__fill_lvl < self.__max_fill_lvl:
            entity = Entity(self.get_fill_model(self.__fill_lvl, texture),
                            self.__milk_foamer_vessel.get_position(), 0, 0, 0, 1)
            self.__milk_foamer_vessel.set_child_1(entity)
            self.__fill_lvl += 1
            self.__fill_cooldown = 1.5

    def empty(self) -> None:
        """
        Empties the milk foamer vessel, resetting the fill level.
        """
        self.__milk_foamer_vessel.remove_child_1()
        self.__fill_lvl = 0

    def display(self) -> None:
        """
        Displays the current status of the milk foamer using the GUI renderer.
        Renders the black texture and the current brewing time as text.
        """
        self.__fbo.bind_frame_buffer()
        guis = [self.__black_texture]
        self.__gui_renderer.render(guis)
        TextMaster.render_specified([self.__text])
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def __finished(self) -> None:
        """
        Ends the brewing process, creating an entity with the filled texture
        and appending content to the milk foamer.
        """
        entity = Entity(self.get_fill_model(self.__fill_lvl, self.__processed_fill_texture),
                        self.__milk_foamer_vessel.get_position(), 0, 0, 0, 1)
        # child_1 = cup
        # child_1.child_1 = filling
        self.__milk_foamer_vessel.set_child_1(entity)
        self.append_content("Foam")

    def get_lid_closed(self) -> bool:
        """
        Checks if the lid of the milk foamer is closed.

        :return: True if the lid is closed, False otherwise.
        """
        return self.__lid_closed

    def set_lid_closed(self, closed: bool) -> None:
        """
        Sets the state of the lid (open or closed).

        :param closed: True to close the lid, False to open it.
        """
        self.__lid_closed = closed

    def get_cup_placed(self) -> bool:
        """
        Checks if the cup is placed on the milk foamer.

        :return: True if the cup is placed, False otherwise.
        """
        return self.__cup_placed

    def set_cup_placed(self, placed: bool) -> None:
        """
        Sets the state of the cup (placed or removed).

        :param placed: True if the cup is placed, False if removed.
        """
        self.__cup_placed = placed

    def get_fill_model(self, level, texture) -> TexturedModel:
        """
        returns the fill model for the specified level and texture.

        :param level: The fill level of the milk foamer.
        :param texture: The texture to apply to the fill model.
        :return: A TexturedModel of the fill model.
        """
        return TexturedModel(self.__obj_loader.load_obj_model(f"objs/machinery/milk_foamer_lvl_{level}", self.__loader), texture)

    def get_text(self) -> GUIText:
        """
        returns the GUI text displaying the brewing time.

        :return: The GUIText instance used for displaying text.
        """
        return self.__text

    def get_is_brewing(self) -> bool:
        """
        Checks if the milk foamer is currently brewing.

        :return: True if brewing, False otherwise.
        """
        return self.__is_brewing

    def append_content(self, content: str | list) -> None:
        """
        Appends content to the milk foamer's content list, ensuring no duplicates are added.

        :param content: The content to append, which can be a string or a list of strings.
        """
        if self.__content and self.__content[-1] == content:
            return
        if isinstance(content, str):
            self.__content.append(content)
        elif isinstance(content, list):
            self.__content.extend(content)

    def remove_content(self) -> list:
        """
        Removes and returns the current content of the milk foamer.

        :return: A list of the content that was removed.
        """
        c = self.__content.copy()
        self.__content = []
        return c

    def get_content(self) -> list:
        """
        returns a copy of the current content of the milk foamer.

        :return: A list of the current content.
        """
        return self.__content.copy()

    def get_texture(self) -> ModelTexture:
        """
        returns the texture used for the processed fill.

        :return: The ModelTexture of the processed fill texture.
        """
        return self.__processed_fill_texture

    def get_fill_lvl(self) -> int:
        """
        returns the current fill level of the milk foamer.

        :return: The current fill level.
        """
        return self.__fill_lvl

    def get_render_target(self) -> Entity:
        """
        returns the render target entity for the milk foamer.

        :return: The Entity used as the render target.
        """
        return self.__render_target
