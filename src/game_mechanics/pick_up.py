from src.render_engine.input_controller import KeyboardInput, ControllerInput
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS
from src.game_mechanics.fridge_object import FridgeObject
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
        self.__sideways_distance = 3.5

    def update(self, can_pick_up: bool = True) -> None:
        relevant_entities = [_ for _ in self.movable_entities if
                             _ not in (self.__carrying_object_right, self.__carrying_object_left)]
        if self.__is_carrying_right:
            self.__move_right()
        if self.__is_carrying_left:
            self.__move_left()

        if not can_pick_up:
            return

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
            if self.__pick_up_special_cases(entity, side):
                return
            if not entity.is_pickup_able():
                return
        if entity is not None:
            if side:
                self.__is_carrying_right = True
                self.__carrying_object_right = entity
            else:
                self.__is_carrying_left = True
                self.__carrying_object_left = entity

    def __pick_up_special_cases(self, entity, side) -> int:
        name = entity.get_int_name()
        if name == "COFFEE" or name == "TEA" or name == "GLASS":
            self.__pick_up_coffee(entity)
            return 0
        elif name == "TOP_DRAWER":
            entity.get_attachment().move_top_drawer()
            return 1
        elif name == "BOTTOM_DRAWER":
            entity.get_attachment().move_bottom_drawer()
            return 1
        elif name == "MILK_FOAMER_LID":
            if entity.get_attachment().get_is_brewing():
                return 1
            entity.get_attachment().set_lid_closed(False)
            return 0
        elif name == "MILK_FOAMER_CUP":
            if entity.get_attachment().get_is_brewing():
                return 1
            if not entity.get_attachment().get_lid_closed():
                if entity.get_attachment().get_cup_placed():
                    entity.get_attachment().set_cup_placed(False)
                    return 0
        elif name == "MILK_FOAMER_VESSEL":
            if entity.get_attachment().get_is_brewing():
                return 1
            if entity.get_attachment().get_lid_closed():
                entity.get_attachment().set_lid_closed(False)
                self.set_carrying_object(side, entity.get_child_0())
            elif entity.get_attachment().get_cup_placed():
                entity.get_attachment().set_cup_placed(False)
                self.set_carrying_object(side, entity.get_child_1())
            return 1

    def __lay_down_special_cases(self, entity, side):
        name = entity.get_int_name()
        if name == "MILK_FOAMER_VESSEL":
            if isinstance(self.get_carrying_object(side), GameObject):
                if self.get_carrying_object(side).get_int_name() == "MILK_FOAMER_LID":
                    entity.get_attachment().set_lid_closed(True)
                    lid = self.remove_carrying_object(side)
                    lid.set_position(entity.get_position())
                    return 1
                elif self.get_carrying_object(side).get_int_name() == "MILK_FOAMER_CUP":
                    entity.get_attachment().set_cup_placed(True)
                    cup = self.remove_carrying_object(side)
                    cup.set_position(entity.get_position())
                    return 1
                elif self.get_carrying_object(side).get_int_name() == "MILK":
                    if entity.get_attachment().get_cup_placed():
                        entity.get_attachment().fill(self.get_carrying_object(side).get_attachment().get_texture())
                        return 1
        elif name == "MILK_FOAMER_CUP":
            if isinstance(self.get_carrying_object(side), GameObject):
                if self.get_carrying_object(side).get_int_name() == "MILK_FOAMER_LID":
                    entity.get_attachment().set_lid_closed(True)
                    lid = self.remove_carrying_object(side)
                    lid.set_position(entity.get_position())
                    return 1
                elif self.get_carrying_object(side).get_int_name() == "MILK":
                    entity.get_attachment().fill(self.get_carrying_object(side).get_attachment().get_texture())
                    return 1
        elif name == "TAP":
            if isinstance(self.get_carrying_object(side), GameObject):
                if self.get_carrying_object(side).get_int_name() == "GLASS":
                    entity.get_attachment().start_fill(self.get_carrying_object(side))
                    self.remove_carrying_object(side)
                    return 1
        elif name == "MIXER":
            if self.get_carrying_object(side).get_int_name() == "MIXER_VESSEL":
                entity.get_attachment().place_vessel(self.get_carrying_object(side))
                entity.get_attachment().start_mix(self.get_carrying_object(side))
                self.remove_carrying_object(side)
                return 1
        elif name == "MIXER_VESSEL":
            if isinstance(self.get_carrying_object(side), GameObject):
                if isinstance(self.get_carrying_object(side).get_attachment(), FridgeObject):
                    entity.get_attachment().fill(self.get_carrying_object(side).get_attachment().get_texture())
                    return 1

    def __lay_down(self, side: int, carrying_entity, relevant_entities: list) -> None:
        relevant_entities = [_ for _ in relevant_entities if
                             _ not in self.__coffee_machine.get_attachment().get_coffee_list()]
        entity = self.__object_picker.update(relevant_entities)
        if isinstance(entity, GameObject):
            if self.__lay_down_special_cases(entity, side):
                return
            if entity.get_int_name() == CoffeeMachineOS.get_name():
                self.__lay_down_coffee(side)
                self.remove_carrying_object(side)
                return
        if entity is not None:
            carrying_entity.set_position(self.__object_picker.get_current_object_point())
            self.remove_carrying_object(side)
        else:
            self.__terrain_picker.update()
            terrain = self.__terrain_picker.get_current_terrain_point()
            if terrain is not None:
                self.remove_carrying_object(side)
                carrying_entity.set_position(terrain)

    def set_carrying_object(self, side: int, entity) -> None:
        if side:
            if not self.__is_carrying_right:
                self.__is_carrying_right = True
                self.__carrying_object_right = entity
        else:
            if not self.__is_carrying_left:
                self.__is_carrying_left = True
                self.__carrying_object_left = entity

    def remove_carrying_object(self, side: int) -> any:
        if side:
            self.__is_carrying_right = False
            obj = self.__carrying_object_right
            self.__carrying_object_right = None
        else:
            self.__is_carrying_left = False
            obj = self.__carrying_object_left
            self.__carrying_object_left = None
        return obj

    def get_carrying_object(self, side: int) -> any:
        if side:
            return self.__carrying_object_right
        else:
            return self.__carrying_object_left

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
            if self.__carrying_object_right.get_int_name() == "COFFEE" or self.__carrying_object_right.get_int_name() == "GLASS":
                if self.__coffee_machine.get_attachment().get_coffee(1) is None:
                    self.__coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_right)
                elif self.__coffee_machine.get_attachment().get_coffee(2) is None:
                    self.__coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_right)
            if self.__carrying_object_right.get_int_name() == "TEA":
                if self.__coffee_machine.get_attachment().get_coffee(0) is None:
                    self.__coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_right)
        else:
            if not isinstance(self.__carrying_object_left, GameObject):
                return
            if self.__carrying_object_left.get_int_name() == "COFFEE" or self.__carrying_object_left.get_int_name() == "GLASS":
                if self.__coffee_machine.get_attachment().get_coffee(1) is None:
                    self.__coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_left)
                elif self.__coffee_machine.get_attachment().get_coffee(2) is None:
                    self.__coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_left)
            if self.__carrying_object_left.get_int_name() == "TEA":
                if self.__coffee_machine.get_attachment().get_coffee(0) is None:
                    self.__coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_left)
