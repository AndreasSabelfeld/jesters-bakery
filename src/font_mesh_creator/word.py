from src.font_mesh_creator.character import Character


class Word:
    """During the loading of a text this represents one word in the text."""

    def __init__(self, font_size: float):
        """Initializes a new empty word.

        :param font_size: The font size used for this word.
        """
        self.__characters = []
        self.__width = 0
        self.__font_size = font_size

    def add_character(self, character: Character) -> None:
        """Adds a character to the word and updates the width.

        :param character: The Character instance to be added to the word.
        """
        self.get_characters().append(character)
        self.__width += character.get_x_advance() * self.get_font_size()

    def get_characters(self) -> list:
        """returns the characters that make up the word.

        :return: A list of Character instances in this word.
        """
        return self.__characters

    def get_word_width(self) -> float:
        """Calculates the total width of the word.

        :return: The width of the word based on its characters.
        """
        return self.__width

    def get_font_size(self) -> float:
        """returns the font size of the word.

        :return: The font size used for this word.
        """
        return self.__font_size
