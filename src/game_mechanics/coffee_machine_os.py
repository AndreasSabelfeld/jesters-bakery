from math import sqrt
from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.pycgtypes import vec3, mat3


class CoffeeMachineOS:

    def __init__(self, render_target, product_entries: list) -> None:
        self.__render_target = render_target
        self.__product_entries = product_entries
        self.__background_texture = None
        self.__interaction_key = b'f'
        self.__interaction_radius = 10
        self.__is_interacting = False
        self.__original_camera_pos = None
        self.__original_camera_angles = None

    def check_for_interaction(self, player, camera) -> None:
        distance = sqrt((self.__render_target.get_position()[0] - player.get_position()[0])**2 +
                        (self.__render_target.get_position()[1] - player.get_position()[1])**2 +
                        (self.__render_target.get_position()[2] - player.get_position()[2])**2)
        if distance < self.__interaction_radius:
            if KeyboardInput.get_keys_held().get(self.__interaction_key):
                if not self.__is_interacting:
                    self.__is_interacting = True
                    self.move_in_front_screen(camera)
                else:
                    self.__is_interacting = False
                    self.move_camera_to_original_pos(camera)

    def move_in_front_screen(self, camera):
        self.__original_camera_pos = camera.get_position()
        self.__original_camera_angles = [camera.get_yaw(), camera.get_pitch(), camera.get_roll()]
        offset = vec3(0, 2.5, 3.5)
        rot_mat = mat3().rotation(self.__render_target.get_rot_x(), vec3(1, 1, 1))
        offset = rot_mat * offset

        position = vec3(self.__render_target.get_position()) + offset

        camera.set_position(position)
        camera.set_yaw(0)
        camera.set_pitch(0)
        camera.set_roll(0)

    def move_camera_to_original_pos(self, camera):
        camera.set_yaw(self.__original_camera_angles[0])
        camera.set_pitch(self.__original_camera_angles[1])
        camera.set_roll(self.__original_camera_angles[2])
        camera.set_position(self.__original_camera_pos)

    def get_is_interacting(self) -> bool:
        return self.__is_interacting
