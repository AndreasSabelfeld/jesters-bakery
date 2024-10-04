
class ModelTexture:
    """
    Class representing the texture of a 3D model.
    """

    def __init__(self, texture_id: int):
        """
        Initializes a new ModelTexture with default parameters.

        :params texture_id: The ID of the texture.
        """
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
        """
        Checks if the model has a specular map.

        :return: True if the model has a specular map, False otherwise.
        """
        return self.__has_specular_map

    def set_specular_map(self, specular_map) -> None:
        """
        Sets the specular map for the texture.

        :params specular_map: The specular map.
        """
        self.__specular_map = specular_map
        self.__has_specular_map = True

    def get_specular_map(self) -> int:
        """
        Returns the specular map of the texture.

        :return: The specular map ID.
        """
        return self.__specular_map

    def set_normal_map(self, normal_map) -> None:
        """
        Sets the normal map for the texture.

        :params normal_map: The normal map.
        """
        self.__normal_map = normal_map

    def get_normal_map(self) -> int:
        """
        Returns the normal map of the texture.

        :return: The normal map ID.
        """
        return self.__normal_map

    def set_number_of_rows(self, num: int):
        """
        Sets the number of rows in the texture atlas.

        :params num: The number of rows.
        """
        self.__number_of_rows = num

    def get_number_of_rows(self) -> int:
        """
        Returns the number of rows in the texture atlas.

        :return: The number of rows.
        """
        return self.__number_of_rows

    def get_id(self) -> int:
        """
        Returns the texture ID.

        :return: The texture ID.
        """
        return self.__texture_id

    def set_shine_damper(self, value: float) -> None:
        """
        Sets the shine damper value for the texture.

        :params value: The shine damper value.
        """
        self.__shine_damper = value

    def get_shine_damper(self) -> float:
        """
        Returns the shine damper value of the texture.

        :return: The shine damper value.
        """
        return self.__shine_damper

    def set_reflectivity(self, value: float) -> None:
        """
        Sets the reflectivity value for the texture.

        :params value: The reflectivity value.
        """
        self.__reflectivity = value

    def get_reflectivity(self) -> float:
        """
        Returns the reflectivity value of the texture.

        :return: The reflectivity value.
        """
        return self.__reflectivity

    def set_has_transparency(self, value: bool) -> None:
        """
        Sets if the texture has transparency.

        :params value: True if the texture has transparency, False otherwise.
        """
        self.__has_transparency = value

    def is_has_transparency(self) -> bool:
        """
        Checks if the texture has transparency.

        :return: True if the texture has transparency, False otherwise.
        """
        return self.__has_transparency

    def set_use_fake_lighting(self, value: bool) -> None:
        """
        Sets if fake lighting should be used.

        :params value: True if fake lighting should be used, False otherwise.
        """
        self.__use_fake_lighting = value

    def is_use_fake_lighting(self) -> bool:
        """
        Checks if fake lighting is used.

        :return: True if fake lighting is used, False otherwise.
        """
        return self.__use_fake_lighting

