from threading import Thread

from src.render_engine.input_controller import KeyboardInput, ControllerInput, UniversalInput
from math import sin, cos, radians
from src.entities.player import FirstPersonPlayer
from src.render_engine.time import Time


class Camera:
    """
    Camera class that keeps track of the angles and position in class variables
    """
    __position = [0.0, 0.0, 0.0]
    __pitch = 20
    __yaw = 0
    __roll = 0
    __inverse_y = True

    def __init__(self, player):
        """Creates a camera object and takes a player entity object as parameter"""
        self.__distance_from_player = 50        # default distance
        if type(player) is FirstPersonPlayer:
            self.__distance_from_player = 0     # if we're in 1st person the camera is in the player
        self.__angle_around_player = 0

        self.__player = player

    def move(self):
        """Move function that is meant to be used in a loop.
           Updates the zoom, rotation and position of the camera."""
        self.calculate_zoom()
        self.calculate_pitch()
        self.calculate_angle_around_player()

        horizontal_distance = self.calculate_horizontal_distance()              # horizontal distance
        vertical_distance = self.calculate_vertical_distance()                  # vertical distance
        self.calculate_camera_position(horizontal_distance, vertical_distance)  # calculate concrete position xyz
        Camera.set_yaw(-1 * self.__angle_around_player)                         # angle around the player
        self.__player.set_rot_y(-self.get_yaw())         # make the player rotation the same as the camera rotation

    @classmethod
    def set_position(cls, position: list[float]):
        """Class method setter that changes the class variable 'position' to a vector (list of 3 floats)"""
        cls.__position = position

    @classmethod
    def get_position(cls) -> list[float]:
        """Class method getter that returns the class variable 'position'"""
        return cls.__position

    @classmethod
    def get_pitch(cls) -> float:
        """Class method getter that returns the class variable 'pitch'"""
        return cls.__pitch

    @classmethod
    def set_pitch(cls, pitch: float):
        """Class method setter that changes the class variable 'pitch' to an angle"""
        if -90 <= pitch <= 90:    # limit the angle to 90° both up and down
            cls.__pitch = pitch

    @classmethod
    def invert_pitch(cls):
        cls.__pitch = -cls.__pitch

    @classmethod
    def get_yaw(cls) -> float:
        """Class method getter that returns the class variable 'yaw'"""
        return cls.__yaw

    @classmethod
    def set_yaw(cls, yaw: float):
        """Class method setter that changes the class variable 'yaw' to an angle"""
        cls.__yaw = yaw

    @classmethod
    def get_roll(cls) -> float:
        """Class method getter that returns the class variable 'roll'"""
        return cls.__roll

    @classmethod
    def set_roll(cls, roll: float):
        """Class method setter that changes the class variable 'roll' to an angle"""
        cls.__roll = roll

    def calculate_camera_position(self, horizontal_distance: float, vertical_distance: float) -> None:
        """Function that calculates and applies the new position of the camera"""
        theta = self.__angle_around_player
        offset_x = horizontal_distance * sin(radians(theta))
        offset_z = horizontal_distance * cos(radians(theta))
        self.__position[0] = self.__player.get_position()[0] + offset_x
        self.__position[1] = self.__player.get_position()[1] + vertical_distance
        self.__position[2] = self.__player.get_position()[2] + offset_z

    def calculate_horizontal_distance(self) -> float:
        """Calculates the horizontal distance of the camera to the player from the pitch with trigonometry"""
        return self.__distance_from_player * cos(radians(self.get_pitch()))

    def calculate_vertical_distance(self) -> float:
        """Calculates the vertical distance of the camera to the player from the pitch with trigonometry"""
        if not type(self.__player) is FirstPersonPlayer:  # if it's not in 1st person mode
            return self.__distance_from_player * sin(radians(self.get_pitch()))
        else:
            return FirstPersonPlayer.get_player_size()

    def calculate_zoom(self) -> None:
        """Calculates the zoom from the input controller"""
        # zoom_level = KeyboardInput.get_scroll() * 2
        # self.__distance_from_player -= zoom_level
        pass

    def calculate_pitch(self) -> None:
        """Calculates the pitch from the input controller"""
        inverse = -1 if self.get_inverse_y() else 1
        pitch_change = UniversalInput.get_y_axis_rotation() * 0.1 * inverse
        self.set_pitch(self.get_pitch() + pitch_change)

    def calculate_angle_around_player(self) -> None:
        """Calculates the angle change of the camera from the input controller"""
        angle_change = UniversalInput.get_x_axis_rotation() * 0.3
        self.__angle_around_player += angle_change

    def set_inverse_y(self, b: bool):
        """Sets the class variable 'inverse_y' to a boolean value. If true the camera Y-Axis will be inversed."""
        self.__inverse_y = b

    def get_inverse_y(self) -> bool:
        """Returns the class variable 'inverse_y'"""
        return self.__inverse_y

    def get_player(self):
        return self.__player
