from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class Instructions:
    def __init__(self, parent: Entity, loader: Loader):
        """
        Initializes the Instructions with a parent entity and a texture loader.

        :param parent: The parent entity that will display the instructions.
        :param loader: The Loader instance to load the instruction pages' textures.
        """
        self.__parent = parent
        self.__loader = loader
        self.__pages = []
        self.__load_pages()
        self.__current_page = 0
        self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def scroll_next(self) -> None:
        """
        Scrolls to the next page of instructions, if available.
        """
        if self.__current_page < len(self.__pages) - 1:
            self.__current_page += 1
            self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def scroll_previous(self) -> None:
        """
        Scrolls to the previous page of instructions, if available.
        """
        if self.__current_page > 0:
            self.__current_page -= 1
            self.__parent.get_model().set_texture(self.__pages[self.__current_page])

    def __load_pages(self) -> None:
        """
        Loads the instruction pages from the specified texture files.
        Each page is loaded as a ModelTexture and added to the pages list.
        """
        for i in range(1, 15):
            self.__pages.append(ModelTexture(self.__loader.load_texture(f"pngs/ui/instructions/page_{i}")))
