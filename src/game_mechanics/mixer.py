from threading import Thread
from time import sleep

from src.game_mechanics.game_object import GameObject


class Mixer:
    def __init__(self, mixer_game_object: GameObject):
        self.__mixer = mixer_game_object
        self.__mixing_time = 3
        self.__mixing = False

    def place_vessel(self, vessel: GameObject) -> None:
        vessel.set_position(self.__mixer.get_position())

    def start_mix(self, vessel: GameObject) -> None:
        vessel.set_pickup_able(False)
        process = Thread(target=self.__mix, args=(vessel,))
        process.start()

    def __mix(self, vessel: GameObject):
        sleep(3)
        vessel.set_pickup_able(True)
