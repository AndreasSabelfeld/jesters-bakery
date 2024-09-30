from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class Instructions:
    def __init__(self, parent: Entity, loader: Loader):
        self.__parent = parent
        self.__loader = loader
        self.__pages = []
        self.__load_pages()
        self.__current_page = 0
        self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def scroll_next(self) -> None:
        if self.__current_page < len(self.__pages) - 1:
            self.__current_page += 1
            self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def scroll_previous(self) -> None:
        if self.__current_page > 0:
            self.__current_page -= 1
            self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def __load_pages(self) -> None:
        for i in range(1, 15):
            self.__pages.append(ModelTexture(self.__loader.load_texture(f"pngs/ui/instructions/page_{i}")))
