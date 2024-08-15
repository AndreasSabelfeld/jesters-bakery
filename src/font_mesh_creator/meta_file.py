from src.render_engine.display_manager import DisplayManager
from src.font_mesh_creator.character import Character


class MetaFile:

    __PAD_TOP = 0
    __PAD_LEFT = 1
    __PAD_BOTTOM = 2
    __PAD_RIGHT = 3

    __DESIRED_PADDING = 10

    __SPLITTER = ' '
    __NUMBER_SEPERATOR = ','

    def __init__(self, file: str):
        self.__vertical_per_pixel_size = -1
        self.__horizontal_per_pixel_size = -1
        self.__space_width = -1
        self.__padding = []
        self.__padding_width = -1
        self.__padding_height = -1
        self.__meta_data = dict()
        self.__reader = None
        self.__values = dict()

        self.__aspect_ratio = DisplayManager.get_width() / DisplayManager.get_height()
        self.open_file(file)
        self.load_padding_data()
        self.load_line_sizes()
        image_width = self.get_value_of_variable("scaleW")
        self.load_character_data(image_width)
        self.close()

    def get_space_width(self) -> float:
        return self.__space_width

    def get_character(self, ascii: int) -> Character:
        return self.__meta_data.get(ascii)

    def open_file(self, file: str) -> None:
        try:
            self.__reader = open(file, 'r')
        except Exception as e:
            print(e)

    def close(self) -> None:
        try:
            self.__reader.close()
        except Exception as e:
            print(e)

    def process_next_line(self) -> bool:
        self.__values.clear()
        line = None
        try:
            line = self.__reader.readline()
        except Exception as e:
            print(e)
        if not line:
            return False
        for part in line.split(self.__SPLITTER):
            value_pairs = part.split("=")
            if len(value_pairs) == 2:
                self.__values.update({value_pairs[0]: value_pairs[1]})
        return True

    def get_value_of_variable(self, variable: str) -> int:
        value = self.__values.get(variable)
        if not value:
            value = 0
        return int(value)

    def get_values_of_variable(self, variable: str) -> list[int]:
        numbers = self.__values.get(variable).split(self.__NUMBER_SEPERATOR)
        actual_values = [0] * len(numbers)
        for i in range(len(actual_values)):
            actual_values[i] = int(numbers[i])
        return actual_values

    def load_padding_data(self) -> None:
        """
        Loads the data about how much padding is used around each character in
        the texture atlas.
        """
        self.process_next_line()
        self.__padding = self.get_values_of_variable("padding")
        self.__padding_width = self.__padding[self.__PAD_LEFT] + self.__padding[self.__PAD_RIGHT]
        self.__padding_height = self.__padding[self.__PAD_TOP] + self.__padding[self.__PAD_BOTTOM]

    def load_line_sizes(self) -> None:
        """
        Loads information about the line height for this font in pixels, and uses
        this as a way to find the conversion rate between pixels in the texture
        atlas and screen-space.
        """
        self.process_next_line()
        line_height_pixels = self.get_value_of_variable("lineHeight") - self.__padding_height
        self.__vertical_per_pixel_size = 0.003 / line_height_pixels  # 0.003 = LINE_HEIGHT (magic number to prevent circular import)
        self.__horizontal_per_pixel_size = self.__vertical_per_pixel_size / self.__aspect_ratio

    def load_character_data(self, image_width: int) -> None:
        self.process_next_line()
        self.process_next_line()
        while self.process_next_line():
            c = self.load_character(image_width)
            if c is not None:
                self.__meta_data.update({c.get_id(): c})

    def load_character(self, image_size: int) -> Character:
        id = self.get_value_of_variable("id")
        if id == 32:  # space ascii (magic number to prevent circular import)
            self.__space_width = (self.get_value_of_variable("xadvance") - self.__padding_width) * self.__horizontal_per_pixel_size
            return None
        x_tex = (self.get_value_of_variable("x") + (self.__padding[self.__PAD_LEFT] - self.__DESIRED_PADDING)) / image_size
        y_tex = (self.get_value_of_variable("y") + (self.__padding[self.__PAD_TOP] - self.__DESIRED_PADDING)) / image_size
        width = self.get_value_of_variable("width") - (self.__padding_width - (2 * self.__DESIRED_PADDING))
        height = self.get_value_of_variable("height") - (self.__padding_height - (2 * self.__DESIRED_PADDING))
        quad_width = width * self.__horizontal_per_pixel_size
        quad_height = height * self.__vertical_per_pixel_size
        x_tex_size = width / image_size
        y_tex_size = height / image_size
        x_off = (self.get_value_of_variable("xoffset") + self.__padding[self.__PAD_LEFT] - self.__DESIRED_PADDING) * self.__horizontal_per_pixel_size
        y_off = (self.get_value_of_variable("yoffset") + self.__padding[self.__PAD_TOP] - self.__DESIRED_PADDING) * self.__vertical_per_pixel_size
        x_advance = (self.get_value_of_variable("xadvance") - self.__padding_width) * self.__horizontal_per_pixel_size
        return Character(id, x_tex, y_tex, x_tex_size, y_tex_size, x_off, y_off, quad_width, quad_height, x_advance)

