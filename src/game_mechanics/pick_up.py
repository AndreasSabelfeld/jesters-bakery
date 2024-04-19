from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS
from src.pycgtypes import vec3


class Carry:

    movable_entities = []
    LEFT = 0
    RIGHT = 1

    def __init__(self, terrain_raycaster, object_raycaster, coffee_machine=None):
        self.__camera = terrain_raycaster.get_camera()
        self.__terrain_picker = terrain_raycaster
        self.__object_picker = object_raycaster
        self.__is_carrying_right = False
        self.__carrying_object_right = None
        self.__is_carrying_left = False
        self.__carrying_object_left = None
        self.__coffee_machine = coffee_machine

        self.__forward_distance = 3
        self.__sideways_distance = 2

    def update(self) -> None:
        relevant_entities = [_ for _ in self.movable_entities if
                             _ not in (self.__carrying_object_right, self.__carrying_object_left)]
        if self.__is_carrying_right:
            self.__move_right()
        if self.__is_carrying_left:
            self.__move_left()

        if KeyboardInput.on_key_down(b'e'):
            if self.__is_carrying_right:
                self.__lay_down(self.RIGHT, self.__carrying_object_right, relevant_entities)
            else:
                self.__pick_up(self.RIGHT, relevant_entities)

        if KeyboardInput.on_key_down(b'q'):
            if self.__is_carrying_left:
                self.__lay_down(self.LEFT, self.__carrying_object_left, relevant_entities)
            else:
                self.__pick_up(self.LEFT, relevant_entities)

    def __pick_up(self, side, relevant_entities) -> None:
        entity = self.__object_picker.update(relevant_entities)
        if isinstance(entity, GameObject):
            if not entity.is_pickup_able():
                return
            if entity.get_name() == "COFFEE" or entity.get_name() == "TEA":
                self.__pick_up_coffee(entity)
        if entity is not None:
            if side:
                self.__is_carrying_right = True
                self.__carrying_object_right = entity
            else:
                self.__is_carrying_left = True
                self.__carrying_object_left = entity

    def __lay_down(self, side: int, carrying_entity, relevant_entities: list) -> None:
        relevant_entities = [_ for _ in relevant_entities if
                             _ not in self.__coffee_machine.get_attachment().get_coffee_list()]
        entity = self.__object_picker.update(relevant_entities)
        if isinstance(entity, GameObject):
            if entity.get_name() == CoffeeMachineOS.get_name():
                self.__lay_down_coffee(side)
                self.__remove_carrying_object(side)
                return
        if entity is not None:
            carrying_entity.set_position(self.__object_picker.get_current_object_point())
            self.__remove_carrying_object(side)
        else:
            self.__terrain_picker.update()
            terrain = self.__terrain_picker.get_current_terrain_point()
            if terrain is not None:
                self.__remove_carrying_object(side)
                carrying_entity.set_position(terrain)

    def __remove_carrying_object(self, side: int) -> None:
        if side:
            self.__is_carrying_right = False
            self.__carrying_object_right = None
        else:
            self.__is_carrying_left = False
            self.__carrying_object_left = None

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

    def __pick_up_coffee(self, entity):
        if entity in self.__coffee_machine.get_attachment().get_coffee_list():
            self.__coffee_machine.get_attachment().remove_coffee(self.__coffee_machine.get_attachment().get_coffee_list().index(entity))

    def __lay_down_coffee(self, side):
        if side:
            if not isinstance(self.__carrying_object_right, GameObject):
                return
            if self.__carrying_object_right.get_name() == "COFFEE":
                if self.__coffee_machine.get_attachment().get_coffee(1) is None:
                    self.__coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_right)
                elif self.__coffee_machine.get_attachment().get_coffee(2) is None:
                    self.__coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_right)
            if self.__carrying_object_right.get_name() == "TEA":
                if self.__coffee_machine.get_attachment().get_coffee(0) is None:
                    self.__coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_right)
        else:
            if not isinstance(self.__carrying_object_left, GameObject):
                return
            if self.__carrying_object_left.get_name() == "COFFEE":
                if self.__coffee_machine.get_attachment().get_coffee(1) is None:
                    self.__coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_left)
                elif self.__coffee_machine.get_attachment().get_coffee(2) is None:
                    self.__coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_left)
            if self.__carrying_object_left.get_name() == "TEA":
                if self.__coffee_machine.get_attachment().get_coffee(0) is None:
                    self.__coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_left)
