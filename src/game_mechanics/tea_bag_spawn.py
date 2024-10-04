from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.obj_converter.obj_loader import OBJLoader
from src.render_engine.input_controller import Binds
from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class TeaBagSpawn:
    """
    Represents a spawn point for tea bags and their packaging.
    """

    def __init__(self, pos: list[float], rot: list[float], size: float, packaging_texture: ModelTexture,
                 bag_texture: ModelTexture, loader: Loader, obj_loader: OBJLoader, entities: list, colliders: list,
                 name: str):
        """Initializes the TeaBagSpawn instance.

        :param pos: The position of the tea bag spawn
        :param rot: The rotation of the tea bag spawn in degrees.
        :param size: The size of the tea bags
        :param packaging_texture: The texture for the tea packaging.
        :param bag_texture: The texture for the tea bag.
        :param loader: The texture loader for loading textures.
        :param obj_loader: The object loader
        :param entities: The list to which the tea packaging GameObject will be added.
        :param colliders: The list to which the tea packaging GameObject collider will be added.
        :param name: The name of the tea bag spawn.
        """
        self.__size = size
        self.__rot = rot
        self.__pos = pos
        self.__bag_texture = bag_texture
        self.__packaging_texture = packaging_texture
        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__colliders = colliders
        self.__entities = entities
        self.__name = name

        model = self.__obj_loader.load_obj_model("objs/ingredients/tea_packaging", self.__loader)
        static_model = TexturedModel(model, self.__packaging_texture)
        static_collider = TexturedModel(self.__obj_loader.load_obj_model("objs/ingredients/tea_packaging", self.__loader),
                                        ModelTexture(self.__loader.load_texture("")))

        ent = Entity(static_model, self.__pos, *self.__rot, self.__size)
        collider = Entity(static_collider, self.__pos, *self.__rot, self.__size)
        self.__packaging_go = GameObject(ent, collider=collider)
        self.__packaging_go.set_attachment(self)
        self.__packaging_go.set_ext_name(name)
        self.__packaging_go.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to pick up")
        self.__entities.append(self.__packaging_go)
        self.__colliders.append(self.__packaging_go)

    def spawn(self) -> GameObject:
        """
        Spawns a tea bag and adds it to the entities and colliders.

        :return: The GameObject representing the spawned tea bag.
        """
        model = self.__obj_loader.load_obj_model("objs/ingredients/tea_bag", self.__loader)
        static_model = TexturedModel(model, self.__bag_texture)
        static_collider = TexturedModel(self.__obj_loader.load_obj_model("objs/ingredients/tea_bag_collider", self.__loader),
                                        ModelTexture(self.__loader.load_texture("")))

        ent = Entity(static_model, self.__pos, *self.__rot, self.__size)
        collider = Entity(static_collider, self.__pos, *self.__rot, self.__size)
        bag = GameObject(ent, collider=collider, int_name="TEA_BAG")
        bag.set_ext_name(self.__name)
        bag.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to pick up")
        self.__entities.append(bag)
        self.__colliders.append(bag)
        return bag

    def get_name(self) -> str:
        """Returns the name of the tea bag spawn.

        :return: A string representing the name of the tea bag spawn.
        """
        return self.__name

    def get_packaging_game_object(self) -> GameObject:
        """Returns the GameObject of the packaging.

        :return: The GameObject representing the tea packaging.
        """
        return self.__packaging_go
