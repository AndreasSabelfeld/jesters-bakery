
class ModelTexture:

    def __init__(self, texture_id: int):
        self.__texture_id = texture_id
        self.__normal_map = None
        self.__specular_map = None
        self.__shine_damper = 1
        self.__reflectivity = 0
        self.__has_transparency = False
        self.__use_fake_lighting = False
        self.__has_specular_map = False
        self.__number_of_rows = 1  # default, there is only 1 texture in the texture atlas

    def is_has_specular_map(self) -> bool:
        return self.__has_specular_map

    def set_specular_map(self, specular_map) -> None:
        self.__specular_map = specular_map
        self.__has_specular_map = True

    def get_specular_map(self) -> int:
        return self.__specular_map

    def set_normal_map(self, normal_map) -> None:
        self.__normal_map = normal_map

    def get_normal_map(self) -> int:
        return self.__normal_map

    def set_number_of_rows(self, num: int):
        self.__number_of_rows = num

    def get_number_of_rows(self) -> int:
        return self.__number_of_rows

    def get_id(self) -> int:
        return self.__texture_id

    def set_shine_damper(self, value: float) -> None:
        self.__shine_damper = value

    def get_shine_damper(self) -> float:
        return self.__shine_damper

    def set_reflectivity(self, value: float) -> None:
        self.__reflectivity = value

    def get_reflectivity(self) -> float:
        return self.__reflectivity

    def set_has_transparency(self, value: bool) -> None:
        self.__has_transparency = value

    def is_has_transparency(self) -> bool:
        return self.__has_transparency

    def set_use_fake_lighting(self, value: bool) -> None:
        self.__use_fake_lighting = value

    def is_use_fake_lighting(self) -> bool:
        return self.__use_fake_lighting

