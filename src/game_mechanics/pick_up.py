from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.pycgtypes import vec3
import multiprocessing


class Carry:

    movable_entities = []

    def __init__(self, terrain_raycaster, object_raycaster):
        self.__camera = terrain_raycaster.get_camera()
        self.__terrain_picker = terrain_raycaster
        self.__object_picker = object_raycaster
        self.__is_carrying_right = False
        self.__carrying_object_right = None
        self.__is_carrying_left = False
        self.__carrying_object_left = None

        self.__forward_distance = 3
        self.__sideways_distance = 2

        self.__right_cooldown = False
        self.__left_cooldown = False

    def update(self) -> None:
        keys_held = KeyboardInput.get_keys_held()
        relevant_entities = [_ for _ in self.movable_entities if
                             _ not in (self.__carrying_object_right, self.__carrying_object_left)]
        if self.__is_carrying_right:
            self.__move_right()
        if self.__is_carrying_left:
            self.__move_left()

        # giant if-else-mess incoming
        if keys_held.get(b'e'):
            if not self.__right_cooldown:
                self.__right_cooldown = True
                if self.__is_carrying_right:
                    # copy the list and remove the carrying object to prevent collision detection with itself
                    entity = self.__object_picker.update(relevant_entities)
                    if entity is not None:
                        self.__is_carrying_right = False
                        self.__carrying_object_right.set_position(self.__object_picker.get_current_object_point())
                        self.__carrying_object_right = None
                    else:
                        self.__terrain_picker.update()
                        terrain = self.__terrain_picker.get_current_terrain_point()
                        if terrain is not None:
                            self.__is_carrying_right = False
                            self.__carrying_object_right.set_position(terrain)
                            self.__carrying_object_right = None
                else:
                    entity = self.__object_picker.update(relevant_entities)
                    if entity is not None:
                        self.__is_carrying_right = True
                        self.__carrying_object_right = entity
        else:
            self.__right_cooldown = False

        if keys_held.get(b'q'):
            if not self.__left_cooldown:
                self.__left_cooldown = True
                if self.__is_carrying_left:
                    # copy the list and remove the carrying object to prevent collision detection with itself
                    entity = self.__object_picker.update(relevant_entities)
                    if entity is not None:
                        self.__is_carrying_left = False
                        self.__carrying_object_left.set_position(self.__object_picker.get_current_object_point())
                        self.__carrying_object_left = None
                    else:
                        self.__terrain_picker.update()
                        terrain = self.__terrain_picker.get_current_terrain_point()
                        if terrain is not None:
                            self.__is_carrying_left = False
                            self.__carrying_object_left.set_position(terrain)
                            self.__carrying_object_left = None
                else:
                    entity = self.__object_picker.update(relevant_entities)
                    if entity is not None:
                        self.__is_carrying_left = True
                        self.__carrying_object_left = entity
        else:
            self.__left_cooldown = False

    def __move_right(self):
        self.__terrain_picker.update()
        object_pos_right = vec3(self.__camera.get_position()) + vec3(self.__terrain_picker.get_current_ray()) * self.__forward_distance
        object_pos_right += vec3(self.__terrain_picker.get_current_ray()).normalize().cross(vec3(0, 1, 0)) * self.__sideways_distance
        self.__carrying_object_right.set_position(list(object_pos_right))
        self.__carrying_object_right.set_rot_x(self.__camera.get_player().get_rot_x())
        self.__carrying_object_right.set_rot_y(self.__camera.get_player().get_rot_y())
        self.__carrying_object_right.set_rot_z(self.__camera.get_player().get_rot_z())

    def __move_left(self):
        self.__terrain_picker.update()
        object_pos_left = vec3(self.__camera.get_position()) + vec3(self.__terrain_picker.get_current_ray()) * self.__forward_distance
        object_pos_left += vec3(self.__terrain_picker.get_current_ray()).normalize().cross(vec3(0, 1, 0)) * (-self.__sideways_distance)
        self.__carrying_object_left.set_position(list(object_pos_left))
        self.__carrying_object_left.set_rot_x(self.__camera.get_player().get_rot_x())
        self.__carrying_object_left.set_rot_y(self.__camera.get_player().get_rot_y())
        self.__carrying_object_left.set_rot_z(self.__camera.get_player().get_rot_z())
