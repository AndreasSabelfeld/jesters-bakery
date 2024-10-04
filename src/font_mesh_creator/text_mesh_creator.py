from src.font_mesh_creator.meta_file import MetaFile
from src.font_mesh_creator.text_mesh_data import TextMeshData
from src.font_mesh_creator.gui_text import GUIText
from src.font_mesh_creator.line import Line
from src.font_mesh_creator.word import Word
from src.font_mesh_creator.character import Character


class TextMeshCreator:
    """
    Creates a mesh for rendering text based on font metadata and provided text input.
    """

    __LINE_HEIGHT = 0.003
    __SPACE_ASCII = 32
    __NEW_LINE = ord('\n')

    def __init__(self, meta_file: str):
        """
        Initializes the TextMeshCreator with the specified metadata file.

        :param meta_file: The path to the font metadata file.
        """
        self.__meta_data = MetaFile(meta_file)

    def create_text_mesh(self, text: GUIText) -> TextMeshData:
        """
        Creates a text mesh from the provided GUIText object.

        :param text: The GUIText object containing the text to be rendered.
        :return: A TextMeshData object containing vertices and texture coordinates for the text mesh.
        """
        lines = self.create_structure(text)
        data = self.create_quad_vertices(text, lines)
        return data

    def create_structure(self, text: GUIText) -> list[Line]:
        """
        Structures the text into lines and words based on the GUIText input.

        :param text: The GUIText object containing the text to be structured.
        :return: A list of Line objects of the structured text.
        """
        chars = [*text.get_text_string()]
        lines = []
        current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
        current_word = Word(text.get_font_size())
        for c in chars:
            ascii = ord(c)
            if ascii == self.__NEW_LINE:
                lines.append(current_line)
                current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
            if ascii == self.__SPACE_ASCII:
                added = current_line.attempt_to_add_word(current_word)
                if not added:
                    lines.append(current_line)
                    current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
                    current_line.attempt_to_add_word(current_word)
                current_word = Word(text.get_font_size())
                continue
            character = self.__meta_data.get_character(ascii)
            if not character:
                continue
            current_word.add_character(character)
        self.complete_structure(lines, current_line, current_word, text)
        return lines

    def complete_structure(self, lines: list[Line], current_line: Line, current_word: Word, text: GUIText) -> None:
        """
        Completes the structure of the text by adding the final word and line to the list.

        :param lines: The list of Line objects of the text structure.
        :param current_line: The current line being processed.
        :param current_word: The current word being processed.
        :param text: The GUIText object containing the text.
        """
        added = current_line.attempt_to_add_word(current_word)
        if not added:
            lines.append(current_line)
            current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
            current_line.attempt_to_add_word(current_word)
        lines.append(current_line)

    def create_quad_vertices(self, text: GUIText, lines: list[Line]) -> TextMeshData:
        """
        Creates vertex and texture coordinate data for the text mesh based on structured lines.

        :param text: The GUIText object containing the text to be rendered.
        :param lines: A list of Line objects of the structured text.
        :return: A TextMeshData object containing vertices and texture coordinates for the text mesh.
        """
        text.set_number_of_lines(len(lines))
        cursor_x = 0
        cursor_y = 0
        vertices = []
        texture_coords = []
        for line in lines:
            if text.is_centered():
                cursor_x = (line.get_max_length() - line.get_line_length()) / 2
            for word in line.get_words():
                for letter in word.get_characters():
                    self.add_vertices_for_character(cursor_x, cursor_y, letter, text.get_font_size(), vertices)
                    self.add_tex_coords(texture_coords, letter.get_x_texture_coord(), letter.get_y_texture_coord(),
                                        letter.get_x_max_texture_coord(), letter.get_y_max_texture_coord())
                    cursor_x += letter.get_x_advance() * text.get_font_size()
                cursor_x += self.__meta_data.get_space_width() * text.get_font_size()
            cursor_x = 0
            cursor_y += self.__LINE_HEIGHT * text.get_font_size()
        return TextMeshData(vertices, texture_coords)

    def add_vertices_for_character(self, cursor_x: float, cursor_y: float, character: Character, font_size: float,
                                   vertices: list[float]):
        """
        Adds vertex data for a specific character to the vertex list.

        :param cursor_x: The current x position of the cursor.
        :param cursor_y: The current y position of the cursor.
        :param character: The Character object to add.
        :param font_size: The size of the font being used.
        :param vertices: The list to which vertex data will be added.
        """
        x = cursor_x + (character.get_x_offset() * font_size)
        y = cursor_y + (character.get_y_offset() * font_size)
        max_x = x + (character.get_size_x() * font_size)
        max_y = y + (character.get_size_y() * font_size)
        proper_x = (2 * x) - 1
        proper_y = (-2 * y) + 1
        proper_max_x = (2 * max_x) - 1
        proper_max_y = (-2 * max_y) + 1
        self.add_vertices(vertices, proper_x, proper_y, proper_max_x, proper_max_y)

    @staticmethod
    def add_vertices(vertices: list[float], x: float, y: float, max_x: float, max_y: float) -> None:
        """
        Adds vertex data to the provided vertex list.

        :param vertices: The list to which vertex data will be added.
        :param x: The x-coordinate of the vertex.
        :param y: The y-coordinate of the vertex.
        :param max_x: The maximum x-coordinate of the vertex.
        :param max_y: The maximum y-coordinate of the vertex.
        """
        vertices.append(x)
        vertices.append(y)
        vertices.append(x)
        vertices.append(max_y)
        vertices.append(max_x)
        vertices.append(max_y)
        vertices.append(max_x)
        vertices.append(max_y)
        vertices.append(max_x)
        vertices.append(y)
        vertices.append(x)
        vertices.append(y)

    @staticmethod
    def add_tex_coords(tex_coords: list[float], x: float, y: float, max_x: float, max_y: float) -> None:
        """
        Adds texture coordinate data to the provided texture coordinate list.

        :param tex_coords: The list to which texture coordinate data will be added.
        :param x: The x-coordinate of the texture.
        :param y: The y-coordinate of the texture.
        :param max_x: The maximum x-coordinate of the texture.
        :param max_y: The maximum y-coordinate of the texture.
        """
        tex_coords.append(x)
        tex_coords.append(y)
        tex_coords.append(x)
        tex_coords.append(max_y)
        tex_coords.append(max_x)
        tex_coords.append(max_y)
        tex_coords.append(max_x)
        tex_coords.append(max_y)
        tex_coords.append(max_x)
        tex_coords.append(y)
        tex_coords.append(x)
        tex_coords.append(y)

    @classmethod
    def get_line_height(cls) -> float:
        """
        Returns the height of a line as defined by the class.

        :return: The line height constant.
        """
        return cls.__LINE_HEIGHT

    @classmethod
    def get_space_ascii(cls) -> int:
        """
        Returns the ASCII value of the space character.

        :return: The ASCII value of the space character.
        """
        return cls.__SPACE_ASCII
