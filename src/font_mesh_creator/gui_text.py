from src.font_rendering.text_master import TextMaster


class GUIText:

    def __init__(self, text: str, font_size: float, font, position: list[float], max_line_length: float, centered: bool):
        """
        Creates a GUIText instance and automatically loads it to the TextMaster class.

        :param text: text message of type string that should be rendered to the screen
        :param font_size: the size of the font in pixels
        :param font: instance of the FontType class
        :param position: 2D position on the screen [0;1]
        :param max_line_length: the maximum length a line can have, before starting a new line [0;1]
        :param centered: bool determining if the text should be centered in its rect
        """
        self.__text_string = text
        self.__font_size = font_size
        self.__font = font
        self.__position = position
        self.__line_max_size = max_line_length
        self.__center_text = centered

        self.__width = 0.5
        self.__edge = 0.1
        self.__border_width = 0.0
        self.__border_edge = 0.1
        self.__offset = [0.0, 0.0]
        self.__outline_color = [0, 0, 0]

        self.__text_mesh_vao = -1
        self.__vertex_count = -1
        self.__color = [0, 0, 0]
        self.__number_of_lines = -1

        TextMaster.load_text(self)

    def remove(self) -> None:
        """Removes the text from the TextMaster."""
        TextMaster.remove_text(self)

    def get_font(self):
        """Returns the font instance used for rendering the text.

        :return: the font instance"""
        return self.__font

    def set_color(self, r: float, g: float, b: float):
        """Sets the color of the text.

        :param r: Red component of the color.
        :param g: Green component of the color.
        :param b: Blue component of the color.
        """
        self.__color = [r, g, b]

    def get_color(self) -> list[float]:
        """Returns the current color of the text.

        :return: A list of the RGB color of the text.
        """
        return self.__color

    def set_width(self, width: float) -> None:
        """Sets the width of the text.

        :param width: The width of the text.
        """
        self.__width = width

    def get_width(self) -> float:
        """Returns the current width of the text.

        :return: The width of the text.
        """
        return self.__width

    def set_edge(self, edge: float) -> None:
        """Sets the edge size of the text.

        :param edge: The edge size.
        """
        self.__edge = edge

    def get_edge(self) -> float:
        """Returns the current edge size of the text.

        :return: The edge size.
        """
        return self.__edge

    def set_border_width(self, border_width: float) -> None:
        """Sets the border width of the text.

        :param border_width: The border width.
        """
        self.__border_width = border_width

    def get_border_width(self) -> float:
        """Returns the current border width of the text.

        :return: The border width.
        """
        return self.__border_width

    def set_border_edge(self, border_edge: float) -> None:
        """Sets the border edge size of the text.

        :param border_edge: The border edge size.
        """
        self.__border_edge = border_edge

    def get_border_edge(self) -> float:
        """Returns the current border edge size of the text.

        :return: The border edge size.
        """
        return self.__border_edge

    def set_offset(self, offset: list[float]) -> None:
        """Sets the offset of the text.

        :param offset: A list of the offset [x, y].
        """
        self.__offset = offset

    def get_offset(self) -> list[float]:
        """Returns the current offset of the text.

        :return: A list of the offset [x, y].
        """
        return self.__offset

    def set_outline_color(self, r: float, g: float, b: float) -> None:
        """Sets the outline color of the text.

        :param r: Red component of the outline color.
        :param g: Green component of the outline color.
        :param b: Blue component of the outline color.
        """
        self.__outline_color = [r, g, b]

    def get_outline_color(self) -> list[float]:
        """Returns the current outline color of the text.

        :return: A list of the RGB outline color.
        """
        return self.__outline_color

    def get_number_of_lines(self) -> int:
        """Returns the number of lines of text.

        :return: The number of lines.
        """
        return self.__number_of_lines

    def set_position(self, position: list[float]) -> None:
        """Sets the position of the text.

        :param position: A list of the 2D position [x, y].
        """
        self.__position = position

    def get_position(self) -> list[float]:
        """Returns the current position of the text.

        :return: A list of the 2D position [x, y].
        """
        return self.__position

    def get_mesh(self) -> int:
        """Returns the VAO for the text mesh.

        :return: The VAO of the text mesh.
        """
        return self.__text_mesh_vao

    def set_mesh_info(self, vao: int, vertices_count: int) -> None:
        """Sets the mesh information for the text.

        :param vao: The VAO of the text mesh.
        :param vertices_count: The number of vertices in the mesh.
        """
        self.__text_mesh_vao = vao
        self.__vertex_count = vertices_count

    def get_vertex_count(self) -> int:
        """Returns the vertex count of the text mesh.

        :return: The number of vertices in the text mesh.
        """
        return self.__vertex_count

    def get_font_size(self) -> float:
        """Returns the font size of the text.

        :return: The font size.
        """
        return self.__font_size

    def set_number_of_lines(self, number: int) -> None:
        """Sets the number of lines of text.

        :param number: The number of lines.
        """
        self.__number_of_lines = number

    def is_centered(self) -> bool:
        """Returns whether the text is centered.

        :return: True if the text is centered, False otherwise.
        """
        return self.__center_text

    def get_max_line_size(self) -> float:
        """Returns the maximum line size of the text.

        :return: The maximum line size.
        """
        return self.__line_max_size

    def get_text_string(self) -> str:
        """Returns the text string.

        :return: The text string.
        """
        return self.__text_string

    def set_text_string(self, text: str) -> None:
        """Sets the text string and reloads it to the TextMaster.

        :param text: The new text string.
        """
        self.__text_string = text
        TextMaster.remove_text(self)
        TextMaster.load_text(self)
