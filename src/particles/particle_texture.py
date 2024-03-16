
class ParticleTexture:

    def __init__(self, texture_id: int, number_of_rows: int, additive: bool):
        self.__texture_id = texture_id
        self.__number_of_rows = number_of_rows
        self.__additive = additive

    def is_additive(self) -> bool:
        return self.__additive

    def get_texture_id(self):
        return self.__texture_id

    def get_number_of_rows(self):
        return self.__number_of_rows
