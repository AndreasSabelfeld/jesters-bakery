from src.render_engine.loader import Loader
from src.font_rendering.font_renderer import FontRenderer


class TextMaster:
    """Singleton class keeps track off all Text objects."""
    __loader = None
    __renderer = None
    __texts = dict()

    def __init__(self, loader: Loader):
        TextMaster.__renderer = FontRenderer()
        TextMaster.__loader = loader

    @classmethod
    def render(cls):
        cls.__renderer.render(cls.__texts)

    @classmethod
    def load_text(cls, text) -> None:
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
        text_batch = cls.__texts.get(text.get_font())
        text_batch.remove(text)
        if not text_batch:
            cls.__texts.pop(text.get_font())

    @classmethod
    def clean_up(cls) -> None:
        cls.__renderer.clean_up()

    @classmethod
    def get_renderer(cls) -> FontRenderer:
        return cls.__renderer

    @classmethod
    def get_loader(cls) -> Loader:
        return cls.__loader

    @classmethod
    def get_texts(cls) -> dict:
        return cls.__texts
