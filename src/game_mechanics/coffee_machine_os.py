import math
from time import sleep
from threading import Thread
from src.render_engine.input_controller import KeyboardInput, ControllerInput, KeyboardInputListener, UniversalInput, \
    UniversalInputListener
from src.render_engine.time import Time
from src.game_mechanics.coffee_product import CoffeeProduct, CoffeeProductLactoseFree
from src.game_mechanics.coffee_page import CoffeePage, CoffeePageLactoseFree
from src.guis.gui_texture import GuiTexture
from src.textures.model_texture import ModelTexture
from src.font_rendering.text_master import TextMaster
from src.font_mesh_creator.gui_text import GUIText
from src.font_mesh_creator.font_type import FontType
from src.pycgtypes import vec3, mat3


class CoffeeMachineOS:

    BACKGROUND_TEXTURE_SIZE = [1920, 1080]
    __NAME = "COFFEE_MACHINE"

    def __init__(self, render_target, loader, obj_loader, fbo, gui_renderer, object_picker) -> None:
        """
        Creates new CoffeeMachineOS instance.

        :param render_target: The object the screen texture should be rendered on
        :param loader: The Loader object
        :param fbo: The FBO object
        :param gui_renderer: the GuiRendered object
        """
        self.__render_target = render_target
        self.__is_interacting = False
        self.__original_camera_pos = None
        self.__original_camera_angles = None

        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__fbo = fbo
        self.__gui_renderer = gui_renderer
        self.__object_picker = object_picker

        self.__icon_offset = 0.25
        self.__text_offset = 0.04
        self.__icon_size = 0.125
        self.__rows = 4
        self.__size_adjustment = 2
        self.__columns = self.__rows
        self.__background_texture = GuiTexture(loader.load_texture("pngs/ui/coffee_machine_background"), [0, 0], [1, 1])
        self.__selected_texture = GuiTexture(loader.load_texture("pngs/ui/selected"), [0, 0], [self.__icon_size * 1.1,
                                                                                                      self.__icon_size * 1.1])
        self.__cancel_texture = GuiTexture(loader.load_texture("pngs/ui/delete"), [-2, -2], [0.06, 0.06])
        self.__start_texture = GuiTexture(loader.load_texture("pngs/ui/confirm"), [-2, -2], [0.05, 0.05])
        self.__decaffeinated_texture = GuiTexture(loader.load_texture("pngs/ui/coffee_beans"), [-2, -2], [self.__icon_size, self.__icon_size])
        self.__decaffeinated_texture.set_position([(self.__icon_offset + 1 / (5 + self.__size_adjustment) * 2 * 5) - 1,
                                                   1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * 0)])
        self.__deactivated_texture = GuiTexture(loader.load_texture("pngs/ui/deactivated"), [-2, -2], [self.__icon_size, self.__icon_size])

        self.__selected_position = [0, 0]  # x y, top-left corner is 0, 0
        self.__current_page = 0
        self.__product_entries = None
        self.__create_products()
        self.__time_remaining = GUIText("", 18,
                                        FontType(self.__loader.load_texture("fnts/arial"), "res/fnts/arial.fnt"),
                                        [0.07, 0.75], 1, False)
        self.__time_remaining.set_color(250 / 255, 218 / 255, 94 / 255)
        self.__time_remaining.set_border_width(0.7)
        self.__time_remaining.set_border_edge(0.1)
        self.__time_passed = 0
        self.__coffee_buffer = False
        self.__coffee_texture = None
        self.__tea_buffer = False
        self.__tea_texture = None
        self.__max_level = 3
        self.__brewing_coffee = False
        self.__brewing_tea = False
        self.__decaffeinated = False
        self.__texts = self.get_page_texts()

        self.__positioned_coffees = [None, None, None]      # tea, coffee1, coffee2
        y, x = 0.35, 2.1
        self.__offset_positions = (vec3(x, y, 0.75) * self.__render_target.get_scale(),
                                   vec3(x, y, 0) * self.__render_target.get_scale(),
                                   vec3(x, y, -0.25) * self.__render_target.get_scale(),
                                   vec3(x, y, 0.25) * self.__render_target.get_scale())

        self.__brewing_queue = []
        self.__max_queue_length = 7

        self.__listener = UniversalInputListener()

    def render_screen(self) -> None:
        self.__update_time_remaining()
        self.__check_bools()
        self.__move_cursor()
        self.__fbo.bind_frame_buffer()
        guis = [self.__background_texture]
        self.__update_positions_of_products()
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        guis.extend([product.get_icon() for product in self.__product_entries])
        guis.extend([product.get_icon() for product in self.__brewing_queue])
        guis.extend([self.__selected_texture, self.__cancel_texture, self.__start_texture, self.__decaffeinated_texture,
                     self.__deactivated_texture])
        self.__gui_renderer.render(guis)
        self.__texts = self.get_page_texts()
        TextMaster.render_specified(self.__texts)
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def interact(self, player, camera) -> None:
        if self.__listener.get_interact() or self.__listener.get_deny():
            collision = self.__object_picker.update([self.__render_target])
            if self.__is_interacting:
                self.__is_interacting = False
                player.set_player_under_control(True)
                self.__move_camera_to_original_pos(camera)
            elif collision == self.__render_target:
                self.__is_interacting = True
                player.set_player_under_control(False)
                self.__move_in_front_screen(camera)

    def get_is_interacting(self) -> bool:
        return self.__is_interacting

    def get_page_texts(self) -> list:
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        texts = [product.get_text() for product in self.__product_entries]
        texts.append(self.__time_remaining)
        return texts

    def get_all_texts(self) -> list:
        texts = CoffeeProduct.all_texts.copy()
        texts.append(self.__time_remaining)
        return texts

    def get_icon_size(self) -> float:
        return self.__icon_size

    def get_text_offset(self) -> float:
        return self.__text_offset

    def set_coffee(self, index: int, entity) -> None:
        if index <= 2:
            self.__positioned_coffees[index] = entity
            match index:
                case 0: entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                case 1: entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                case 2:
                    self.get_coffee(1).set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                    entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index + 1])

    def get_coffee(self, index: int):
        if index <= 2:
            return self.__positioned_coffees[index]

    def get_coffee_list(self) -> list:
        """Returns a copy of the list of coffees"""
        return self.__positioned_coffees.copy()

    def remove_coffee(self, index: int):
        if index <= 2:
            self.__positioned_coffees[index] = None
            if self.get_coffee(1) is None and self.get_coffee(2) is not None:
                self.set_coffee(1, self.get_coffee(2))
                self.remove_coffee(2)
            if self.get_coffee(2) is None and self.get_coffee(1) is not None:
                self.get_coffee(1).set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[1])

    @classmethod
    def get_name(cls) -> str:
        return cls.__NAME

    def get_fbo(self):
        return self.__fbo

    def is_brewing_coffee(self) -> bool:
        return self.__brewing_coffee

    def is_brewing_tea(self) -> bool:
        return self.__brewing_tea

    def __move_cursor(self) -> None:
        """Updates the cursor of the coffee machine. Method is being called from the render_screen method."""
        if self.__is_interacting:
            if UniversalInput.get_up():
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] = self.__current_page * 4
                self.__selected_position[1] -= 1 if self.__selected_position[1] > 0 else 0
            if UniversalInput.get_down():
                self.__selected_position[1] += 1 if self.__selected_position[1] < 5 else 0
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] = 0
            if UniversalInput.get_left():
                if self.__selected_position[1] < 4:
                    self.__selected_position[0] -= 1 if self.__selected_position[0] > -1 else 0
            if UniversalInput.get_right():
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] += 1 if self.__selected_position[0] < self.__max_queue_length - 1 else 0
                elif self.__selected_position[0] < 4 * len(CoffeePage.get_instances()) - 1:
                    self.__selected_position[0] += 1
            if UniversalInput.get_confirm():    # enter key
                if self.__selected_position[1] == 4:
                    self.__remove_beverage_from_queue(self.__selected_position[0])
                elif self.__selected_position[1] == 5:
                    self.__start_making_coffee()
                elif self.__selected_position[0] == -1:
                    if self.__decaffeinated:
                        self.__decaffeinated = False
                    else:
                        self.__decaffeinated = True
                else:
                    index = self.__selected_position[1] * 4 + self.__selected_position[0] % 4
                    if index < len(self.__product_entries):
                        self.__add_beverage_to_queue(self.__product_entries[index])

        if not self.__selected_position[1] >= 4 and not self.__selected_position[0] == -1:
            # page should not change if we are currently deleting products from the queue
            self.__current_page = self.__selected_position[0] // 4

        self.__move_selected_texture()
        self.__move_cancel_button()
        self.__move_start_button()
        self.__move_deactivated()

    def __move_cancel_button(self) -> None:
        # if the fourth row is selected and any product are in queue, the brewing queue cancel button should appear
        if self.__selected_position[1] == 4 and self.__brewing_queue:
            self.__selected_texture.set_position([-2, -2])  # out of bounds
            self.__cancel_texture.set_position([self.__icon_offset * (self.__selected_position[0] + 1) - 0.95, -0.70])
        else:
            # else move the cancel button out of bounds
            self.__cancel_texture.set_position([-2, -2])

    def __move_start_button(self) -> None:
        # if the fifth row is selected and any product are in queue, the brewing queue start button should appear
        if self.__selected_position[1] == 5 and self.__brewing_queue:
            self.__selected_texture.set_position([-2, -2])  # out of bounds
            self.__start_texture.set_position([self.__icon_offset - 0.95, -0.8])
        else:
            # else move the start button out of bounds
            self.__start_texture.set_position([-2, -2])

    def __move_selected_texture(self) -> None:
        if self.__selected_position[0] == -1:
            self.__selected_texture.set_position([(self.__icon_offset + 1 / (5 + self.__size_adjustment) * 2 * 5) - 1,
                                                  1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * 0)])
        else:
            # selected texture loops back from x-position 4 to 1, but internally the position is being counted further
            self.__selected_texture.set_position([(self.__icon_offset + 1 / (self.__rows + self.__size_adjustment) * 2 * (self.__selected_position[0] % 4)) - 1,
                                              1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * self.__selected_position[1])])

    def __move_deactivated(self) -> None:
        if self.__decaffeinated:
            self.__deactivated_texture.set_position([(self.__icon_offset + 1 / (5 + self.__size_adjustment) * 2 * 5) - 1,
                                                  1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * 0)])
        else:
            self.__deactivated_texture.set_position([-2, -2])

    def __check_bools(self):
        if not self.__brewing_queue:
            self.__brewing_coffee = False
            return
        if self.__coffee_buffer:
            self.__coffee_texture = self.__brewing_queue[0].get_texture()
            self.__fill_original_thread(self.__coffee_texture)
            self.__coffee_buffer = False
        if self.__tea_buffer:
            if not self.__tea_texture:
                self.__tea_texture = self.__brewing_queue[0].get_texture()
                # now that the texture is saved, we can remove the tea from the brewing queue
                self.__update_time_remaining()
            self.__fill_tea_original_thread(self.__tea_texture)
            self.__tea_buffer = False

    def __move_in_front_screen(self, camera) -> None:
        self.__original_camera_pos = camera.get_position()
        self.__original_camera_angles = [camera.get_yaw(), camera.get_pitch(), camera.get_roll()]
        x = 3.5 * math.sin(math.radians(self.__render_target.get_rot_y()))
        z = 3.5 * math.cos(math.radians(self.__render_target.get_rot_y()))
        offset = vec3(x, 2.5, z) * self.__render_target.get_scale()

        position = vec3(self.__render_target.get_position()) + offset

        camera.set_position(position)
        camera.set_yaw(-self.__render_target.get_rot_y())
        camera.set_pitch(0)
        camera.set_roll(0)

    def __move_camera_to_original_pos(self, camera) -> None:
        camera.set_yaw(self.__original_camera_angles[0])
        camera.set_pitch(self.__original_camera_angles[1])
        camera.set_roll(self.__original_camera_angles[2])
        camera.set_position(self.__original_camera_pos)

    def __update_positions_of_products(self) -> None:
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        for i, product in enumerate(self.__product_entries):
            product.get_icon().set_position([(self.__icon_offset + 1 / (self.__rows + self.__size_adjustment) * 2 * (i % 4)) - 1,
                                             1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * (i // 4))])
            product.get_text().set_position([(product.get_icon().get_position()[0] + 1) / 2 - self.__icon_size / 2,
                                             (1 - product.get_icon().get_position()[1]) / 2 + self.__text_offset])

    def __add_beverage_to_queue(self, beverage: CoffeeProduct) -> None:
        if len(self.__brewing_queue) >= self.__max_queue_length:
            return
        product = CoffeeProduct(beverage.get_name(),
                                GuiTexture(beverage.get_icon().get_texture(),
                                           [(len(self.__brewing_queue) * self.__icon_size * 2 + self.__icon_offset) - 1, -0.75],
                                           [self.__icon_size * 0.9, self.__icon_size * 0.9]),
                                beverage.get_brew_length(), beverage.get_container_type(),
                                beverage.is_allow_double(), self.__loader, beverage.get_texture(),
                                beverage.get_content(), add_to_coffee_page=False)
        if self.__decaffeinated:
            product.get_content().append("Decaffeinated")
        self.__brewing_queue.append(product)
        self.__start_making_coffee()

    def __remove_beverage_from_queue(self, index: int = 0) -> None:
        if len(self.__brewing_queue) >= index + 1:
            self.__brewing_queue.pop(index)
            self.__update_queue()

    def __update_queue(self) -> None:
        for i in range(len(self.__brewing_queue)):
            self.__brewing_queue[i].get_icon().set_position([(i * self.__icon_size * 2 + self.__icon_offset) - 1, -0.75])

    def __start_making_coffee(self):
        if not self.__brewing_queue:
            return

        if self.__brewing_queue[0].get_container_type() == CoffeeProduct.TEA_POT:
            if not self.__brewing_tea:
                if self.__positioned_coffees[0]:
                    self.__brewing_tea = True
                    self.__positioned_coffees[0].get_attachment().append_content(self.__brewing_queue[0].get_content())
                    process = Thread(target=self.__fill_timing, args=(self.__max_level, True,))
                    process.start()
            return  # if tea is being made, no coffee should be let out

        if self.__brewing_coffee:
            return
        if not self.__positioned_coffees[1]:
            return

        if self.__brewing_queue[0].is_allow_double():
            # is allowed to make to 2 coffees and 2 coffees are placed:
            if self.__positioned_coffees[1] and self.__positioned_coffees[2]:
                process = Thread(target=self.__fill_timing, args=(self.__max_level,))
                process.start()
                # content is split in half
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content()[0])
                self.__positioned_coffees[2].get_attachment().append_content(self.__brewing_queue[0].get_content()[1])
            # is allowed to make to 2 coffees and 1 coffee is placed:
            else:
                process = Thread(target=self.__fill_timing, args=(self.__max_level + 1,))
                process.start()
                # whole content is poured into
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content())
        else:
            # is NOT allowed to make to 2 coffees and 2 coffees are placed:
            if self.__positioned_coffees[1] and self.__positioned_coffees[2]:
                # both coffees are not full
                process = Thread(target=self.__fill_timing, args=(1,))
                process.start()
                # both get a half
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content()[0] + " half")
                self.__positioned_coffees[2].get_attachment().append_content(self.__brewing_queue[0].get_content()[0] + " half")
            # 1 coffee is allowed and 1 is placed
            else:
                process = Thread(target=self.__fill_timing, args=(self.__max_level,))
                process.start()
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content())
        self.__time_remaining.set_text_string(f"time remaining: {self.__brewing_queue[0].get_brew_length()}")
        self.__brewing_coffee = True

    def __fill_timing(self, levels: int, is_tea: bool = False):
        """
        Method running in a parallel thread for the timing. Sets the __tea_buffer or __coffee_buffer to True, which
        is being checked in the render_screen method. This workaround was made because of issues with multithreading
        OpenGL calls.
        """
        self.__time_passed = 0
        waiting_time = self.__brewing_queue[0].get_brew_length() / levels
        if is_tea:
            self.__remove_beverage_from_queue()

        for i in range(levels):
            sleep(waiting_time)
            if is_tea:
                self.__tea_buffer = True
            else:
                self.__coffee_buffer = True
        if is_tea:
            self.__brewing_tea = False
        else:
            self.__brewing_coffee = False

    def __fill_original_thread(self, texture):
        if self.__positioned_coffees[1]:
            self.__positioned_coffees[1].get_attachment().fill(texture)
            if self.__positioned_coffees[1].get_attachment().get_level() == self.__max_level:
                self.__check_for_compatibility_of_container(self.__positioned_coffees[1].get_attachment(), texture)
        if self.__positioned_coffees[2]:
            self.__positioned_coffees[2].get_attachment().fill(texture)
            if self.__positioned_coffees[2].get_attachment().get_level() == self.__max_level:
                self.__check_for_compatibility_of_container(self.__positioned_coffees[2].get_attachment(), texture)

        if not self.__brewing_coffee:
            self.__remove_beverage_from_queue()

    def __check_for_compatibility_of_container(self, container, texture):
        if self.__brewing_queue[0].is_allow_double() and self.__positioned_coffees[1] and not self.__positioned_coffees[2]:
            # two coffees should have been placed, only one is there.
            return  # no action needed, as the logic for overflowing is already in the __start_making_coffee method
        # if the container is smaller than the brewing coffee...
        if container.get_container_type() < self.__brewing_queue[0].get_container_type():
            # ... the cup should overflow
            container.toggle_overflown(texture)
        # if it is bigger...
        elif container.get_container_type() > self.__brewing_queue[0].get_container_type():
            # ... the cup should not be full
            container.set_level(self.__max_level - 1, texture)

    def __fill_tea_original_thread(self, texture):
        if self.__positioned_coffees[0]:
            self.__positioned_coffees[0].get_attachment().fill(texture)

    def __update_time_remaining(self):
        if self.__brewing_coffee and self.__brewing_queue:
            self.__time_passed += Time.get_delta_time()
            self.__time_remaining.set_text_string(f"time remaining: {self.__brewing_queue[0].get_brew_length() - self.__time_passed:.2f}")
        else:
            self.__time_remaining.set_text_string("")

    def __create_products(self) -> None:
        CoffeeProduct(f"Espresso",
                      GuiTexture(self.__loader.load_texture("pngs/ui/espresso_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.ESPRESSO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Espresso"])
        CoffeeProduct(f"Doppio",
                      GuiTexture(self.__loader.load_texture("pngs/ui/doppio_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Espresso", "Espresso"])
        CoffeeProduct(f"Cafe Creme",
                      GuiTexture(self.__loader.load_texture("pngs/ui/coffee_creme_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                      content=["Cafe Creme"])
        CoffeeProduct(f"2 Cafe Creme",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_coffee_creme_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                      content=["Cafe Creme", "Cafe Creme"])
        CoffeeProduct(f"Milk Coffee",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_coffee_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                      content=["Milk Coffee"])
        CoffeeProduct(f"2 Milk Coffee",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_milk_coffee_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                      content=["Milk Coffee", "Milk Coffee"])
        CoffeeProduct(f"Cappuccino",
                      GuiTexture(self.__loader.load_texture("pngs/ui/cappuccino_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                      content=["Cappuccino"])
        CoffeeProduct(f"2 Cappuccini",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_cappuccino_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                      content=["Cappuccino", "Cappuccino"])
        CoffeeProduct(f"Latte Macchiato",
                      GuiTexture(self.__loader.load_texture("pngs/ui/latte_macchiato_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Latte Macchiato"])
        CoffeeProduct(f"Cafe Latte",
                      GuiTexture(self.__loader.load_texture("pngs/ui/latte_macchiato_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Cafe Latte"])
        CoffeeProduct(f"Tea",
                      GuiTexture(self.__loader.load_texture("pngs/ui/tea_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=18,
                      allows_double=False,
                      container_type=CoffeeProduct.TEA_POT,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/tea_filling_tex")),
                      content=["Tea"])
        CoffeeProduct(f"Hot Chocolate",
                      GuiTexture(self.__loader.load_texture("pngs/ui/chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Hot Chocolate"])
        CoffeeProduct(f"Cold Chocolate",
                      GuiTexture(self.__loader.load_texture("pngs/ui/chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Cold Chocolate"])
        CoffeeProduct(f"Children Chocolate",
                      GuiTexture(self.__loader.load_texture("pngs/ui/small_chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.SMALL_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Children Chocolate"])
        CoffeeProduct(f"Milk for Chai, Ovo",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Milk for Chai, Ovo"])
        CoffeeProduct(f"Warm Milk",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Warm Milk"])
        CoffeeProduct(f"Cold Milk",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Cold Milk"])
        CoffeeProduct(f"Babyccino",
                      GuiTexture(self.__loader.load_texture("pngs/ui/small_milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.SMALL_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_foam_filling_tex")),
                      content=["Babyccino"])
        CoffeeProduct(f"Americano",
                      GuiTexture(self.__loader.load_texture("pngs/ui/americano_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Americano"])
        CoffeeProduct(f"Doppio Macchiato",
                      GuiTexture(self.__loader.load_texture("pngs/ui/flatwhite_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Doppio Macchiato"])


class CoffeeMachineOSLactoseFree:

    BACKGROUND_TEXTURE_SIZE = [1920, 1080]
    __NAME = "COFFEE_MACHINE"

    def __init__(self, render_target, loader, obj_loader, fbo, gui_renderer, object_picker) -> None:
        """
        Creates new CoffeeMachineOS instance.

        :param render_target: The object the screen texture should be rendered on
        :param loader: The Loader object
        :param fbo: The FBO object
        :param gui_renderer: the GuiRendered object
        """
        self.__render_target = render_target
        self.__is_interacting = False
        self.__original_camera_pos = None
        self.__original_camera_angles = None

        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__fbo = fbo
        self.__gui_renderer = gui_renderer
        self.__object_picker = object_picker

        self.__icon_offset = 0.25
        self.__text_offset = 0.04
        self.__icon_size = 0.125
        self.__rows = 4
        self.__size_adjustment = 2
        self.__columns = self.__rows
        self.__background_texture = GuiTexture(loader.load_texture("pngs/ui/coffee_machine_background"), [0, 0], [1, 1])
        self.__selected_texture = GuiTexture(loader.load_texture("pngs/ui/selected"), [0, 0], [self.__icon_size * 1.1,
                                                                                            self.__icon_size * 1.1])
        self.__cancel_texture = GuiTexture(loader.load_texture("pngs/ui/delete"), [-2, -2], [0.05, 0.05])
        self.__start_texture = GuiTexture(loader.load_texture("pngs/ui/confirm"), [-2, -2], [0.05, 0.05])
        self.__selected_position = [0, 0]  # x y, top-left corner is 0, 0
        self.__current_page = 0
        self.__product_entries = None
        self.__create_products()
        self.__time_remaining = GUIText("", 18,
                                        FontType(self.__loader.load_texture("fnts/arial"), "res/fnts/arial.fnt"),
                                        [0.07, 0.75], 1, False)
        self.__time_remaining.set_color(1, 0, 0)
        self.__time_remaining.set_border_width(0.7)
        self.__time_remaining.set_border_edge(0.1)
        self.__time_passed = 0
        self.__coffee_buffer = False
        self.__coffee_texture = None
        self.__tea_buffer = False
        self.__tea_texture = None
        self.__max_level = 3
        self.__brewing_coffee = False
        self.__brewing_tea = False
        self.__texts = self.get_page_texts()

        self.__positioned_coffees = [None, None, None]  # tea, coffee1, coffee2
        y, x = 0.35, 2.1
        self.__offset_positions = (vec3(x, y, 0.75) * self.__render_target.get_scale(),
                                   vec3(x, y, 0) * self.__render_target.get_scale(),
                                   vec3(x, y, -0.25) * self.__render_target.get_scale(),
                                   vec3(x, y, 0.25) * self.__render_target.get_scale())

        self.__brewing_queue = []
        self.__max_queue_length = 7

        self.__listener = UniversalInputListener()

    def render_screen(self) -> None:
        self.__update_time_remaining()
        self.__check_bools()
        self.__move_cursor()
        self.__fbo.bind_frame_buffer()
        guis = [self.__background_texture]
        self.__update_positions_of_products()
        self.__product_entries = CoffeePageLactoseFree.get_instances()[self.__current_page].get_products()
        guis.extend([product.get_icon() for product in self.__product_entries])
        guis.extend([product.get_icon() for product in self.__brewing_queue])
        guis.extend([self.__selected_texture, self.__cancel_texture, self.__start_texture])
        self.__gui_renderer.render(guis)
        self.__texts = self.get_page_texts()
        TextMaster.render_specified(self.__texts)
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def interact(self, player, camera) -> None:
        if self.__listener.get_interact() or self.__listener.get_deny():
            collision = self.__object_picker.update([self.__render_target])
            if self.__is_interacting:
                self.__is_interacting = False
                player.set_player_under_control(True)
                self.__move_camera_to_original_pos(camera)
            elif collision == self.__render_target:
                self.__is_interacting = True
                player.set_player_under_control(False)
                self.__move_in_front_screen(camera)

    def get_is_interacting(self) -> bool:
        return self.__is_interacting

    def get_icon_size(self) -> float:
        return self.__icon_size

    def get_text_offset(self) -> float:
        return self.__text_offset

    def set_coffee(self, index: int, entity) -> None:
        if index <= 2:
            self.__positioned_coffees[index] = entity
            match index:
                case 0:
                    entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                case 1:
                    entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                case 2:
                    self.get_coffee(1).set_position(
                        vec3(self.__render_target.get_position()) + self.__offset_positions[index])
                    entity.set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[index + 1])

    def get_coffee(self, index: int):
        if index <= 2:
            return self.__positioned_coffees[index]

    def get_coffee_list(self) -> list:
        """Returns a copy of the list of coffees"""
        return self.__positioned_coffees.copy()

    def remove_coffee(self, index: int):
        if index <= 2:
            self.__positioned_coffees[index] = None
            if self.get_coffee(1) is None and self.get_coffee(2) is not None:
                self.set_coffee(1, self.get_coffee(2))
                self.remove_coffee(2)
            if self.get_coffee(2) is None and self.get_coffee(1) is not None:
                self.get_coffee(1).set_position(vec3(self.__render_target.get_position()) + self.__offset_positions[1])

    @classmethod
    def get_name(cls) -> str:
        return cls.__NAME

    def get_fbo(self):
        return self.__fbo

    def is_brewing_coffee(self) -> bool:
        return self.__brewing_coffee

    def is_brewing_tea(self) -> bool:
        return self.__brewing_tea

    def __move_cursor(self) -> None:
        """Updates the cursor of the coffee machine. Method is being called from the render_screen method."""
        if self.__is_interacting:
            if UniversalInput.get_up():
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] = self.__current_page * 4
                self.__selected_position[1] -= 1 if self.__selected_position[1] > 0 else 0
            if UniversalInput.get_down():
                self.__selected_position[1] += 1 if self.__selected_position[1] < 5 else 0
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] = 0
            if UniversalInput.get_left():
                self.__selected_position[0] -= 1 if self.__selected_position[0] > 0 else 0
            if UniversalInput.get_right():
                if self.__selected_position[1] == 4:
                    self.__selected_position[0] += 1 if self.__selected_position[0] < self.__max_queue_length - 1 else 0
                elif self.__selected_position[0] < 4 * len(CoffeePage.get_instances()) - 1:
                    self.__selected_position[0] += 1
            if UniversalInput.get_confirm():    # enter key
                if self.__selected_position[1] == 4:
                    self.__remove_beverage_from_queue(self.__selected_position[0])
                elif self.__selected_position[1] == 5:
                    self.__start_making_coffee()
                else:
                    index = self.__selected_position[1] * 4 + self.__selected_position[0] % 4
                    if index < len(self.__product_entries):
                        self.__add_beverage_to_queue(self.__product_entries[index])

        if not self.__selected_position[1] >= 4:
            # page should not change if we are currently deleting products from the queue
            self.__current_page = self.__selected_position[0] // 4

        self.__move_cancel_button()
        self.__move_start_button()

    def get_page_texts(self) -> list:
        self.__product_entries = CoffeePageLactoseFree.get_instances()[self.__current_page].get_products()
        texts = [product.get_text() for product in self.__product_entries]
        texts.append(self.__time_remaining)
        return texts

    def get_all_texts(self) -> list:
        texts = CoffeeProductLactoseFree.all_texts.copy()
        texts.append(self.__time_remaining)
        return texts

    def __update_positions_of_products(self) -> None:
        self.__product_entries = CoffeePageLactoseFree.get_instances()[self.__current_page].get_products()
        for i, product in enumerate(self.__product_entries):
            product.get_icon().set_position([(self.__icon_offset + 1 / (self.__rows + self.__size_adjustment) * 2 * (i % 4)) - 1,
                                             1 - (self.__icon_offset + 1 / (self.__columns + self.__size_adjustment) * 2 * (i // 4))])
            product.get_text().set_position([(product.get_icon().get_position()[0] + 1) / 2 - self.__icon_size / 2,
                                             (1 - product.get_icon().get_position()[1]) / 2 + self.__text_offset])

    def __add_beverage_to_queue(self, beverage: CoffeeProduct) -> None:
        if len(self.__brewing_queue) >= self.__max_queue_length:
            return
        self.__brewing_queue.append(CoffeeProductLactoseFree(beverage.get_name(),
                                                             GuiTexture(beverage.get_icon().get_texture(),
                                                                        [(len(self.__brewing_queue) * self.__icon_size * 2 + self.__icon_offset) - 1, -0.75],
                                                                        [self.__icon_size * 0.9, self.__icon_size * 0.9]),
                                                             beverage.get_brew_length(), beverage.get_container_type(),
                                                             beverage.is_allow_double(), self.__loader, beverage.get_texture(),
                                                             beverage.get_content(), add_to_coffee_page=False))
        self.__start_making_coffee()

    def __move_cancel_button(self) -> None:
        # if the fourth row is selected and any product are in queue, the brewing queue cancel button should appear
        if self.__selected_position[1] == 4 and self.__brewing_queue:
            self.__selected_texture.set_position([-2, -2])  # out of bounds
            self.__cancel_texture.set_position([self.__icon_offset * (self.__selected_position[0] + 1) - 0.95, -0.70])
        else:
            # else move the cancel button out of bounds
            self.__cancel_texture.set_position([-2, -2])
            # selected texture loops back from x-position 4 to 1, but internally the position is being counted further
            self.__selected_texture.set_position([(self.__icon_offset + 1 / (
                        self.__rows + self.__size_adjustment) * 2 * (self.__selected_position[0] % 4)) - 1,
                                                  1 - (self.__icon_offset + 1 / (
                                                              self.__columns + self.__size_adjustment) * 2 *
                                                       self.__selected_position[1])])

    def __move_start_button(self) -> None:
        # if the fifth row is selected and any product are in queue, the brewing queue start button should appear
        if self.__selected_position[1] == 5 and self.__brewing_queue:
            self.__selected_texture.set_position([-2, -2])  # out of bounds
            self.__start_texture.set_position([self.__icon_offset - 0.95, -0.8])
        else:
            # else move the start button out of bounds
            self.__start_texture.set_position([-2, -2])

    def __check_bools(self):
        if not self.__brewing_queue:
            self.__brewing_coffee = False
            return
        if self.__coffee_buffer:
            if not self.__coffee_texture:
                self.__coffee_texture = self.__brewing_queue[0].get_texture()
            self.__fill_original_thread(self.__coffee_texture)
            self.__coffee_buffer = False
        if self.__tea_buffer:
            if not self.__tea_texture:
                self.__tea_texture = self.__brewing_queue[0].get_texture()
                # now that the texture is saved, we can remove the tea from the brewing queue
                self.__update_time_remaining()
            self.__fill_tea_original_thread(self.__tea_texture)
            self.__tea_buffer = False

    def __move_in_front_screen(self, camera) -> None:
        self.__original_camera_pos = camera.get_position()
        self.__original_camera_angles = [camera.get_yaw(), camera.get_pitch(), camera.get_roll()]
        x = 3.5 * math.sin(math.radians(self.__render_target.get_rot_y()))
        z = 3.5 * math.cos(math.radians(self.__render_target.get_rot_y()))
        offset = vec3(x, 2.5, z) * self.__render_target.get_scale()

        position = vec3(self.__render_target.get_position()) + offset

        camera.set_position(position)
        camera.set_yaw(-self.__render_target.get_rot_y())
        camera.set_pitch(0)
        camera.set_roll(0)

    def __move_camera_to_original_pos(self, camera) -> None:
        camera.set_yaw(self.__original_camera_angles[0])
        camera.set_pitch(self.__original_camera_angles[1])
        camera.set_roll(self.__original_camera_angles[2])
        camera.set_position(self.__original_camera_pos)

    def __remove_beverage_from_queue(self, index: int = 0) -> None:
        if len(self.__brewing_queue) >= index + 1:
            self.__brewing_queue.pop(index)
            self.__update_queue()

    def __update_queue(self) -> None:
        for i in range(len(self.__brewing_queue)):
            self.__brewing_queue[i].get_icon().set_position(
                [(i * self.__icon_size * 2 + self.__icon_offset) - 1, -0.75])

    def __start_making_coffee(self):
        if not self.__brewing_queue:
            return

        if self.__brewing_queue[0].get_container_type() == CoffeeProduct.TEA_POT:
            if not self.__brewing_tea:
                if self.__positioned_coffees[0]:
                    process = Thread(target=self.__fill_timing, args=(self.__max_level, True,))
                    process.start()
                    self.__brewing_tea = True
                    self.__positioned_coffees[0].get_attachment().append_content(self.__brewing_queue[0].get_content())
            return  # if tea is being made, no coffee should be let out

        if self.__brewing_coffee:
            return
        if not self.__positioned_coffees[1]:
            return

        if self.__brewing_queue[0].is_allow_double():
            # is allowed to make to 2 coffees and 2 coffees are placed:
            if self.__positioned_coffees[1] and self.__positioned_coffees[2]:
                process = Thread(target=self.__fill_timing, args=(self.__max_level,))
                process.start()
                # content is split in half
                if len(self.__brewing_queue[0].get_content()) == 2:
                    self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content()[0])
                    self.__positioned_coffees[2].get_attachment().append_content(self.__brewing_queue[0].get_content()[1])
                if len(self.__brewing_queue[0].get_content()) == 4:
                    self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content()[0:2])
                    self.__positioned_coffees[2].get_attachment().append_content(self.__brewing_queue[0].get_content()[2:4])
            # is allowed to make to 2 coffees and 1 coffee is placed:
            else:
                process = Thread(target=self.__fill_timing, args=(self.__max_level + 1,))
                process.start()
                # whole content is poured into
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content())
        else:
            # is NOT allowed to make to 2 coffees and 2 coffees are placed:
            if self.__positioned_coffees[1] and self.__positioned_coffees[2]:
                # both coffees are not full
                process = Thread(target=self.__fill_timing, args=(1,))
                process.start()
                # both get a half
                self.__positioned_coffees[1].get_attachment().append_content(
                    self.__brewing_queue[0].get_content()[0] + " half")
                self.__positioned_coffees[2].get_attachment().append_content(
                    self.__brewing_queue[0].get_content()[0] + " half")
            # 1 coffee is allowed and 1 is placed
            else:
                process = Thread(target=self.__fill_timing, args=(self.__max_level,))
                process.start()
                self.__positioned_coffees[1].get_attachment().append_content(self.__brewing_queue[0].get_content())
        self.__time_remaining.set_text_string(f"time remaining: {self.__brewing_queue[0].get_brew_length()}")
        self.__brewing_coffee = True

    def __fill_timing(self, levels: int, is_tea: bool = False):
        """
        Method running in a parallel thread for the timing. Sets the __tea_buffer or __coffee_buffer to True, which
        is being checked in the render_screen method. This workaround was made because of issues with multithreading
        OpenGL calls.
        """
        self.__time_passed = 0
        waiting_time = self.__brewing_queue[0].get_brew_length() / levels
        if is_tea:
            self.__remove_beverage_from_queue()

        for i in range(levels):
            sleep(waiting_time)
            if is_tea:
                self.__tea_buffer = True
            else:
                self.__coffee_buffer = True
        if is_tea:
            self.__brewing_tea = False
        else:
            self.__brewing_coffee = False

    def __fill_original_thread(self, texture):
        if self.__positioned_coffees[1]:
            self.__positioned_coffees[1].get_attachment().fill(texture)
            if self.__positioned_coffees[1].get_attachment().get_level() == self.__max_level:
                self.__check_for_compatibility_of_container(self.__positioned_coffees[1].get_attachment(), texture)
        if self.__positioned_coffees[2]:
            self.__positioned_coffees[2].get_attachment().fill(texture)
            if self.__positioned_coffees[2].get_attachment().get_level() == self.__max_level:
                self.__check_for_compatibility_of_container(self.__positioned_coffees[2].get_attachment(), texture)

        if not self.__brewing_coffee:
            self.__remove_beverage_from_queue()

    def __check_for_compatibility_of_container(self, container, texture):
        if self.__brewing_queue[0].is_allow_double() and self.__positioned_coffees[1] and not self.__positioned_coffees[2]:
            # two coffees should have been placed, only one is there.
            return  # no action needed, as the logic for overflowing is already in the __start_making_coffee method
        # if the container is smaller than the brewing coffee...
        if container.get_container_type() < self.__brewing_queue[0].get_container_type():
            # ... the cup should overflow
            container.toggle_overflown()
        # if it is bigger...
        elif container.get_container_type() > self.__brewing_queue[0].get_container_type():
            # ... the cup should not be full
            container.set_level(self.__max_level - 1, texture)

    def __fill_tea_original_thread(self, texture):
        if self.__positioned_coffees[0]:
            self.__positioned_coffees[0].get_attachment().fill(texture)

    def __update_time_remaining(self):
        if self.__brewing_coffee and self.__brewing_queue:
            self.__time_passed += Time.get_delta_time()
            self.__time_remaining.set_text_string(
                f"time remaining: {self.__brewing_queue[0].get_brew_length() - self.__time_passed:.2f}")
        else:
            self.__time_remaining.set_text_string("")

    def __create_products(self) -> None:
        CoffeeProductLactoseFree(f"Espresso",
                      GuiTexture(self.__loader.load_texture("pngs/ui/espresso_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.ESPRESSO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Espresso"])
        CoffeeProductLactoseFree(f"Doppio",
                      GuiTexture(self.__loader.load_texture("pngs/ui/doppio_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Espresso", "Espresso"])
        CoffeeProductLactoseFree(f"Cafe Creme",
                      GuiTexture(self.__loader.load_texture("pngs/ui/coffee_creme_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                      content=["Cafe Creme"])
        CoffeeProductLactoseFree(f"2 Cafe Creme",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_coffee_creme_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_creme_filling_tex")),
                      content=["Cafe Creme", "Cafe Creme"])
        CoffeeProductLactoseFree(f"Milk Coffee Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_coffee_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                      content=["Milk Coffee", "Lactose Free"])
        CoffeeProductLactoseFree(f"2 Milk Coffee Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_milk_coffee_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_coffee_filling_tex")),
                      content=["Milk Coffee", "Lactose Free", "Milk Coffee", "Lactose Free"])
        CoffeeProductLactoseFree(f"Cappuccino Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/cappuccino_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                      content=["Cappuccino", "Lactose Free"])
        CoffeeProductLactoseFree(f"2 Cappuccini Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/2_cappuccino_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=10,
                      allows_double=True,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/cappuccino_filling_tex")),
                      content=["Cappuccino", "Lactose Free", "Cappuccino", "Lactose Free"])
        CoffeeProductLactoseFree(f"Latte Macchiato Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/latte_macchiato_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Latte Macchiato", "Lactose Free"])
        CoffeeProductLactoseFree(f"Cafe Latte Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/latte_macchiato_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Cafe Latte", "Lactose Free"])
        CoffeeProductLactoseFree(f"Tea",
                      GuiTexture(self.__loader.load_texture("pngs/ui/tea_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=18,
                      allows_double=False,
                      container_type=CoffeeProduct.TEA_POT,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/tea_filling_tex")),
                      content=["Tea"])
        CoffeeProductLactoseFree(f"Hot Chocolate Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Hot Chocolate", "Lactose Free"])
        CoffeeProductLactoseFree(f"Cold Chocolate Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Cold Chocolate", "Lactose Free"])
        CoffeeProductLactoseFree(f"Children Chocolate Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/small_chocolate_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.SMALL_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/chocolate_filling_tex")),
                      content=["Children Chocolate", "Lactose Free"])
        CoffeeProductLactoseFree(f"Milk for Chai, Ovo Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Milk for Chai, Ovo", "Lactose Free"])
        CoffeeProductLactoseFree(f"Warm Milk Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Warm Milk", "Lactose Free"])
        CoffeeProductLactoseFree(f"Cold Milk Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.BIG_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_filling_tex")),
                      content=["Cold Milk", "Lactose Free"])
        CoffeeProductLactoseFree(f"Babyccino Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/small_milk_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=6,
                      allows_double=False,
                      container_type=CoffeeProduct.SMALL_GLASS,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/milk_foam_filling_tex")),
                      content=["Babyccino", "Lactose Free"])
        CoffeeProductLactoseFree(f"Americano",
                      GuiTexture(self.__loader.load_texture("pngs/ui/americano_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.CAPPUCCINO_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/coffee_filling_tex")),
                      content=["Americano"])
        CoffeeProductLactoseFree(f"Doppio Macchiato Lactose Free",
                      GuiTexture(self.__loader.load_texture("pngs/ui/flatwhite_icon"),
                                 [0, 0],
                                 [self.__icon_size, self.__icon_size]),
                      brew_length=8,
                      allows_double=False,
                      container_type=CoffeeProduct.COFFEE_CUP,
                      loader=self.__loader,
                      texture=ModelTexture(self.__loader.load_texture("pngs/cups/latte_macchiato_filling_tex")),
                      content=["Doppio Macchiato", "Lactose Free"])
