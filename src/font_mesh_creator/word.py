from src.font_mesh_creator.character import Character


class Word:
    """During the loading of a text this represents one word in the text."""
    def __init__(self, font_size: float):
        """Creates a new empty word"""
        self.__characters = []
        self.__width = 0
        self.__font_size = font_size

    def add_character(self, character: Character):
        self.get_characters().append(character)
        self.__width += character.get_x_advance() * self.get_font_size()

    def get_characters(self) -> list:
        return self.__characters

    def get_word_width(self) -> float:
        return self.__width

    def get_font_size(self) -> float:
        return self.__font_size
