from math import sqrt
from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.game_mechanics.coffee_product import CoffeeProduct
from src.guis.gui_texture import GuiTexture
from src.textures.model_texture import ModelTexture
from src.font_rendering.text_master import TextMaster
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
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
        self.__background_texture = GuiTexture(loader.load_texture("coffee_machine_background"), [0, 0], [1, 1])
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
        self.__font = FontType(loader.load_texture("candara"), "res/candara.fnt")
        self.__product_entries = None
        self.__create_products()
        self.__create_texts()

    def render_screen(self) -> None:
        self.__fbo.bind_frame_buffer()
        guis = [self.__background_texture]
        guis.extend([product.get_icon() for product in self.__product_entries])
        self.__gui_renderer.render(guis)
        TextMaster.render()
        self.__fbo.unbind_frame_buffer()
        self.__render_target.get_model().set_texture(ModelTexture(self.__fbo.get_color_texture()))

    def check_for_interaction(self, player, camera) -> None:
        distance = sqrt((self.__render_target.get_position()[0] - player.get_position()[0])**2 +
                        (self.__render_target.get_position()[1] - player.get_position()[1])**2 +
                        (self.__render_target.get_position()[2] - player.get_position()[2])**2)
        if distance < self.__interaction_radius:
            if KeyboardInput.get_keys_held().get(self.__interaction_key):
                if not self.__is_interacting:
                    self.__is_interacting = True
                    self.move_in_front_screen(camera)
                else:
                    self.__is_interacting = False
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
        self.__product_entries = [
            CoffeeProduct("product_1",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_2",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_3",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_4",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_5",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_6",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_7",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP),
            CoffeeProduct("product_8",
                          GuiTexture(self.__loader.load_texture("product_icon_test"),
                                     [0, 0],
                                     [self.__icon_size, self.__icon_size]),
                          7,
                          container_type=CoffeeProduct.COFFEE_CUP)
        ]
        for i, product in enumerate(self.__product_entries):
            product.get_icon().set_position([(self.__icon_offset + 1/self.__rows*2 * (i % 4)) - 1,
                                             1 - (self.__icon_offset + 1/self.__columns*2 * (i // 4))])

    def __create_texts(self) -> None:
        for product in self.__product_entries:
            tmp_text = GUIText(product.get_name(),
                               25,
                               self.__font,
                               [(product.get_icon().get_position()[0] + 1) / 2 - self.__icon_size / 2,
                                (1 - product.get_icon().get_position()[1]) / 2 + self.__text_offset],
                               self.__icon_size,
                               True)
            tmp_text.set_color(1, 0, 0)
            tmp_text.set_border_width(0.7)
            tmp_text.set_border_edge(0.1)
