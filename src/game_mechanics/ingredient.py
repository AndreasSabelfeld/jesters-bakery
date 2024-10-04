from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class Ingredient:
    def __init__(self, content: str, loader: Loader, fill_texture: str):
        """
        Initializes an Ingredient with content and a texture.

        :param content: The content of the ingredient.
        :param loader: The Loader instance to load the texture.
        :param fill_texture: The file path or name of the texture to fill.
        """
        self.__content = content
        self.__texture = ModelTexture(loader.load_texture(fill_texture))

    def get_content(self) -> str:
        """
        Returns the content of this ingredient.
        """
        return self.__content

    def get_texture(self) -> ModelTexture:
        """
        Returns the texture of this ingredient.
        """
        return self.__texture
