from math import sqrt
from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.game_mechanics.coffee_product import CoffeeProduct
from src.game_mechanics.coffe_page import CoffeePage
from src.guis.gui_texture import GuiTexture
from src.textures.model_texture import ModelTexture
from src.font_rendering.text_master import TextMaster
from src.pycgtypes import vec3, mat3


class CoffeeMachineOS:

    BACKGROUND_TEXTURE_SIZE = [1920, 1080]

    def __init__(self, render_target, loader, fbo, gui_renderer) -> None:
        """
        Creates new CoffeeMachineOS instance.

        :param render_target: The object the screen texture should be rendered on
        :param loader: The Loader object
        :param fbo: The FBO object
        :param gui_renderer: the GuiRendered object
        """
        self.__render_target = render_target
        self.__interaction_key = b'f'
        self.__interaction_radius = 10
        self.__is_interacting = False
        self.__original_camera_pos = None
        self.__original_camera_angles = None

        self.__loader = loader
        self.__fbo = fbo
        self.__gui_renderer = gui_renderer

        self.__icon_offset = 0.25
        self.__text_offset = 0.08
        self.__icon_size = 0.175
        self.__rows = 4
        self.__columns = self.__rows
        self.__background_texture = GuiTexture(loader.load_texture("coffee_machine_background"), [0, 0], [1, 1])
        self.__selected_texture = GuiTexture(loader.load_texture("selected_test"), [0, 0], [self.__icon_size * 1.1,
                                                                                            self.__icon_size * 1.1])
        self.__selected_position = [0, 0]  # x y, top-left corner is 0, 0
        self.__current_page = 0
        self.__product_entries = None
        self.__create_products()
        self.__texts = self.get_page_texts()

    def render_screen(self) -> None:
        self.__move_cursor()
        self.__fbo.bind_frame_buffer()
        guis = [self.__background_texture]
        self.__update_positions_of_products()
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        guis.extend([product.get_icon() for product in self.__product_entries])
        guis.append(self.__selected_texture)
        self.__gui_renderer.render(guis)
        self.__texts = self.get_page_texts()
        TextMaster.render_specified(self.__texts)
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def __move_cursor(self) -> None:
        """Updates the cursor of the coffee machine. Method is being called from the render_screen method."""
        if self.__is_interacting:
            if KeyboardInput.on_key_down(b'w'):
                self.__selected_position[1] -= 1 if self.__selected_position[1] > 0 else 0
            if KeyboardInput.on_key_down(b'a'):
                self.__selected_position[0] -= 1 if self.__selected_position[0] > 0 else 0
            if KeyboardInput.on_key_down(b's'):
                self.__selected_position[1] += 1 if self.__selected_position[1] < 3 else 0
            if KeyboardInput.on_key_down(b'd'):
                if self.__selected_position[0] < 4 * len(CoffeePage.get_instances()) - 1:
                    self.__selected_position[0] += 1
        self.__current_page = self.__selected_position[0] // 4
        # selected texture loops back from x-position 4 to 1, but internally the position is being counted further
        self.__selected_texture.set_position([(self.__icon_offset + 1/self.__rows*2 * (self.__selected_position[0] % 4)) - 1,
                                             1 - (self.__icon_offset + 1/self.__columns*2 * self.__selected_position[1])])

    def check_for_interaction(self, player, camera) -> None:
        distance = sqrt((self.__render_target.get_position()[0] - player.get_position()[0])**2 +
                        (self.__render_target.get_position()[1] - player.get_position()[1])**2 +
                        (self.__render_target.get_position()[2] - player.get_position()[2])**2)
        if distance < self.__interaction_radius:
            if KeyboardInput.on_key_down(self.__interaction_key):
                if not self.__is_interacting:
                    self.__is_interacting = True
                    player.set_player_under_control(False)
                    self.move_in_front_screen(camera)
                else:
                    self.__is_interacting = False
                    player.set_player_under_control(True)
                    self.move_camera_to_original_pos(camera)

    def move_in_front_screen(self, camera) -> None:
        self.__original_camera_pos = camera.get_position()
        self.__original_camera_angles = [camera.get_yaw(), camera.get_pitch(), camera.get_roll()]
        offset = vec3(0, 2.5, 3.5)
        rot_mat = mat3().rotation(self.__render_target.get_rot_x(), vec3(1, 1, 1))
        offset = rot_mat * offset

        position = vec3(self.__render_target.get_position()) + offset

        camera.set_position(position)
        camera.set_yaw(0)
        camera.set_pitch(0)
        camera.set_roll(0)

    def move_camera_to_original_pos(self, camera) -> None:
        camera.set_yaw(self.__original_camera_angles[0])
        camera.set_pitch(self.__original_camera_angles[1])
        camera.set_roll(self.__original_camera_angles[2])
        camera.set_position(self.__original_camera_pos)

    def get_is_interacting(self) -> bool:
        return self.__is_interacting

    def __create_products(self) -> None:
        for i in range(23):
            CoffeeProduct(f"product_{i}",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP,
                          loader=self.__loader)

    def __update_positions_of_products(self) -> None:
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        for i, product in enumerate(self.__product_entries):
            product.get_icon().set_position([(self.__icon_offset + 1 / self.__rows * 2 * (i % 4)) - 1,
                                             1 - (self.__icon_offset + 1 / self.__columns * 2 * (i // 4))])
            product.get_text().set_position([(product.get_icon().get_position()[0] + 1) / 2 - self.__icon_size / 2,
                                             (1 - product.get_icon().get_position()[1]) / 2 + self.__text_offset])

    def get_page_texts(self) -> list:
        self.__product_entries = CoffeePage.get_instances()[self.__current_page].get_products()
        return [product.get_text() for product in self.__product_entries]

    @staticmethod
    def get_all_texts() -> list:
        return CoffeeProduct.all_texts

    def get_icon_size(self) -> float:
        return self.__icon_size

    def get_text_offset(self) -> float:
        return self.__text_offset
