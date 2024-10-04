from src.render_engine.loader import Loader
from src.font_rendering.font_renderer import FontRenderer


class TextMaster:
    """Singleton class keeps track off all Text objects."""

    __loader = None
    __renderer = None
    __texts = dict()

    def __init__(self, loader: Loader):
        """Initializes the TextMaster with the loader.

        :param loader: An instance of the Loader class used to load font data.
        """
        TextMaster.__renderer = FontRenderer()
        TextMaster.__loader = loader

    @classmethod
    def render(cls) -> None:
        """Renders all texts managed by the TextMaster."""
        cls.__renderer.render(cls.__texts)

    @classmethod
    def render_specified(cls, gui_texts: list) -> None:
        """Renders only the specified texts from the provided list.

        :param gui_texts: A list of GUIText objects to be rendered.
        """
        specified_texts = {}
        for key in cls.__texts.keys():
            intersection = [value for value in cls.__texts[key] if value in gui_texts]
            specified_texts.update({key: intersection})

        cls.__renderer.render(specified_texts)

    @classmethod
    def render_not_specified(cls, gui_texts: list) -> None:
        """Renders texts that are not in the specified list.

        :param gui_texts: A list of GUIText objects that should not be rendered.
        """
        unspecified_texts = {}
        for key in cls.__texts.keys():
            difference = [value for value in cls.__texts[key] if value not in gui_texts]
            unspecified_texts.update({key: difference})

        cls.__renderer.render(unspecified_texts)

    @classmethod
    def load_text(cls, text) -> None:
        """Loads a text object and prepares it for rendering.

        :param text: The GUIText object to be loaded.
        """
        font = text.get_font()
        data = font.load_text(text)
        vao = cls.__loader.load_font_to_vao(data.get_vertex_positions(), data.get_texture_coords())
        text.set_mesh_info(vao, data.get_vertex_count())
        text_batch = cls.__texts.get(font)
        if text_batch is None:
            text_batch = []
            cls.__texts.update({font: text_batch})
        text_batch.append(text)

    @classmethod
    def remove_text(cls, text) -> None:
        """Removes a text object from the TextMaster.

        :param text: The GUIText object to be removed.
        """
        text_batch = cls.__texts.get(text.get_font())
        text_batch.remove(text)
        if not text_batch:
            cls.__texts.pop(text.get_font())

    @classmethod
    def clean_up(cls) -> None:
        """Cleans up the resources used by the TextMaster."""
        cls.__renderer.clean_up()

    @classmethod
    def get_renderer(cls) -> FontRenderer:
        """Gets the FontRenderer instance.

        :return: The FontRenderer instance.
        """
        return cls.__renderer

    @classmethod
    def get_loader(cls) -> Loader:
        """Gets the Loader instance.

        :return: The Loader instance.
        """
        return cls.__loader

    @classmethod
    def get_texts(cls) -> dict:
        """Gets the dictionary of texts managed by the TextMaster.

        :return: A dictionary mapping fonts to lists of GUIText objects.
        """
        return cls.__texts
