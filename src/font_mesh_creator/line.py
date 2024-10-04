from src.font_mesh_creator.word import Word


class Line:
    """
    Represents a line of text consisting of multiple words
    """

    def __init__(self, space_width: float, font_size: float, max_length: float):
        """
        Initializes a Line instance.

        :param space_width: The width of the space between words as a fraction of the font size.
        :param font_size: The size of the font in pixels.
        :param max_length: The maximum length of the line.
        """
        self.__words = []
        self.__current_line_length = 0
        self.__space_size = space_width * font_size
        self.__max_length = max_length

    def attempt_to_add_word(self, word: Word) -> bool:
        """
        Attempts to add a word to the line.

        If the line can fit the word in without exceeding the maximum length,
        the word is added, and the line length is increased.

        :param word: The word to be added to the line.
        :return: True if the word was added successfully; False otherwise.
        """
        additional_length = word.get_word_width()
        additional_length += self.__space_size if self.__words else 0
        if self.__current_line_length + additional_length <= self.__max_length:
            self.__words.append(word)
            self.__current_line_length += additional_length
            return True
        else:
            return False

    def get_max_length(self) -> float:
        """
        Returns the maximum length of the line.

        :return: The maximum length of the line.
        """
        return self.__max_length

    def get_line_length(self) -> float:
        """
        Returns the current length of the line.

        :return: The current length of the line.
        """
        return self.__current_line_length

    def get_words(self) -> list:
        """
        Returns the list of words in the line.

        :return: A list of words contained in the line.
        """
        return self.__words
