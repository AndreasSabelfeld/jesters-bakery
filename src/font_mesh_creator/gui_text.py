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
        TextMaster.remove_text(self)

    def get_font(self):
        return self.__font

    def set_color(self, r: float, g: float, b: float):
        self.__color = [r, g, b]

    def get_color(self) -> list[float]:
        return self.__color

    def set_width(self, width: float) -> None:
        self.__width = width

    def get_width(self) -> float:
        return self.__width

    def set_edge(self, edge: float) -> None:
        self.__edge = edge

    def get_edge(self) -> float:
        return self.__edge

    def set_border_width(self, border_width: float) -> None:
        self.__border_width = border_width

    def get_border_width(self) -> float:
        return self.__border_width

    def set_border_edge(self, border_edge: float) -> None:
        self.__border_edge = border_edge

    def get_border_edge(self) -> float:
        return self.__border_edge

    def set_offset(self, offset: list[float]) -> None:
        self.__offset = offset

    def get_offset(self) -> list[float]:
        return self.__offset

    def set_outline_color(self, r: float, g: float, b: float) -> None:
        self.__outline_color = [r, g, b]

    def get_outline_color(self) -> list[float]:
        return self.__outline_color

    def get_number_of_lines(self) -> int:
        return self.__number_of_lines

    def set_position(self, position: list[float]):
        self.__position = position

    def get_position(self) -> list[float]:
        return self.__position

    def get_mesh(self) -> int:
        return self.__text_mesh_vao

    def set_mesh_info(self, vao: int, vertices_count: int) -> None:
        self.__text_mesh_vao = vao
        self.__vertex_count = vertices_count

    def get_vertex_count(self) -> int:
        return self.__vertex_count

    def get_font_size(self) -> float:
        return self.__font_size

    def set_number_of_lines(self, number: int) -> None:
        self.__number_of_lines = number

    def is_centered(self) -> bool:
        return self.__center_text

    def get_max_line_size(self) -> float:
        return self.__line_max_size

    def get_text_string(self) -> str:
        return self.__text_string

    def set_text_string(self, text: str) -> None:
        self.__text_string = text
        TextMaster.remove_text(self)
        TextMaster.load_text(self)
