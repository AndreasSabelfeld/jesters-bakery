import inputs
from OpenGL.GL import *
from OpenGL.GLUT import *
from inputs import get_gamepad
import math
import threading


class Binds:
    INTERACT = 0
    CONFIRM = 1
    DPAD_UP = 2
    DPAD_DOWN = 3
    DPAD_LEFT = 4
    DPAD_RIGHT = 5
    LEFT_JOYSTICK = 6
    RIGHT_JOYSTICK = 7
    R2 = 8
    L2 = 9
    R1 = 10
    L1 = 11
    OPTIONS = 12

    dict = {
        INTERACT: ("Ｆ", "⇠", "⇐"),
        CONFIRM: ("␮", "⇣", "⇓"),
        DPAD_UP: ("Ｗ", "↟", "↟"),
        DPAD_DOWN: ("Ｓ", "↡", "↡"),
        DPAD_LEFT: ("Ａ", "↞", "↞"),
        DPAD_RIGHT: ("Ｄ", "↠", "↠"),
        LEFT_JOYSTICK: ("␣", "↺", "↺"),
        RIGHT_JOYSTICK: ("Mouse", "↻", "↻"),
        R2: ("Ｅ", "↳", "↗"),
        L2: ("Ｑ", "↲", "↖"),
        R1: ("Ｃ", "↱", "↙"),
        L1: ("Ｙ", "↰", "↘"),
        OPTIONS: ("␯", "⇨", "⇻")
    }

    @classmethod
    def get_bind(cls, bind: int) -> str:
        if ControllerInput.is_using_controller:
            return cls.dict.get(bind)[1]
        else:
            return cls.dict.get(bind)[0]


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

    __dead_zone = 0.2
    __sensitivity = 10

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
            try:
                events = get_gamepad()
            except inputs.UnpluggedError:
                cls.is_using_controller = False
                return
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
                    cls.Y_triangle = event.state    # previously switched with X
                elif event.code == 'BTN_WEST':
                    cls.X_square = event.state      # previously switched with Y
                elif event.code == 'BTN_EAST':
                    cls.B_circle = event.state
                elif event.code == 'BTN_THUMBL':
                    cls.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    cls.RightThumb = event.state
                elif event.code == 'BTN_START':
                    cls.Back = event.state
                elif event.code == 'BTN_SELECT':
                    cls.Start = event.state

                # Andreas Sabelfeld: changed the code from here as the event codes and states where wrong
                elif event.code == 'ABS_HAT0X' and event.state == -1:
                    # print(event.state) -1
                    cls.LeftDPad = event.state
                elif event.code == 'ABS_HAT0X' and event.state == 0:
                    # print(event.state) 0
                    cls.RightDPad = event.state
                elif event.code == 'ABS_HAT0Y' and event.state == 1:
                    # print(event.state) 1
                    cls.UpDPad = event.state
                elif event.code == 'ABS_HAT0Y' and event.state == 0:
                    # print(event.state) 0
                    cls.DownDPad = event.state
                elif event.code != "SYN_REPORT":
                    print(event.code, event.state)

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


