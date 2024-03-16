from .entity import Entity
from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.render_engine.time import Time
from src.terrain.terrain import Terrain
from src.pycgtypes import vec3

from src.collision.detection import Detection
from src.collision.plane import Plane
from src.collision.utility import convert_to_ellipsoid_space, convert_to_r3_space

import math


class Player(Entity):
    """
    Base player class holding the speed, gravity and jump power of the player. Inherits from the Entity class.
    """
    __instance = None

    __RUN_SPEED = 20
    __TURN_SPEED = 160
    __GRAVITY = -50
    __JUMP_POWER = 30

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)

    @classmethod
    def set_instance(cls, instance):
        cls.__instance = instance

    @classmethod
    def get_instance(cls):
        return cls.__instance

    @classmethod
    def get_instance_type(cls):
        return type(cls.__instance)

    @classmethod
    def get_run_speed(cls):
        return cls.__RUN_SPEED

    @classmethod
    def get_turn_speed(cls):
        return cls.__TURN_SPEED

    @classmethod
    def get_gravity(cls):
        return cls.__GRAVITY

    @classmethod
    def get_jump_power(cls):
        return cls.__JUMP_POWER


class ThirdPersonPlayer(Player):
    """
    Player with a camera from the 3rd person view.
    """
    __current_upwards_speed: float = 0
    __is_in_air: bool = False
    __units_per_meter = 100

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        self.__current_z_speed = 0
        self.__current_x_speed = 0
        self.__current_turn_speed = 0
        self.__speed_vector = vec3()
        self.__collision_detection = Detection(vec3(1, 1, 1))
        self.__collision_recursion_depth = 0
        # self.__controller = ControllerInput(False)
        # self.__controller.set_sensitivity(7)
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)
        Player.set_instance(self)

    def collide_and_slide(self, entities):
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

    def collide_with_world(self, pos: vec3, velocity: vec3, entities):
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

    def move(self, collider_entities=None):
        self.__speed_vector = [0, 0, 0]
        self.__check_inputs()
        # super().increase_rotation(0, self.__current_turn_speed * Time.get_delta_time(), 0)
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

    def jump(self):
        if not self.__is_in_air:
            self.__current_upwards_speed = super().get_jump_power()
            self.__is_in_air = True

    def get_speed_vector(self) -> vec3:
        return self.__speed_vector

    def __check_inputs(self):
        """Private function getting inputs from the input controller"""
        self.__current_z_speed = 0
        self.__current_x_speed = 0
        self.__current_turn_speed = 0
        if ControllerInput.is_using_controller:
            if abs(ControllerInput.LeftJoystickY) > ControllerInput.get_dead_zone():
                self.__current_z_speed = -ControllerInput.LeftJoystickY * super().get_run_speed()
            if abs(ControllerInput.LeftJoystickX) > self.__controller.get_dead_zone():
                self.__current_x_speed = ControllerInput.LeftJoystickX * super().get_run_speed()
            if ControllerInput.A_cross:
                self.jump()
        else:
            keys_held = KeyboardInput.get_keys_held()
            if keys_held.get(b's'):
                self.__current_z_speed = super().get_run_speed()
            if keys_held.get(b'w'):
                self.__current_z_speed = -super().get_run_speed()
            if keys_held.get(b'd'):
                # self.__current_turn_speed = -super().get_turn_speed()
                self.__current_x_speed = super().get_run_speed()
            if keys_held.get(b'a'):
                # self.__current_turn_speed = super().get_turn_speed()
                self.__current_x_speed = -super().get_run_speed()
            if keys_held.get(b' '):
                self.jump()


class FirstPersonPlayer(ThirdPersonPlayer):
    """
    Player with a camera from the 1st person view.
    """
    __player_size = 4

    def __init__(self, model, position: list[float], rot_x: float, rot_y: float, rot_z: float, scale: float):
        super().__init__(model, position, rot_x, rot_y, rot_z, scale)
        Player.set_instance(self)

    @classmethod
    def set_player_size(cls, size: float):
        cls.__player_size = size

    @classmethod
    def get_player_size(cls):
        return cls.__player_size
