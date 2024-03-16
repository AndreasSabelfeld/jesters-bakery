from src.font_mesh_creator.meta_file import MetaFile
from src.font_mesh_creator.text_mesh_data import TextMeshData
from src.font_mesh_creator.gui_text import GUIText
from src.font_mesh_creator.line import Line
from src.font_mesh_creator.word import Word
from src.font_mesh_creator.character import Character


class TextMeshCreator:

    __LINE_HEIGHT = 0.003
    __SPACE_ASCII = 32

    def __init__(self, meta_file: str):
        self.__meta_data = MetaFile(meta_file)

    def create_text_mesh(self, text: GUIText) -> TextMeshData:
        lines = self.create_structure(text)
        data = self.create_quad_vertices(text, lines)
        return data

    def create_structure(self, text: GUIText) -> list[Line]:
        chars = [*text.get_text_string()]
        lines = []
        current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
        current_word = Word(text.get_font_size())
        for c in chars:
            ascii = ord(c)
            if ascii == self.__SPACE_ASCII:
                added = current_line.attempt_to_add_word(current_word)
                if not added:
                    lines.append(current_line)
                    current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
                    current_line.attempt_to_add_word(current_word)
                current_word = Word(text.get_font_size())
                continue
            character = self.__meta_data.get_character(ascii)
            current_word.add_character(character)
        self.complete_structure(lines, current_line, current_word, text)
        return lines

    def complete_structure(self, lines: list[Line], current_line: Line, current_word: Word, text: GUIText) -> None:
        added = current_line.attempt_to_add_word(current_word)
        if not added:
            lines.append(current_line)
            current_line = Line(self.__meta_data.get_space_width(), text.get_font_size(), text.get_max_line_size())
            current_line.attempt_to_add_word(current_word)
        lines.append(current_line)

    def create_quad_vertices(self, text: GUIText, lines: list[Line]) -> TextMeshData:
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
        return cls.__LINE_HEIGHT

    @classmethod
    def get_space_ascii(cls) -> int:
        return cls.__SPACE_ASCII
