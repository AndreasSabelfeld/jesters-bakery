from src.entities.entity import Entity
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.obj_converter.obj_loader import OBJLoader
from src.render_engine.loader import Loader
from src.textures.model_texture import ModelTexture


class TeaBagSpawn:
    def __init__(self, pos: list[float], rot: list[float], size: float, packaging_texture: ModelTexture,
                 bag_texture: ModelTexture, loader: Loader, obj_loader: OBJLoader, entities: list, colliders: list,
                 name: str):
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
        self.__packaging_go.set_info(name)
        self.__entities.append(self.__packaging_go)
        self.__colliders.append(self.__packaging_go)

    def spawn(self) -> GameObject:
        model = self.__obj_loader.load_obj_model("objs/ingredients/tea_bag", self.__loader)
        static_model = TexturedModel(model, self.__bag_texture)
        static_collider = TexturedModel(self.__obj_loader.load_obj_model("objs/ingredients/tea_bag_collider", self.__loader),
                                        ModelTexture(self.__loader.load_texture("")))

        ent = Entity(static_model, self.__pos, *self.__rot, self.__size)
        collider = Entity(static_collider, self.__pos, *self.__rot, self.__size)
        bag = GameObject(ent, collider=collider, int_name="TEA_BAG")
        bag.set_info(self.__name)
        self.__entities.append(bag)
        self.__colliders.append(bag)
        return bag

    def get_name(self) -> str:
        return self.__name
