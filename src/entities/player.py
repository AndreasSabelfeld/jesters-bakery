from .entity import Entity
from src.toolbox.path import PATH
from src.render_engine.input_controller import KeyboardInput, ControllerInput, UniversalInput
from src.render_engine.time import Time
from src.terrain.terrain import Terrain
from src.pycgtypes import vec3

from src.collision.detection import Detection
from src.collision.plane import Plane
from src.collision.utility import convert_to_ellipsoid_space, convert_to_r3_space

import math

from ..audio.audio_master import AudioMaster
from ..audio.source import Source


class Player(Entity):
    """
    Base player class holding the speed, gravity, and jump power of the player. Inherits from the Entity class.
    """
    __instance = None

    __RUN_SPEED = 20
    __TURN_SPEED = 160
    __GRAVITY = -50
    __JUMP_POWER = 30

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        """Creates a player object with the specified model and transformation parameters.

        :param model: The model of the player.
        :param position: The initial position of the player.
        :param rot_x: The rotation around the X-axis.
        :param rot_y: The rotation around the Y-axis.
        :param rot_z: The rotation around the Z-axis.
        :param scale: The scale of the player.
        """
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)

    @classmethod
    def set_instance(cls, instance) -> None:
        """Sets the singleton instance of the Player class.

        :param instance: The instance of the Player.
        """
        cls.__instance = instance

    @classmethod
    def get_instance(cls):
        """Gets the singleton instance of the Player class.

        :return: The instance of the Player.
        """
        return cls.__instance

    @classmethod
    def get_run_speed(cls) -> float:
        """Gets the run speed of the player

        :return: The run speed
        """
        return cls.__RUN_SPEED

    @classmethod
    def get_turn_speed(cls) -> float:
        """Gets the turn speed of the player.

        :return: The turn speed
        """
        return cls.__TURN_SPEED

    @classmethod
    def get_gravity(cls) -> float:
        """Gets the gravity affecting the player.

        :return: The gravity value
        """
        return cls.__GRAVITY

    @classmethod
    def get_jump_power(cls) -> float:
        """Gets the jump power of the player

        :return: The jump power
        """
        return cls.__JUMP_POWER


