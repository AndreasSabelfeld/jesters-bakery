from src.font_mesh_creator.word import Word


class Line:
    def __init__(self, space_width: float, font_size: float, max_length: float):
        self.__words = []
        self.__current_line_length = 0
        self.__space_size = space_width * font_size
        self.__max_length = max_length

    def attempt_to_add_word(self, word: Word) -> bool:
        """
        Attempt to add a word to the line. If the line can fit the word in
        without reaching the maximum line length then the word is added and the
        line length increased.
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
        return self.__max_length

    def get_line_length(self) -> float:
        return self.__current_line_length

    def get_words(self) -> list:
        return self.__words
