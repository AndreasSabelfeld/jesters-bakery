from OpenGL.GL import *

from src.entities.entity import Entity
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.game_object import GameObject
from src.guis.gui_texture import GuiTexture
from src.models.textured_model import TexturedModel
from src.render_engine.input_controller import KeyboardInputListener
from src.render_engine.time import Time
from src.textures.model_texture import ModelTexture


class MilkFoamer:

    def __init__(self, milk_foamer: GameObject, render_target, loader, obj_loader, fbo, gui_renderer, object_picker):
        self.__milk_foamer = milk_foamer
        self.__render_target = render_target
        self.__interaction_key = b'f'
        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__fbo = fbo
        self.__gui_renderer = gui_renderer
        self.__object_picker = object_picker

        self.__text = GUIText("", 216, FontType(self.__loader.load_texture("candara"), "res/candara.fnt"), [0, 0.2], 1, True)
        self.__black_texture = GuiTexture(self.__loader.load_texture("black"), [0, 0], [1920, 1080])
        self.__text.set_color(1, 0, 0)
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
        self.__processed_fill_texture = ModelTexture(loader.load_texture("grass_block"))
        self.__content = list()

        self.__listener = KeyboardInputListener()

    def update(self):
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
        if self.__listener.on_key_down(self.__interaction_key) and not self.__is_finished and not self.__is_brewing:
            collision = self.__object_picker.update([self.__milk_foamer])
            if collision == self.__milk_foamer and self.__fill_lvl == self.__max_fill_lvl:
                if self.__cup_placed and self.__lid_closed:
                    self.__is_brewing = True
                    self.__brewing_time = 30.0

    def fill(self, texture: ModelTexture) -> None:
        if self.__fill_cooldown == 0.0 and self.__fill_lvl < self.__max_fill_lvl:
            entity = Entity(self.get_fill_model(self.__fill_lvl, texture),
                            self.__milk_foamer.get_child_1().get_position(), 0, 0, 0, 1)
            self.__milk_foamer.get_child_1().set_child_1(entity)
            self.__fill_lvl += 1
            self.__fill_cooldown = 1.5

    def empty(self) -> None:
        self.__milk_foamer.get_child_1().remove_child_1()
        self.__fill_lvl = 0

    def display(self) -> None:
        self.__fbo.bind_frame_buffer()
        guis = [self.__black_texture]
        self.__gui_renderer.render(guis)
        TextMaster.render_specified([self.__text])
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def __finished(self):
        entity = Entity(self.get_fill_model(self.__fill_lvl, self.__processed_fill_texture),
                        self.__milk_foamer.get_child_1().get_position(), 0, 0, 0, 1)
        # child_1 = cup
        # child_1.child_1 = filling
        self.__milk_foamer.get_child_1().set_child_1(entity)
        self.append_content("Foam")

    def get_lid_closed(self) -> bool:
        return self.__lid_closed

    def set_lid_closed(self, closed: bool) -> None:
        self.__lid_closed = closed

    def get_cup_placed(self) -> bool:
        return self.__cup_placed

    def set_cup_placed(self, placed: bool) -> None:
        self.__cup_placed = placed

    def get_fill_model(self, level, texture) -> TexturedModel:
        return TexturedModel(self.__obj_loader.load_obj_model(f"milk_foamer_lvl_{level}", self.__loader), texture)

    def get_text(self) -> GUIText:
        return self.__text

    def get_is_brewing(self) -> bool:
        return self.__is_brewing

    def append_content(self, content: str | list) -> None:
        if self.__content and self.__content[-1] == content:
            return
        if isinstance(content, str):
            self.__content.append(content)
        elif isinstance(content, list):
            self.__content.extend(content)

    def remove_content(self) -> list:
        c = self.__content.copy()
        self.__content = []
        return c

    def get_content(self) -> list:
        return self.__content.copy()

    def get_texture(self):
        return self.__processed_fill_texture

    def get_fill_lvl(self) -> int:
        return self.__fill_lvl