class UniversalInput:
    __controller = ControllerInput(True)
    __keyboard = KeyboardInputListener()

    __left_cooldown = False
    __right_cooldown = False
    __up_cooldown = False
    __down_cooldown = False
    __confirm_cooldown = False
    __deny_cooldown = False
    __interact_cooldown = False
    __r2_cooldown = False
    __l2_cooldown = False
    __r1_cooldown = False
    __l1_cooldown = False
    __options_cooldown = False

    @classmethod
    def set_using_controller(cls, using: bool) -> None:
        cls.__controller.is_using_controller = using
        cls.__controller.restart_monitor_thread()

    @classmethod
    def get_x_axis_movement(cls) -> float:
        if cls.__controller.is_using_controller:
            if abs(cls.__controller.LeftJoystickX) > ControllerInput.get_dead_zone():
                return cls.__controller.LeftJoystickX
            else:
                return 0
        elif cls.__keyboard.get_keys_held().get(b'a'):
            return -1
        elif cls.__keyboard.get_keys_held().get(b'd'):
            return 1
        else:
            return 0

    @classmethod
    def get_y_axis_movement(cls) -> float:
        if cls.__controller.is_using_controller:
            if abs(cls.__controller.LeftJoystickY) > ControllerInput.get_dead_zone():
                return -cls.__controller.LeftJoystickY
            else:
                return 0
        elif cls.__keyboard.get_keys_held().get(b'w'):
            return -1
        elif cls.__keyboard.get_keys_held().get(b's'):
            return 1
        else:
            return 0

    @classmethod
    def get_x_axis_rotation(cls) -> float:
        if cls.__controller.is_using_controller:
            if abs(cls.__controller.RightJoystickX) > ControllerInput.get_dead_zone():
                return -cls.__controller.RightJoystickX * ControllerInput.get_sensitivity() * 10
            else:
                return 0
        else:
            return KeyboardInput.get_dx()

    @classmethod
    def get_y_axis_rotation(cls) -> float:
        if cls.__controller.is_using_controller:
            if abs(cls.__controller.RightJoystickY) > ControllerInput.get_dead_zone():
                return cls.__controller.RightJoystickY * ControllerInput.get_sensitivity() * 10
            else:
                return 0
        else:
            return KeyboardInput.get_dy()

    @classmethod
    def get_left(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftJoystickX < -0.8 and not cls.__left_cooldown:
                cls.__left_cooldown = True
                return True
            elif cls.__controller.LeftJoystickX > -cls.__controller.get_dead_zone() and cls.__left_cooldown:
                cls.__left_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'a'):
            return True
        else:
            return False

    @classmethod
    def get_right(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftJoystickX > 0.8 and not cls.__right_cooldown:
                cls.__right_cooldown = True
                return True
            elif cls.__controller.LeftJoystickX < cls.__controller.get_dead_zone() and cls.__right_cooldown:
                cls.__right_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'd'):
            return True
        else:
            return False

    @classmethod
    def get_up(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftJoystickY > 0.8 and not cls.__up_cooldown:
                cls.__up_cooldown = True
                return True
            elif cls.__controller.LeftJoystickY < cls.__controller.get_dead_zone() and cls.__up_cooldown:
                cls.__up_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'w'):
            return True
        else:
            return False

    @classmethod
    def get_down(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftJoystickY < -0.8 and not cls.__down_cooldown:
                cls.__down_cooldown = True
                return True
            elif cls.__controller.LeftJoystickY > -cls.__controller.get_dead_zone() and cls.__down_cooldown:
                cls.__down_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b's'):
            return True
        else:
            return False

    @classmethod
    def get_confirm(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.A_cross and not cls.__confirm_cooldown:
                cls.__confirm_cooldown = True
                return True
            elif not cls.__controller.A_cross and cls.__confirm_cooldown:
                cls.__confirm_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'\r'):
            return True
        else:
            return False

    @classmethod
    def get_deny(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.B_circle and not cls.__deny_cooldown:
                cls.__deny_cooldown = True
                return True
            elif not cls.__controller.B_circle and cls.__deny_cooldown:
                cls.__deny_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'f'):
            return True
        else:
            return False

    @classmethod
    def get_interact(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.X_square and not cls.__interact_cooldown:
                cls.__interact_cooldown = True
                return True
            elif not cls.__controller.X_square and cls.__interact_cooldown:
                cls.__interact_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'f'):
            return True
        else:
            return False

    @classmethod
    def get_r2(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.RightTrigger and not cls.__r2_cooldown:
                cls.__r2_cooldown = True
                return True
            elif not cls.__controller.RightTrigger and cls.__r2_cooldown:
                cls.__r2_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'e'):
            return True
        else:
            return False

    @classmethod
    def get_l2(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftTrigger and not cls.__l2_cooldown:
                cls.__l2_cooldown = True
                return True
            elif not cls.__controller.LeftTrigger and cls.__l2_cooldown:
                cls.__l2_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'q'):
            return True
        else:
            return False

    @classmethod
    def get_r1(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.RightBumper and not cls.__r1_cooldown:
                cls.__r1_cooldown = True
                return True
            elif not cls.__controller.RightBumper and cls.__r1_cooldown:
                cls.__r1_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'c'):
            return True
        else:
            return False

    @classmethod
    def get_l1(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.LeftBumper and not cls.__l1_cooldown:
                cls.__l1_cooldown = True
                return True
            elif not cls.__controller.LeftTrigger and cls.__l1_cooldown:
                cls.__l1_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'y'):
            return True
        else:
            return False

    @classmethod
    def get_options(cls) -> bool:
        if cls.__controller.is_using_controller:
            if cls.__controller.Start and not cls.__options_cooldown:
                cls.__options_cooldown = True
                return True
            elif not cls.__controller.Start and cls.__options_cooldown:
                cls.__options_cooldown = False
                return False
            else:
                return False
        elif cls.__keyboard.on_key_down(b'\x1b'):
            return True
        else:
            return False


