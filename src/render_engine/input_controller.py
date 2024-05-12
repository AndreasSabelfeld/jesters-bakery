from OpenGL.GL import *
from OpenGL.GLUT import *
from inputs import get_gamepad
import math
import threading


class KeyboardInput:
    """Class handling all the inputs from the opened OpenGL window"""
    __polygon_mode = False
    __keys_held = dict()
    __cooldowns = dict()

    __scroll = 0
    __last_direction = 0
    __mouse_pos = [0, 0]
    __mouse_keys_held = dict()

    __dy = 0.0
    __dx = 0.0

    __window_size = [0, 0]

    @classmethod
    def on_key_down(cls, key_to_check) -> bool:
        if key_to_check not in cls.__cooldowns.keys():
            cls.__cooldowns.update({key_to_check: False})
        # if key is held down for the first frame
        if cls.__keys_held.get(key_to_check) and not cls.__cooldowns.get(key_to_check):
            cls.__cooldowns.update({key_to_check: True})  # key is on cooldown
            return True
        if not cls.__keys_held.get(key_to_check) and cls.__cooldowns.get(key_to_check):
            cls.__cooldowns.update({key_to_check: False})  # key can be pressed again
        return False

    @classmethod
    def key_down(cls, player_input, *args):
        cls.__keys_held.update({player_input: True})

    @classmethod
    def key_up(cls, player_input, *args):
        cls.__keys_held.update({player_input: False})

    @classmethod
    def special_keys(cls, player_input, *args):
        if player_input == GLUT_KEY_F1:
            if not cls.get_polygon_mode():
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                cls.set_polygon_mode(True)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                cls.set_polygon_mode(False)

    @classmethod
    def mouse_buttons(cls, button: int, state: int, x: int, y: int):
        if not (button == 3 or button == 4):
            # if not the mouse wheel was used update pressed key
            cls.__mouse_keys_held.update({button: True})
        else:
            # else nothing was pressed, so make it false
            for key in cls.__mouse_keys_held.keys():
                cls.__mouse_keys_held[key] = False

    @classmethod
    def mouse_movement(cls, x: int, y: int):
        middle_x = cls.get_window_size()[0]
        middle_y = cls.get_window_size()[1]
        cls.__mouse_pos = [x, y]
        cls.__dx = middle_x - x
        cls.__dy = middle_y - y

    @classmethod
    def mouse_wheel(cls, button: int, direction: int, x: int, y: int):
        cls.__scroll = direction

    @classmethod
    def set_polygon_mode(cls, b: bool):
        cls.__polygon_mode = b

    @classmethod
    def get_polygon_mode(cls) -> bool:
        return cls.__polygon_mode

    @classmethod
    def get_keys_held(cls) -> dict:
        return cls.__keys_held

    @classmethod
    def get_mouse_keys_held(cls) -> dict:
        return cls.__mouse_keys_held

    @classmethod
    def get_mouse_pos(cls) -> list[float]:
        return cls.__mouse_pos

    @classmethod
    def get_scroll(cls) -> int:
        return cls.__scroll

    @classmethod
    def get_dx(cls) -> float:
        return cls.__dx

    @classmethod
    def get_dy(cls) -> float:
        return cls.__dy

    @classmethod
    def set_window_size(cls, size: list[int]) -> None:
        cls.__window_size = size

    @classmethod
    def get_window_size(cls) -> list[int, int]:
        return cls.__window_size

    @classmethod
    def get_cooldowns(cls) -> dict:
        return cls.__cooldowns


class KeyboardInputListener(KeyboardInput):
    """Individual Keyboard Listener working with instances"""

    def __init__(self):
        self.__cooldowns = dict()

    def on_key_down(self, key_to_check) -> bool:
        if key_to_check not in self.__cooldowns.keys():
            self.__cooldowns.update({key_to_check: False})
        # if key is held down for the first frame
        if self.get_keys_held().get(key_to_check) and not self.__cooldowns.get(key_to_check):
            self.__cooldowns.update({key_to_check: True})  # key is on cooldown
            return True
        if not self.get_keys_held().get(key_to_check) and self.__cooldowns.get(key_to_check):
            self.__cooldowns.update({key_to_check: False})  # key can be pressed again
        return False

    def get_keys_held(self) -> dict:
        return super().get_keys_held()

    def get_mouse_keys_held(self) -> dict:
        return super().get_mouse_keys_held()

    def get_mouse_pos(self) -> list[float]:
        return super().get_mouse_pos()

    def get_scroll(self) -> int:
        return super().get_scroll()

    def get_dx(self) -> float:
        return super().get_dx()

    def get_dy(self) -> float:
        return super().get_dx()

    def get_cooldowns(self) -> dict:
        return self.__cooldowns


# copied from https://stackoverflow.com/questions/46506850/how-can-i-get-input-from-an-xbox-one-controller-in-python
class ControllerInput(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    LeftJoystickY = 0
    LeftJoystickX = 0
    RightJoystickY = 0
    RightJoystickX = 0
    LeftTrigger = 0
    RightTrigger = 0
    LeftBumper = 0
    RightBumper = 0
    A_cross = 0
    X_square = 0
    Y_triangle = 0
    B_circle = 0
    LeftThumb = 0
    RightThumb = 0
    Back = 0
    Start = 0
    LeftDPad = 0
    RightDPad = 0
    UpDPad = 0
    DownDPad = 0

    __dead_zone = 0.1
    __sensitivity = 1

    is_using_controller = False

    def __init__(self, is_using_controller: bool):
        ControllerInput.is_using_controller = is_using_controller

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def restart_monitor_thread(self):
        self._monitor_thread.start()

    @classmethod
    def _monitor_controller(cls):
        while cls.is_using_controller:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    cls.LeftJoystickY = event.state / ControllerInput.MAX_JOY_VAL   # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    cls.LeftJoystickX = event.state / ControllerInput.MAX_JOY_VAL   # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    cls.RightJoystickY = event.state / ControllerInput.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    cls.RightJoystickX = event.state / ControllerInput.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    cls.LeftTrigger = event.state / ControllerInput.MAX_TRIG_VAL    # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    cls.RightTrigger = event.state / ControllerInput.MAX_TRIG_VAL   # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    cls.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    cls.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    cls.A_cross = event.state
                elif event.code == 'BTN_NORTH':
                    cls.Y_triangle = event.state                                            # previously switched with X
                elif event.code == 'BTN_WEST':
                    cls.X_square = event.state                                            # previously switched with Y
                elif event.code == 'BTN_EAST':
                    cls.B_circle = event.state
                elif event.code == 'BTN_THUMBL':
                    cls.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    cls.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    cls.Back = event.state
                elif event.code == 'BTN_START':
                    cls.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    cls.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    cls.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    cls.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    cls.DownDPad = event.state

    @classmethod
    def set_dead_zone(cls, val: float) -> None:
        if 0 <= val <= 1:
            cls.__dead_zone = val
        else:
            print("Dead zone value out of bounds (0 to 1)")

    @classmethod
    def get_dead_zone(cls) -> float:
        return cls.__dead_zone

    @classmethod
    def set_sensitivity(cls, val: float) -> None:
        if val > 0:
            cls.__sensitivity = val
        else:
            print("Sensitivity value must be over 0")

    @classmethod
    def get_sensitivity(cls) -> float:
        return cls.__sensitivity
