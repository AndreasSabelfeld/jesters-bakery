from OpenGL.GLUT import *

from src.audio.audio_master import AudioMaster
from src.audio.source import Source
from src.entities.camera import Camera
from src.entities.player import ThirdPersonPlayer, FirstPersonPlayer
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.guis.gui_texture import GuiTexture
from src.master.levels import Levels
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.input_controller import KeyboardInput, Binds, UniversalInput
from src.render_engine.loader import Loader
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.time import Time


class UI:
    NO_SCREEN = -1
    LOADING_SCREEN = 0
    MAIN_MENU = 1
    GAME_LOOP = 2

    def __init__(self, loader: Loader, gui_renderer: GuiRenderer, level_master: Levels, display: DisplayManager, sfx_source: Source,
                 player: FirstPersonPlayer, camera: Camera):
        self.__time_zero = Time.time_current_time()
        self.__loader = loader
        self.__gui_renderer = gui_renderer
        self.__level_master = level_master
        self.__display = display
        self.__sfx_source = sfx_source
        self.__player = player
        self.__camera = camera
        self.__clear_tex = GuiTexture(self.__loader.load_texture("pngs/machinery/black"), [0, 0], [1920, 1080])
        self.__current_screen = self.NO_SCREEN
        self.__current_texts = list()
        self.__current_textures = list()
        self.__menu_scroll = AudioMaster.load_sound("res/audio/menu_scroll.wav")
        self.__select = AudioMaster.load_sound("res/audio/menu_selected.wav")

    def render(self) -> None:
        self.__gui_renderer.render(self.__current_textures)
        TextMaster.render_specified(self.__current_texts)

        glutSwapBuffers()       # needs to be called AFTER finished drawing
        glutMainLoopEvent()     # used to run openGL manually in a loop instead of glutMainLoop()

    def clear(self) -> None:
        self.__gui_renderer.render([self.__clear_tex])

    def loading_screen(self, elapsed_time: float) -> None:
        self.__current_texts.clear()
        self.__current_textures.clear()
        self.clear()
        loading_time = 30000
        percentage = ((elapsed_time - self.__time_zero) / loading_time) * 100
        if percentage > 100:
            percentage = 100

        font = FontType(self.__loader.load_texture("fnts/joystix"), "res/fnts/joystix.fnt")
        text = GUIText(f"LOADING... \n{percentage:.2f}% DONE", 15, font, [0, 0.5], 1, True)
        text.set_color(1, 1, 1)
        text.set_border_width(0.7)
        text.set_border_edge(0.1)

        self.__current_texts.append(text)
        self.render()

    def main_menu(self, master_renderer: MasterRenderer, entities: list, nm_entities: list, terrains: list, lights: list,
                  sm_entities: list, sun) -> None:
        self.__current_texts.clear()
        self.__current_textures.clear()

        selected_item = 0

        font = FontType(self.__loader.load_texture("fnts/lonely_coffee"), "res/fnts/lonely_coffee.fnt")
        title_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item4"), [0, 0.6], [0.6, 0.4])
        title_text = GUIText(f"Jester's Bakery", 35, font, [0, 0.08], 1, True)
        title_text.set_color(1, 1, 1)
        title_text.set_border_width(0.7)
        title_text.set_offset([0.003, 0.003])

        item_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item3"), [0, -0.25], [0.33, 0.5])
        item_1 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, 0], [0.25, 0.10])
        item_1_text = GUIText(f"Start Game", 20, font, [0, 0.47], 1, True)
        item_1_text.set_color(1, 1, 1)
        item_1_text.set_border_width(0.7)
        item_1_text.set_offset([0.003, 0.003])

        item_2 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.25], [0.25, 0.10])
        item_2_text = GUIText(f"Options", 20, font, [0, 0.6], 1, True)
        item_2_text.set_color(1, 1, 1)
        item_2_text.set_border_width(0.7)
        item_2_text.set_offset([0.003, 0.003])

        item_3 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.5], [0.25, 0.10])
        item_3_text = GUIText(f"Exit Game", 20, font, [0, 0.72], 1, True)
        item_3_text.set_color(1, 1, 1)
        item_3_text.set_border_width(0.7)
        item_3_text.set_offset([0.003, 0.003])

        icon_right = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Right"), [-0.3, 0], [0.04, 0.1])

        items = [item_1_text, item_2_text, item_3_text]
        self.__current_textures = [title_bg, item_bg, item_1, item_2, item_3, icon_right]
        self.__current_texts = [title_text, *items]

        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()  # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        self.__camera.set_position([200, 19.18, 260])
        self.__camera.set_yaw(-90)
        direction = 1

        while True:
            Time.set_current_time(Time.time_current_time())
            Time.set_delta_time()  # automatically calculates delta time
            Time.set_last_frame_time(Time.time_current_time())

            if self.__camera.get_position()[2] >= 260:
                direction = -2 * Time.get_delta_time()
            elif self.__camera.get_position()[2] <= 75:
                direction = 2 * Time.get_delta_time()

            self.__camera.get_position()[2] += direction

            # because of some reason the camera doesn't move except when something is printed, so I'm printing an
            # empty string
            print(end='')

            if UniversalInput.get_up():
                if selected_item > 0:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item -= 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] + 0.25])
            if UniversalInput.get_down():
                if selected_item < 2:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item += 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] - 0.25])
            if UniversalInput.get_confirm():  # enter key
                self.__sfx_source.play(self.__select)
                if selected_item == 0:
                    return
                if selected_item == 1:
                    self.options_menu()
                if selected_item == 2:
                    self.__display.destroy_window()
                    return

            items[selected_item].set_color(250 / 255, 218 / 255, 94 / 255)
            master_renderer.render_shadow_map(sm_entities, sun)
            master_renderer.render_scene(entities, nm_entities, terrains, lights, self.__camera, self.__display)
            self.render()

    def options_menu(self) -> bool:
        old_texts = self.__current_texts.copy()
        old_textures = self.__current_textures.copy()
        self.__current_texts.clear()
        self.__current_textures.clear()

        selected_item = 0

        font = FontType(self.__loader.load_texture("fnts/lonely_coffee"), "res/fnts/lonely_coffee.fnt")

        item_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item3"), [0, -0.25], [0.33, 0.5])
        item_1 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, 0], [0.25, 0.10])
        item_1_text = GUIText(f"Reset Character", 20, font, [0, 0.47], 1, True)
        item_1_text.set_color(1, 1, 1)
        item_1_text.set_border_width(0.7)
        item_1_text.set_offset([0.003, 0.003])

        item_2 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.25], [0.25, 0.10])
        item_2_text = GUIText(f"Reset Progress", 20, font, [0, 0.6], 1, True)
        item_2_text.set_color(1, 1, 1)
        item_2_text.set_border_width(0.7)
        item_2_text.set_offset([0.003, 0.003])

        item_3 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.5], [0.25, 0.10])
        item_3_text = GUIText(f"Return", 20, font, [0, 0.72], 1, True)
        item_3_text.set_color(1, 1, 1)
        item_3_text.set_border_width(0.7)
        item_3_text.set_offset([0.003, 0.003])

        icon_right = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Right"), [-0.3, 0], [0.04, 0.1])

        items = [item_1_text, item_2_text, item_3_text]
        self.__current_textures = [item_bg, item_1, item_2, item_3, icon_right]
        self.__current_texts = [*items]

        while True:
            Time.set_current_time(Time.time_current_time())
            Time.set_delta_time()  # automatically calculates delta time
            Time.set_last_frame_time(Time.time_current_time())

            if UniversalInput.get_up():
                if selected_item > 0:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item -= 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] + 0.25])
            if UniversalInput.get_down():
                if selected_item < 2:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item += 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] - 0.25])
            if UniversalInput.get_confirm():  # enter key
                self.__sfx_source.play(self.__select)
                if selected_item == 0:
                    self.__camera.set_position([160.5, 5.18, 180])
                    self.__player.set_position([160.5, 5.18, 180])
                    self.__current_texts = old_texts
                    self.__current_textures = old_textures
                    return True
                if selected_item == 1:
                    self.__level_master._write_save(1)
                    self.__level_master._load_save()
                if selected_item == 2:
                    self.__current_texts = old_texts
                    self.__current_textures = old_textures
                    return False

            items[selected_item].set_color(250 / 255, 218 / 255, 94 / 255)
            self.render()

    def game_loop(self) -> None:
        self.__current_texts.clear()
        self.__current_textures.clear()

        font = FontType(self.__loader.load_texture("fnts/lonely_coffee"), "res/fnts/lonely_coffee.fnt")
        title_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item4"), [0, 0.74], [0.3, 0.2])
        day = GUIText(f"Day: {self.__level_master.get_current_lvl()}", 32, font, [0, 0.05], 1, True)
        day.set_color(1, 1, 1)
        day.set_border_width(0.7)
        day.set_offset([0.003, 0.003])

        prompt_font = FontType(self.__loader.load_texture("fnts/prompt_font"), "res/fnts/prompt_font.fnt")
        menu_icon = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Menu"), [-0.9, 0.8], [0.05, 0.075])
        hint = GUIText(f"{Binds.get_bind(Binds.OPTIONS)}", 24, prompt_font, [0.08, 0.05], 1, False)
        hint.set_color(1, 1, 1)
        hint.set_border_width(0.7)
        hint.set_offset([0.003, 0.003])

        if self.__level_master.get_count_down():
            count_down = GUIText(f"Game starts in: {self.__level_master.get_count_down():.0f} seconds", 25, font, [0, 0.5], 1, True)
        else:
            count_down = GUIText(f"", 25, font, [0, 0.5], 1, True)

            for i in range(self.__level_master.get_current_order() + 1):
                text_x = 0.82
                text_y = 0.1 + i / 10
                text_offset = -0.017
                texture_y = 1 - (text_y * 2)
                text = GUIText(f"Order {i + 1}: {self.__level_master.get_orders()[i].get_time():.0f} sec", 12, font, [text_x, text_y + text_offset], 1, False)
                text.set_color(1, 1, 1)
                text.set_border_width(0.7)
                text.set_offset([0.003, 0.003])
                self.__current_textures.append(GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item2"), [0.8, texture_y], [0.2, 0.08]))
                self.__current_textures.append(GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Write"), [0.6, texture_y], [0.0375, 0.0675]))
                self.__current_texts.append(text)

        count_down.set_color(1, 1, 1)
        count_down.set_border_width(0.7)
        count_down.set_offset([0.003, 0.003])
        self.__current_texts.extend([day, count_down, hint])
        self.__current_textures.extend([title_bg, menu_icon])

        if UniversalInput.get_options():  # ESC key
            self.pause_menu()

    def pause_menu(self) -> None:
        self.__current_texts.clear()
        self.__current_textures.clear()

        selected_item = 0

        font = FontType(self.__loader.load_texture("fnts/lonely_coffee"), "res/fnts/lonely_coffee.fnt")
        title_text = GUIText(f"Paused", 35, font, [0, 0.25], 1, True)
        title_text.set_color(1, 1, 1)
        title_text.set_border_width(0.7)
        title_text.set_offset([0.003, 0.003])

        item_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item3"), [0, -0.25], [0.33, 0.5])
        item_1 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, 0], [0.25, 0.10])
        item_1_text = GUIText(f"Continue", 20, font, [0, 0.47], 1, True)
        item_1_text.set_color(1, 1, 1)
        item_1_text.set_border_width(0.7)
        item_1_text.set_offset([0.003, 0.003])

        item_2 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.25], [0.25, 0.10])
        item_2_text = GUIText(f"Options", 20, font, [0, 0.6], 1, True)
        item_2_text.set_color(1, 1, 1)
        item_2_text.set_border_width(0.7)
        item_2_text.set_offset([0.003, 0.003])

        item_3 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.5], [0.25, 0.10])
        item_3_text = GUIText(f"Exit Game", 20, font, [0, 0.72], 1, True)
        item_3_text.set_color(1, 1, 1)
        item_3_text.set_border_width(0.7)
        item_3_text.set_offset([0.003, 0.003])

        icon_right = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Right"), [-0.3, 0], [0.04, 0.1])

        items = [item_1_text, item_2_text, item_3_text]
        self.__current_textures = [item_bg, item_1, item_2, item_3, icon_right]
        self.__current_texts = [title_text, *items]

        while True:
            Time.set_current_time(Time.time_current_time())
            Time.set_delta_time()  # automatically calculates delta time
            Time.set_last_frame_time(Time.time_current_time())

            if UniversalInput.get_up():
                if selected_item > 0:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item -= 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] + 0.25])
            elif UniversalInput.get_down():
                if selected_item < 2:
                    self.__sfx_source.play(self.__menu_scroll)
                    items[selected_item].set_color(1, 1, 1)
                    selected_item += 1
                    icon_right.set_position([icon_right.get_position()[0], icon_right.get_position()[1] - 0.25])
            elif UniversalInput.get_confirm():
                self.__sfx_source.play(self.__select)
                if selected_item == 0:
                    return
                if selected_item == 1:
                     if self.options_menu():
                         return
                if selected_item == 2:
                    self.__display.destroy_window()
                    return
            elif UniversalInput.get_options():
                return

            items[selected_item].set_color(250 / 255, 218 / 255, 94 / 255)
            self.render()

    def level_complete(self) -> None:
        self.__current_texts.clear()
        self.__current_textures.clear()
        points = self.__level_master.get_total_points()

        font = FontType(self.__loader.load_texture("fnts/lonely_coffee"), "res/fnts/lonely_coffee.fnt")

        title_bg = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item4"), [0, 0.5], [0.45, 0.3])
        title_text = GUIText(f"Level Complete!", 35, font, [0, 0.4], 1, True)
        title_text.set_color(1, 1, 1)
        title_text.set_border_width(0.7)
        title_text.set_offset([0.003, 0.003])

        points_text = GUIText(f"Your Points: {points}", 16, font, [0, 0.6], 1, True)
        points_text.set_color(1, 1, 1)
        points_text.set_border_width(0.7)
        points_text.set_offset([0.003, 0.003])

        item_2 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Item5"), [0, -0.65], [0.25, 0.10])
        item_2_text = GUIText(f"Next Day", 20, font, [0, 0.8], 1, True)
        item_2_text.set_color(1, 1, 1)
        item_2_text.set_border_width(0.7)
        item_2_text.set_offset([0.003, 0.003])

        if -1 >= self.__level_master.get_goal_points():
            star_1 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Star"), [-0.25, 0.6], [0.12, 0.2])
            star_2 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Star"), [0, 0.7], [0.12, 0.2])
            star_3 = GuiTexture(self.__loader.load_texture("pngs/ui/PenzillaUI/Icon_Star"), [0.25, 0.6], [0.12, 0.2])

            self.__current_textures = [title_bg, star_1, star_2, star_3, item_2]
            self.__current_texts = [title_text, item_2_text, points_text]
        else:
            title_text.set_text_string("Level Failed!")
            title_text.set_position([0, 0.15])
            points_text.set_text_string(f"Your Points: {points} \nPoints needed: {self.__level_master.get_goal_points()}")
            item_2_text.set_text_string("Restart Day")

            self.__current_textures = [title_bg, item_2]
            self.__current_texts = [title_text, item_2_text, points_text]

        while True:
            Time.set_current_time(Time.time_current_time())
            Time.set_delta_time()  # automatically calculates delta time
            Time.set_last_frame_time(Time.time_current_time())

            if UniversalInput.get_confirm():  # enter key
                return
            self.render()
