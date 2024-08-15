import math
from threading import Thread
from time import sleep

from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.render_engine.input_controller import Binds
from src.textures.model_texture import ModelTexture


class TapFaucet:
    def __init__(self, obj_loader, loader, pos: list[float], rotation: list[float], size: int, fill_texture, content: str,
                 sign_texture: str):
        self.__obj_loader = obj_loader
        self.__loader = loader
        self.__pos = pos
        self.__rot = rotation
        self.__size = size
        self.__content = content

        self.__faucet = None
        self.__fill_texture = fill_texture
        self.__filling = False
        x_offset = 0.75 * math.sin(math.radians(self.__rot[1]))
        z_offset = -0.75 * math.cos(math.radians(self.__rot[1]))
        self.__offset = [x_offset, 2, z_offset]
        self.__brewing_length = 6
        self.__placed_glass = None
        self.__timing_buffer = False

        self.__load_assets(sign_texture)

    def update(self):
        if self.__timing_buffer:
            self.__fill(self.__placed_glass)
            self.__timing_buffer = False

    def start_fill(self, glass: GameObject) -> None:
        self.__filling = True
        glass.set_pickup_able(False)
        glass.set_position([self.__pos[0] + self.__offset[0],
                            self.__pos[1] + self.__offset[1],
                            self.__pos[2] + self.__offset[2]])

        glass.get_attachment().append_content(self.get_content())
        self.__placed_glass = glass
        process = Thread(target=self.__fill_timing, args=(glass,))
        process.start()

    def __fill_timing(self, glass: GameObject):
        levels = 3
        interval = self.__brewing_length / levels
        for i in range(levels):
            sleep(interval)
            self.__timing_buffer = True
        self.__filling = False
        glass.set_pickup_able(True)

    def __fill(self, glass: GameObject):
        glass.get_attachment().fill(self.__fill_texture)

    def __load_assets(self, sign_texture: str) -> None:
        tap_tap_model = self.__obj_loader.load_obj_model("objs/machinery/tap_tap", self.__loader)
        tap_tap_texture = ModelTexture(self.__loader.load_texture("pngs/machinery/white"))
        tap_tap_texture.set_reflectivity(5)
        static_tap_tap_model = TexturedModel(tap_tap_model, tap_tap_texture)
        static_tap_tap_collider = TexturedModel(self.__obj_loader.load_obj_model("objs/machinery/tap_tap_collider", self.__loader),
                                                ModelTexture(self.__loader.load_texture("")))

        tap_sign_model = self.__obj_loader.load_obj_model("objs/machinery/tap_sign", self.__loader)
        tap_sign_texture = ModelTexture(self.__loader.load_texture(sign_texture))
        tap_sign_texture.set_reflectivity(0)
        static_tap_sign_model = TexturedModel(tap_sign_model, tap_sign_texture)

        tap_tap = Entity(static_tap_tap_model, self.__pos, *self.__rot, self.__size)
        tap_sign = Entity(static_tap_sign_model, self.__pos, *self.__rot, self.__size)
        tap_tap_collider = Entity(static_tap_tap_collider, self.__pos, *self.__rot, self.__size)
        self.__faucet = GameObject(tap_tap, child_0=tap_sign, collider=tap_tap_collider, int_name="TAP")
        self.__faucet.set_attachment(self)
        self.__faucet.set_pickup_able(False)
        self.__faucet.set_ext_name("Tap Faucet")
        self.__faucet.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to place a glass.")
        self.__faucet.set_info(self.__content)

    def set_brewing_length(self, length: float) -> None:
        self.__brewing_length = length

    def get_faucet_game_object(self) -> GameObject:
        return self.__faucet

    def get_position(self) -> list[float]:
        return self.__pos

    def is_filling(self) -> bool:
        return self.__filling

    def get_content(self) -> str:
        return self.__content