class ThirdPersonPlayer(Player):
    """
    Player with a camera from the 3rd person view.
    """
    __current_upwards_speed: float = 0
    __is_in_air: bool = False
    __units_per_meter = 100

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        """Creates a third-person player object with the specified model and transformation parameters.

        :param model: The model of the player.
        :param position: The initial position of the player.
        :param rot_x: The rotation around the X-axis.
        :param rot_y: The rotation around the Y-axis.
        :param rot_z: The rotation around the Z-axis.
        :param scale: The scale of the player.
        """
        self.__current_z_speed = 0
        self.__current_x_speed = 0
        self.__current_turn_speed = 0
        self.__speed_vector = vec3()
        self.__collision_detection = Detection(vec3(1, 1, 1))
        self.__collision_recursion_depth = 0
        self.__player_under_control = True
        self.__music_source = None
        self.__bg_sfx_source = None
        self.__sfx_source = None
        self.__steps_sfx = None
        self.__load_audio()
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)
        Player.set_instance(self)

    def collide_and_slide(self, entities) -> vec3:
        """Handles collision detection and sliding for the player.

        :param entities: The entities to collide with.
        :return: The final position after collision handling.
        """
        self.__collision_detection.get_packet().r3_position = vec3(super().get_position())
        self.__collision_detection.get_packet().r3_velocity = vec3(self.__speed_vector)

        e_space_position = convert_to_ellipsoid_space(self.__collision_detection.get_packet().e_radius,
                                                      self.__collision_detection.get_packet().r3_position)
        e_space_velocity = convert_to_ellipsoid_space(self.__collision_detection.get_packet().e_radius,
                                                      self.__collision_detection.get_packet().r3_velocity)

        self.__collision_recursion_depth = 0
        final_position = self.collide_with_world(e_space_position, e_space_velocity, entities)
        final_position = convert_to_r3_space(self.__collision_detection.get_packet().e_radius, final_position)
        return final_position

    def collide_with_world(self, pos: vec3, velocity: vec3, entities) -> vec3:
        """Handles collision detection with the world and adjusts the player's position

        :param pos: The current position of the player.
        :param velocity: The current velocity of the player.
        :param entities: The entities to collide with
        :return: The new position after collision handling
        """
        # All hard-coded distances in this function are scaled to fit the setting above...
        unit_scale = self.__units_per_meter / 100
        very_close_distance = 0.005 * unit_scale

        # do we need to worry?
        if self.__collision_recursion_depth > 5:
            return pos

        # yes we do!
        self.__collision_detection.get_packet().velocity = velocity
        self.__collision_detection.get_packet().normalized_velocity = velocity.normalize()
        self.__collision_detection.get_packet().base_point = pos
        self.__collision_detection.get_packet().found_collision = False
        self.__collision_detection.get_packet().nearest_distance = 999

        for entity in entities:
            self.__collision_detection.detect_object(entity)
        if not self.__collision_detection.get_packet().found_collision:
            return pos + velocity

        destination_point = pos + velocity
        new_base_point = pos
        # only update if we are not already very close and if so we only move very close to intersection, not
        # to the exact spot.
        if self.__collision_detection.get_packet().nearest_distance >= very_close_distance:
            v = velocity
            v = v.normalize() * (self.__collision_detection.get_packet().nearest_distance - very_close_distance)
            new_base_point = self.__collision_detection.get_packet().base_point + v

            # Adjust polygon intersection point (so sliding plane will be unaffected by the fact that we
            # move slightly less than collision tells us)
            v = v.normalize()
            self.__collision_detection.get_packet().intersection_point -= very_close_distance * v

        slide_plane_origin = self.__collision_detection.get_packet().intersection_point
        slide_plane_normal = new_base_point - self.__collision_detection.get_packet().intersection_point
        slide_plane_normal = slide_plane_normal.normalize()
        sliding_plane = Plane(slide_plane_origin, slide_plane_normal)

        new_destination_point = destination_point - sliding_plane.signed_distance_to(destination_point) * slide_plane_normal
        # // Generate the slide vector, which will become our new velocity vector for the next iteration
        new_velocity_vector = new_destination_point - self.__collision_detection.get_packet().intersection_point

        if new_velocity_vector.length() < very_close_distance:
            return new_base_point

        self.__collision_recursion_depth += 1
        return self.collide_with_world(new_base_point, new_velocity_vector, entities)

    def move(self, collider_entities=None) -> None:
        """Moves the player based on input and collision detection.

        :param collider_entities: The entities to check for collisions.
        """
        if not self.__player_under_control:
            return

        self.__speed_vector = [0, 0, 0]
        self.__check_inputs()
        terrain = Terrain.get_existing_terrains().get((self.get_position()[0] // Terrain.get_size(),
                                                       self.get_position()[2] // Terrain.get_size()))
        distance_z = self.__current_z_speed * Time.get_delta_time()
        dx = distance_z * math.sin(math.radians(super().get_rot_y()))
        dz = distance_z * math.cos(math.radians(super().get_rot_y()))
        self.__speed_vector[0] += dx
        self.__speed_vector[2] += dz

        distance_x = self.__current_x_speed * Time.get_delta_time()
        dx = distance_x * math.cos(-math.radians(super().get_rot_y()))
        dz = distance_x * math.sin(-math.radians(super().get_rot_y()))
        self.__speed_vector[0] += dx
        self.__speed_vector[2] += dz

        self.__current_upwards_speed += self.get_gravity() * Time.get_delta_time()
        self.__speed_vector[1] = self.__current_upwards_speed * Time.get_delta_time()

        if collider_entities:
            super().set_position(self.collide_and_slide(collider_entities))
        else:
            super().set_position(vec3(super().get_position()) + vec3(self.__speed_vector))
        if terrain is not None:
            terrain_height = terrain.get_height_of_terrain(super().get_position()[0], super().get_position()[2])
        else:
            terrain_height = 0
        if super().get_position()[1] < terrain_height:
            self.__current_upwards_speed = 0
            self.__is_in_air = False
            super().get_position()[1] = terrain_height

        AudioMaster.set_listener_data(self.get_position(), self.get_speed_vector())
        self.__sfx_source.set_position(*self.get_position())
        self.__music_source.set_position(*self.get_position())
        self.__steps_sfx.set_position(*self.get_position())
        self.play_footsteps()

    def jump(self) -> None:
        """Makes the player jump if they are not already in the air."""
        if not self.__is_in_air:
            self.__current_upwards_speed = super().get_jump_power()
            self.__is_in_air = True

    def get_speed_vector(self) -> vec3:
        """Gets the current speed vector of the player.

        :return: The speed vector.
        """
        return self.__speed_vector

    def set_player_under_control(self, is_under_control: bool) -> None:
        """Sets whether the player is under control.

        :param is_under_control: True if the player is under control, False otherwise.
        """
        self.__player_under_control = is_under_control

    def __load_audio(self) -> None:
        """Loads the audio sources for the player."""
        self.__steps_sfx = Source()
        self.__steps_sfx.set_looping(True)
        self.__steps_sfx.play(AudioMaster.load_sound(f"{PATH}/res/audio/footsteps.wav"))
        self.__steps_sfx.set_volume(0.5)
        self.__steps_sfx.pause()
        self.__sfx_source = Source()
        self.__bg_sfx_source = Source()
        self.__bg_sfx_source.set_position(186, 5.18, 89)
        self.__bg_sfx_source.set_looping(True)
        self.__bg_sfx_source.play(AudioMaster.load_sound(f"{PATH}/res/audio/dinner_atmo.wav"))
        self.__bg_sfx_source.set_volume(0.2)
        self.__bg_sfx_source.pause()
        self.__music_source = Source()
        self.__music_source.set_looping(True)
        self.__music_source.play(AudioMaster.load_sound(f"{PATH}/res/audio/music_loop.wav"))
        self.__music_source.set_volume(0.1)
        self.__music_source.pause()

    def get_sfx_source(self) -> Source:
        """Gets the sound effects source.

        :return: The sound effects source.
        """
        return self.__sfx_source

    def get_bg_sfx_source(self) -> Source:
        """Gets the background sound effects source.

        :return: The background sound effects source.
        """
        return self.__bg_sfx_source

    def start_music(self) -> None:
        """Starts playing background music."""
        self.__bg_sfx_source.continue_playing()
        self.__music_source.continue_playing()

    def play_footsteps(self) -> None:
        """Plays the footstep sound effect based on the player's speed."""
        if math.sqrt(self.get_speed_vector()[0]**2 + self.get_speed_vector()[1]**2 + self.get_speed_vector()[2]**2) > 2:
            if not self.__steps_sfx.is_playing():
                self.__steps_sfx.continue_playing()
        else:
            self.__steps_sfx.pause()

    def __check_inputs(self) -> None:
        """Private function getting inputs from the input controller."""
        self.__current_x_speed = UniversalInput.get_x_axis_movement() * super().get_run_speed()
        self.__current_z_speed = UniversalInput.get_y_axis_movement() * super().get_run_speed()


class FirstPersonPlayer(ThirdPersonPlayer):
    """
    Player with a camera from the 1st person view.
    """
    __player_size = 4

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        """Creates a first-person player object with the specified model and transformation parameters.

        :param model: The model of the player.
        :param position: The initial position of the player.
        :param rot_x: The initial rotation around the X-axis.
        :param rot_y: The initial rotation around the Y-axis.
        :param rot_z: The initial rotation around the Z-axis.
        :param scale: The scale of the player.
        """
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)
        Player.set_instance(self)

    @classmethod
    def set_player_size(cls, size: float) -> None:
        """Sets the size of the player.

        :param size: The new size of the player.
        """
        cls.__player_size = size

    @classmethod
    def get_player_size(cls) -> float:
        """Gets the size of the player.

        :return: The size of the player.
        """
        return cls.__player_size
