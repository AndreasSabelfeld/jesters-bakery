from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class Ingredient:
    def __init__(self, content: str, loader: Loader, fill_texture: str):
        self.__content = content
        self.__texture = ModelTexture(loader.load_texture(fill_texture))

    def get_content(self) -> str:
        return self.__content

    def get_texture(self) -> ModelTexture:
        return self.__texture
