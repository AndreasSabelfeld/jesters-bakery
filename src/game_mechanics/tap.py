import math

from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.textures.model_texture import ModelTexture
from src.game_mechanics.tap_faucet import TapFaucet


class Tap:
    def __init__(self, obj_loader, loader, pos: list[float], rotation: list[float], size: int, textures: list):
        self.__obj_loader = obj_loader
        self.__loader = loader
        self.__pos = pos
        self.__rot = rotation
        self.__size = size
        self.__textures = textures

        self.__base = None

        self.__faucet_0 = None
        self.__faucet_1 = None
        self.__faucet_2 = None
        self.__faucet_3 = None
        self.__faucet_4 = None

        self.__load_assets()

    def update(self):
        self.__faucet_0.update()
        self.__faucet_1.update()
        self.__faucet_2.update()
        self.__faucet_3.update()
        self.__faucet_4.update()

    def __load_assets(self) -> None:
        tap_base_model = self.__obj_loader.load_obj_model("objs/machinery/tap_base", self.__loader)
        tap_base_texture = ModelTexture(self.__loader.load_texture("pngs/machinery/tap_base_texture"))
        tap_base_texture.set_reflectivity(0.5)
        static_tap_base_model = TexturedModel(tap_base_model, tap_base_texture)

        tap_base = Entity(static_tap_base_model, self.__pos, *self.__rot, self.__size)
        self.__base = GameObject(tap_base)
        self.__base.set_pickup_able(False)

        x_offset = 1 * math.cos(math.radians(self.__rot[1]))
        z_offset = -1 * math.sin(math.radians(self.__rot[1]))
        pos_0 = [self.__pos[0] - 2 * x_offset, self.__pos[1], self.__pos[2] - 2 * z_offset]
        pos_1 = [self.__pos[0] - 1 * x_offset, self.__pos[1], self.__pos[2] - 1 * z_offset]
        pos_2 = [self.__pos[0] - 0 * x_offset, self.__pos[1], self.__pos[2] - 0 * z_offset]
        pos_3 = [self.__pos[0] + 1 * x_offset, self.__pos[1], self.__pos[2] + 1 * z_offset]
        pos_4 = [self.__pos[0] + 2 * x_offset, self.__pos[1], self.__pos[2] + 2 * z_offset]
        self.__faucet_0 = TapFaucet(self.__obj_loader, self.__loader, pos_0, self.__rot, self.__size, self.__textures[0], "Coke",
                                    "pngs/machinery/tap_faucet_coke_tex")
        self.__faucet_1 = TapFaucet(self.__obj_loader, self.__loader, pos_1, self.__rot, self.__size, self.__textures[1], "Schorle",
                                    "pngs/machinery/tap_faucet_schorle_tex")
        self.__faucet_2 = TapFaucet(self.__obj_loader, self.__loader, pos_2, self.__rot, self.__size, self.__textures[2], "Still Water",
                                    "pngs/machinery/tap_faucet_still_water_tex")
        self.__faucet_3 = TapFaucet(self.__obj_loader, self.__loader, pos_3, self.__rot, self.__size, self.__textures[3], "Sparkling Water",
                                    "pngs/machinery/tap_faucet_sparkling_water_tex")
        self.__faucet_4 = TapFaucet(self.__obj_loader, self.__loader, pos_4, self.__rot, self.__size, self.__textures[4], "Beer",
                                    "pngs/machinery/tap_faucet_beer_tex")

    def get_base(self) -> GameObject:
        return self.__base

    def get_faucet(self, num: int) -> GameObject:
        match num:
            case 0:
                return self.__faucet_0
            case 1:
                return self.__faucet_1
            case 2:
                return self.__faucet_2
            case 3:
                return self.__faucet_3
            case 4:
                return self.__faucet_4
            case _:
                print("Faucet number out of range!")

    def get_game_objects(self) -> list[GameObject]:
        return [self.__base,
                self.__faucet_0.get_faucet_game_object(),
                self.__faucet_1.get_faucet_game_object(),
                self.__faucet_2.get_faucet_game_object(),
                self.__faucet_3.get_faucet_game_object(),
                self.__faucet_4.get_faucet_game_object()]
