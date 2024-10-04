from src.audio.audio_master import AudioMaster
from src.entities.entity import Entity
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.game_object import GameObject
from src.models.textured_model import TexturedModel
from src.render_engine.time import Time
from src.textures.model_texture import ModelTexture
from src.toolbox.path import PATH


class MixerVessel:
    def __init__(self, vessel: GameObject, obj_loader, loader):
        """
        Initializes the MixerVessel with a game object of the vessel.

        :param vessel: The GameObject of the mixer vessel.
        :param obj_loader: The obj loader
        :param loader: The loader for textures.
        """
        self.__vessel = vessel
        self.__obj_loader = obj_loader
        self.__loader = loader
        self.__content = list()
        self.__lvl = 0
        self.__max_lvl = 3
        self.__fill_cooldown = 0
        self.__content = []
        self.__texture = None
        self.__pour_sound = AudioMaster.load_sound(f"{PATH}/res/audio/pour.wav")

    def update(self) -> None:
        """
        Updates the fill cooldown timer, decrementing it based on the elapsed time.
        Resets the cooldown to zero if it has elapsed.
        """
        if self.__fill_cooldown > 0:
            self.__fill_cooldown -= Time.get_delta_time()
        else:
            self.__fill_cooldown = 0

    def get_model(self, level: int, texture: ModelTexture) -> TexturedModel:
        """
        Gets the TexturedModel for the specified level and texture.

        :param level: The level of the vessel's fill.
        :param texture: The texture to be applied to the model.
        :return: A TexturedModel instance of the vessel at the specified level.
        """
        return TexturedModel(self.__obj_loader.load_obj_model(f"objs/machinery/mixer_vessel_lvl_{level}", self.__loader), texture)

    def get_level(self) -> int:
        """
        Returns the current fill level of the vessel.

        :return: An integer of the current fill level.
        """
        return self.__lvl

    def set_level(self, level: int, texture: ModelTexture) -> None:
        """
        Sets the fill level of the vessel, updating its texture and playing the pour sound.

        :param level: The new fill level to set.
        :param texture: The texture to apply to the vessel model.
        """
        self.__vessel.get_sfx_source().play(self.__pour_sound)
        self.__lvl = level
        self.__vessel.set_child_0(Entity(self.get_model(self.__lvl, texture), self.__vessel.get_position(), 0, 0, 0,
                                         self.__vessel.get_scale()))
        self.__texture = texture

    def set_texture(self, texture: ModelTexture) -> None:
        """
        Sets the texture of the vessel by updating its level.

        :param texture: The ModelTexture to apply to the vessel.
        """
        self.set_level(self.get_level(), texture)

    @staticmethod
    def get_container_type() -> int:
        """
        Returns the type of container represented by this vessel.

        :return: An integer of the container type (e.g., BIG_GLASS).
        """
        return CoffeeContainer.BIG_GLASS

    def fill(self, texture: ModelTexture) -> None:
        """
        Fills the vessel with the specified texture, incrementing its fill level.

        :param texture: The ModelTexture to apply while filling the vessel.
        """
        if self.__fill_cooldown == 0 and self.__lvl < self.__max_lvl:
            self.__vessel.set_child_0(Entity(self.get_model(self.__lvl, texture),
                                             self.__vessel.get_position(),
                                             self.__vessel.get_rot_x(),
                                             self.__vessel.get_rot_y(),
                                             self.__vessel.get_rot_z(),
                                             self.__vessel.get_scale()))
            self.__vessel.get_sfx_source().play(self.__pour_sound)
            self.__lvl += 1
            self.__fill_cooldown = 1.5
            self.__texture = texture

    def empty(self) -> None:
        """
        Empties the vessel, removing its contents and resetting the fill level.
        """
        self.__vessel.remove_child_0()
        self.remove_content()
        self.__lvl = 0

    def append_content(self, content: str | list) -> None:
        """
        Appends the specified content to the vessel. Prevents duplicates if the last content is the same.

        :param content: The content to append, which can be a string or a list of strings.
        """
        if self.__content and self.__content[-1] == content:
            return
        if isinstance(content, str):
            self.__content.append(content)
        elif isinstance(content, list):
            self.__content.extend(content)

    def remove_content(self) -> list:
        """
        Removes and returns the current content of the vessel.

        :return: A list of the contents that were in the vessel before removal.
        """
        c = self.__content.copy()
        self.__content.clear()
        return c

    def get_content(self) -> list:
        """
        Returns a copy of the current content of the vessel.

        :return: A list of contents in the vessel.
        """
        return self.__content

    def get_texture(self) -> ModelTexture:
        """
        Returns the current texture of the vessel.

        :return: The ModelTexture currently applied to the vessel.
        """
        return self.__texture

    def get_fill_lvl(self) -> int:
        """
        Returns the current fill level of the vessel.

        :return: An integer of the current fill level.
        """
        return self.__lvl
