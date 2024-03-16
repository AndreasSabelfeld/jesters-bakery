from src.font_mesh_creator.text_mesh_creator import TextMeshCreator
from src.font_mesh_creator.gui_text import GUIText


class FontType:
    def __init__(self, texture_atlas: int, font_file: str):
        """
        Creates a new font and loads up the data about each character from the
        font file.
        :param texture_atlas:
        - the ID of the font atlas texture.
        :param font_file:
        - the font file containing information about each character in the texture atlas.
        """
        self.__texture_atlas = texture_atlas
        self.__loader = TextMeshCreator(font_file)

    def get_texture_atlas(self) -> int:
        return self.__texture_atlas

    def load_text(self, text: GUIText):
        """
        Takes in an unloaded text and calculate all of the vertices for the quads
        on which this text will be rendered. The vertex positions and texture
        coords and calculated based on the information from the font file.
        :param text: - the unloaded text.
        :return: Information about the vertices of all the quads.
        """
        return self.__loader.create_text_mesh(text)
