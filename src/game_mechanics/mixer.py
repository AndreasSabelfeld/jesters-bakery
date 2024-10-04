from threading import Thread
from time import sleep

from src.audio.audio_master import AudioMaster
from src.game_mechanics.game_object import GameObject
from src.toolbox.path import PATH


class Mixer:
    def __init__(self, mixer_game_object: GameObject):
        """
        Initializes the Mixer (meant to be blender) with a game object of the blender.

        :param mixer_game_object: The GameObject of the mixer.
        """
        self.__mixer = mixer_game_object
        self.__mixing_time = 3
        self.__mixing = False
        self.__blend_sound = AudioMaster.load_sound(f"{PATH}/res/audio/short_blend.wav")

    def place_vessel(self, vessel: GameObject) -> None:
        """
        Places the specified vessel at the blender’s current position.

        :param vessel: The GameObject of the vessel to be placed.
        """
        vessel.set_position(self.__mixer.get_position())

    def start_mix(self, vessel: GameObject) -> None:
        """
        Starts the mixing process for the specified vessel.
        It plays the blending sound and initiates a thread to handle mixing.

        :param vessel: The GameObject of the vessel to be mixed.
        """
        self.__mixer.get_sfx_source().play(self.__blend_sound)
        vessel.set_pickup_able(False)
        process = Thread(target=self.__mix, args=(vessel,))
        process.start()

    def __mix(self, vessel: GameObject) -> None:
        """
        Handles the mixing process. It sleeps for the mixing duration,
        then makes the vessel pickable again and appends "Mixed" to its contents
        if it has any.

        :param vessel: The GameObject of the vessel being mixed.
        """
        sleep(3)
        vessel.set_pickup_able(True)
        if vessel.get_attachment().get_content():
            vessel.get_attachment().append_content("Mixed")