class UniversalInputListener(UniversalInput):
    def __init__(self):
        self.__controller = ControllerInput(True)
        self.__keyboard = KeyboardInputListener()

        self.__left_cooldown = False
        self.__right_cooldown = False
        self.__up_cooldown = False
        self.__down_cooldown = False
        self.__confirm_cooldown = False
        self.__deny_cooldown = False
        self.__interact_cooldown = False
        self.__r2_cooldown = False
        self.__l2_cooldown = False
        self.__r1_cooldown = False
        self.__l1_cooldown = False
        self.__options_cooldown = False

    def set_using_controller(self, using: bool) -> None:
        self.__controller.is_using_controller = using
        self.__controller.restart_monitor_thread()

    def get_x_axis_movement(self) -> float:
        return super().get_x_axis_movement()

    def get_y_axis_movement(self) -> float:
        return super().get_y_axis_movement()

    def get_x_axis_rotation(self) -> float:
        return super().get_x_axis_rotation()

    def get_y_axis_rotation(self) -> float:
        return super().get_y_axis_rotation()

    def get_left(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftJoystickX < -0.8 and not self.__left_cooldown:
                self.__left_cooldown = True
                return True
            elif self.__controller.LeftJoystickX > -self.__controller.get_dead_zone() and self.__left_cooldown:
                self.__left_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'a'):
            return True
        else:
            return False

    def get_right(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftJoystickX > 0.8 and not self.__right_cooldown:
                self.__right_cooldown = True
                return True
            elif self.__controller.LeftJoystickX < self.__controller.get_dead_zone() and self.__right_cooldown:
                self.__right_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'd'):
            return True
        else:
            return False

    def get_up(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftJoystickY > 0.8 and not self.__up_cooldown:
                self.__up_cooldown = True
                return True
            elif self.__controller.LeftJoystickY < self.__controller.get_dead_zone() and self.__up_cooldown:
                self.__up_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'w'):
            return True
        else:
            return False

    def get_down(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftJoystickY < -0.8 and not self.__down_cooldown:
                self.__down_cooldown = True
                return True
            elif self.__controller.LeftJoystickY > -self.__controller.get_dead_zone() and self.__down_cooldown:
                self.__down_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b's'):
            return True
        else:
            return False

    def get_confirm(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.A_cross and not self.__confirm_cooldown:
                self.__confirm_cooldown = True
                return True
            elif not self.__controller.A_cross and self.__confirm_cooldown:
                self.__confirm_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'\r'):
            return True
        else:
            return False

    def get_deny(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.B_circle and not self.__deny_cooldown:
                self.__deny_cooldown = True
                return True
            elif not self.__controller.B_circle and self.__deny_cooldown:
                self.__deny_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'f'):
            return True
        else:
            return False

    def get_interact(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.X_square and not self.__interact_cooldown:
                self.__interact_cooldown = True
                return True
            elif not self.__controller.X_square and self.__interact_cooldown:
                self.__interact_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'f'):
            return True
        else:
            return False

    def get_r2(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.RightTrigger and not self.__r2_cooldown:
                self.__r2_cooldown = True
                return True
            elif not self.__controller.RightTrigger and self.__r2_cooldown:
                self.__r2_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'e'):
            return True
        else:
            return False

    def get_l2(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftTrigger and not self.__l2_cooldown:
                self.__l2_cooldown = True
                return True
            elif not self.__controller.LeftTrigger and self.__l2_cooldown:
                self.__l2_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'q'):
            return True
        else:
            return False

    def get_r1(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.RightBumper and not self.__r1_cooldown:
                self.__r1_cooldown = True
                return True
            elif not self.__controller.RightBumper and self.__r1_cooldown:
                self.__r1_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'c'):
            return True
        else:
            return False

    def get_l1(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.LeftBumper and not self.__l1_cooldown:
                self.__l1_cooldown = True
                return True
            elif not self.__controller.LeftTrigger and self.__l1_cooldown:
                self.__l1_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'y'):
            return True
        else:
            return False

    def get_options(self) -> bool:
        if self.__controller.is_using_controller:
            if self.__controller.Start and not self.__options_cooldown:
                self.__options_cooldown = True
                return True
            elif not self.__controller.Start and self.__options_cooldown:
                self.__options_cooldown = False
                return False
            else:
                return False
        elif self.__keyboard.on_key_down(b'\x1b'):
            return True
        else:
            return False
