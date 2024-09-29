from src.audio.audio_master import AudioMaster
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.cup_spawn import CupSpawn
from src.game_mechanics.food import Food
from src.game_mechanics.food_spawn import FoodSpawn
from src.game_mechanics.order import MasterOrder
from src.game_mechanics.ingredient import Ingredient
from src.game_mechanics.tea_bag_spawn import TeaBagSpawn
from src.game_ui.key_hints import KeyHints
from src.render_engine.input_controller import KeyboardInput, ControllerInput, UniversalInput, Binds
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS, CoffeeMachineOSLactoseFree
from src.game_mechanics.fridge_object import FridgeObject
from src.pycgtypes import vec3
from src.toolbox.path import PATH


class Carry:

    movable_entities = []
    LEFT = 0
    RIGHT = 1

    def __init__(self, terrain_raycaster, object_raycaster, coffee_machine, coffee_machine_lf, sfx_source):
        self.__camera = terrain_raycaster.get_camera()
        self.__terrain_picker = terrain_raycaster
        self.__object_picker = object_raycaster
        self.__sfx_source = sfx_source
        self.__is_carrying_right = False
        self.__carrying_object_right = None
        self.__is_carrying_left = False
        self.__carrying_object_left = None
        self.__coffee_machine = coffee_machine
        self.__coffee_machine_lf = coffee_machine_lf

        self.__forward_distance = 5
        self.__sideways_distance = 3.5

        self.__c_pressed = False
        self.__y_pressed = False

        self.__pick_up_audio = AudioMaster.load_sound(f"{PATH}/res/audio/grab.wav")
        self.__lay_down_audio = AudioMaster.load_sound(f"{PATH}/res/audio/put_down.wav")

    def update(self, can_pick_up: bool = True) -> None:
        relevant_entities = [_ for _ in self.movable_entities if
                             _ not in (self.__carrying_object_right, self.__carrying_object_left)]

        if self.__is_carrying_right:
            self.__move_right()
        if self.__is_carrying_left:
            self.__move_left()

        if self.__is_carrying_right and self.__is_carrying_left:
            KeyHints.set_text(f"Press {Binds.get_bind(Binds.L1)} + {Binds.get_bind(Binds.R1)} to interact with objects")

        if not can_pick_up:
            return

        if UniversalInput.get_r2():
            if self.__is_carrying_right:
                self.__lay_down(self.RIGHT, self.__carrying_object_right, relevant_entities)
            else:
                self.__pick_up(self.RIGHT, relevant_entities)

        if UniversalInput.get_l2():
            if self.__is_carrying_left:
                self.__lay_down(self.LEFT, self.__carrying_object_left, relevant_entities)
            else:
                self.__pick_up(self.LEFT, relevant_entities)

        if UniversalInput.get_r1() or self.__c_pressed:
            self.__c_pressed = True
            if UniversalInput.get_l1():
                self.__put_right_in_left()
                self.__c_pressed = False
                self.__y_pressed = False

        if UniversalInput.get_l1() or self.__y_pressed:
            self.__y_pressed = True
            if UniversalInput.get_r1() or self.__c_pressed:
                self.__put_left_in_right()
                self.__y_pressed = False
                self.__c_pressed = False

    def __pick_up(self, side, relevant_entities) -> None:
        entity = self.__object_picker.update(relevant_entities)
        if isinstance(entity, GameObject):
            if not entity.is_pickup_able():
                return
            if self.__pick_up_special_cases(entity, side):
                return
            if entity.get_parent():
                if entity is entity.get_parent().get_child_0():
                    entity.get_parent().remove_child_0()
                else:
                    entity.get_parent().remove_child_1()
                entity.set_offset([0, 0, 0])
        if entity is not None:
            self.__sfx_source.play(self.__pick_up_audio)
            if side:
                self.__is_carrying_right = True
                self.__carrying_object_right = entity
            else:
                self.__is_carrying_left = True
                self.__carrying_object_left = entity

    def __pick_up_special_cases(self, entity, side) -> int:
        name = entity.get_int_name()
        if name == "COFFEE" or name == "TEA" or name == "GLASS" or name == "MIXER_VESSEL":
            if not self.__pick_up_coffee(entity):
                return 1
            else:
                self.__sfx_source.play(self.__pick_up_audio)
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
            self.__sfx_source.play(self.__pick_up_audio)
            entity.get_attachment().set_lid_closed(False)
            return 0
        elif name == "MILK_FOAMER_CUP":
            if entity.get_attachment().get_is_brewing():
                return 1
            if not entity.get_attachment().get_lid_closed():
                if entity.get_attachment().get_cup_placed():
                    self.__sfx_source.play(self.__pick_up_audio)
                    entity.get_attachment().set_cup_placed(False)
                    return 0
        elif name == "MILK_FOAMER_VESSEL":
            if entity.get_attachment().get_is_brewing():
                return 1
            if entity.get_attachment().get_lid_closed():
                self.__sfx_source.play(self.__pick_up_audio)
                entity.get_attachment().set_lid_closed(False)
                self.set_carrying_object(side, entity.get_child_0())
            elif entity.get_attachment().get_cup_placed():
                self.__sfx_source.play(self.__pick_up_audio)
                entity.get_attachment().set_cup_placed(False)
                self.set_carrying_object(side, entity.get_child_1())
            return 1
        elif isinstance(entity.get_attachment(), FoodSpawn):
            self.__sfx_source.play(self.__pick_up_audio)
            self.set_carrying_object(side, entity.get_attachment().spawn())
            return 1
        elif isinstance(entity.get_attachment(), CupSpawn):
            self.__sfx_source.play(self.__pick_up_audio)
            self.set_carrying_object(side, entity.get_attachment().spawn())
            return 1
        elif isinstance(entity.get_attachment(), TeaBagSpawn):
            self.__sfx_source.play(self.__pick_up_audio)
            self.set_carrying_object(side, entity.get_attachment().spawn())
            return 1
        elif name == "DOOR":
            if entity.get_rot_z() == 90:
                entity.set_rot_z(0)
                entity.get_collider().set_position(entity.get_position())
            else:
                entity.set_rot_z(90)
                entity.get_collider().set_position([entity.get_position()[0],
                                                   entity.get_position()[1] - 1,
                                                   entity.get_position()[2]])
            return 1
        elif name == "TICKET":
            self.__sfx_source.play(self.__pick_up_audio)
            entity.get_attachment().remove_game_object_from_list(entity)
            return 0

    def __lay_down(self, side: int, carrying_entity, relevant_entities: list) -> None:
        relevant_entities = [_ for _ in relevant_entities if
                             _ not in self.__coffee_machine.get_attachment().get_coffee_list()]
        entity = self.__object_picker.update(relevant_entities)
        if isinstance(entity, GameObject):
            if self.__lay_down_special_cases(entity, side):
                return
            if isinstance(entity.get_attachment(), (CoffeeMachineOS, CoffeeMachineOSLactoseFree)):
                self.__lay_down_coffee(side, entity)
                self.remove_carrying_object(side)
                return

        # there isn't really ever a situation, where you want to put something below this height, mostly it's caused by
        # a faulty collision detection, so this is kind of a way to fight that
        min_height = 12.5
        if entity is not None:
            self.__sfx_source.play(self.__lay_down_audio)
            pos = self.__object_picker.get_current_object_point()
            pos[1] = max(min_height, pos[1])
            carrying_entity.set_position([pos[0], pos[1], pos[2]])
            self.remove_carrying_object(side)
        else:
            self.__terrain_picker.update()
            terrain = self.__terrain_picker.get_current_terrain_point()
            if terrain is not None:
                self.__sfx_source.play(self.__lay_down_audio)
                self.remove_carrying_object(side)
                terrain[1] = max(min_height, terrain[1])
                terrain = [terrain[0], terrain[1], terrain[2]]
                carrying_entity.set_position(terrain)

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
                        entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().get_content())
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
                    entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().get_content())
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
                    entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().get_content())
                    return 1
                elif isinstance(self.get_carrying_object(side).get_attachment(), Ingredient):
                    entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().get_content())
                    entity.get_attachment().set_texture(self.get_carrying_object(side).get_attachment().get_texture())
                    return 1
        elif name == "PLATE":
            if isinstance(self.get_carrying_object(side), GameObject):
                if self.get_carrying_object(side).get_int_name() == "FOOD":
                    offset = [0, 0.4, 0]
                    pos = [entity.get_position()[0] + offset[0],
                           entity.get_position()[1] + offset[1],
                           entity.get_position()[2] + offset[2]]
                    self.get_carrying_object(side).set_position(pos)
                    entity.set_child_0(self.get_carrying_object(side))
                    self.remove_carrying_object(side)
                    return 1
        if isinstance(entity.get_attachment(), CoffeeContainer):
            if self.get_carrying_object(side).get_int_name() == "MILK_FOAMER_CUP" or self.get_carrying_object(side).get_int_name() == "MIXER_VESSEL":
                if not self.get_carrying_object(side).get_attachment().get_fill_lvl():
                    return 1
                entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().remove_content())
                entity.get_attachment().set_level(self.get_carrying_object(side).get_attachment().get_fill_lvl(),
                                                  self.get_carrying_object(side).get_attachment().get_texture())
                self.get_carrying_object(side).get_attachment().empty()
                return 1
            elif isinstance(self.get_carrying_object(side).get_attachment(), FridgeObject):
                entity.get_attachment().append_content(self.get_carrying_object(side).get_attachment().get_content())
                entity.get_attachment().fill(self.get_carrying_object(side).get_attachment().get_texture())
                return 1
            elif entity.get_attachment().get_container_type() == CoffeeContainer.BIG_GLASS:
                if isinstance(self.get_carrying_object(side), GameObject) and isinstance(self.get_carrying_object(side).get_attachment(), Food):
                    food = self.get_carrying_object(side).get_attachment().get_food()
                    if food == "Ice" or food == "Lemon":
                        if not entity.get_child_0():
                            self.get_carrying_object(side).set_position([entity.get_position()[0],
                                                                         entity.get_position()[1] + 1,
                                                                         entity.get_position()[2]])
                            entity.set_child_0(self.get_carrying_object(side))
                        elif not entity.get_child_1():
                            self.get_carrying_object(side).set_position([entity.get_position()[0],
                                                                         entity.get_position()[1] + 1,
                                                                         entity.get_position()[2]])
                            entity.set_child_1(self.get_carrying_object(side))
                        else:
                            return 0
                        entity.get_attachment().append_content(food)
                        self.get_carrying_object(side).set_pickup_able(False)
                        self.movable_entities.remove(self.remove_carrying_object(side))
                        return 1
            elif entity.get_attachment().get_container_type() == CoffeeContainer.TEA_POT:
                if isinstance(self.get_carrying_object(side), GameObject) and self.get_carrying_object(side).get_int_name() == "TEA_BAG":
                    entity.get_attachment().append_content(self.get_carrying_object(side).get_ext_name())
                    self.get_carrying_object(side).set_position([entity.get_position()[0] + 0.4,
                                                                 entity.get_position()[1] + 1.1,
                                                                 entity.get_position()[2]])
                    self.get_carrying_object(side).set_pickup_able(False)
                    entity.set_child_1(self.get_carrying_object(side))
                    self.remove_carrying_object(side)

        elif name == "FINISHED":
            if isinstance(entity.get_attachment(), MasterOrder):
                if isinstance(self.get_carrying_object(side).get_attachment(), CoffeeContainer):
                    entity.get_attachment().place(self.get_carrying_object(side))
                    self.get_carrying_object(side).set_pickup_able(False)
                    self.remove_carrying_object(side)
                    return 1
                if self.get_carrying_object(side).get_int_name() == "PLATE":
                    if isinstance(self.get_carrying_object(side).get_child_0(), GameObject) and isinstance(self.get_carrying_object(side).get_child_0().get_attachment(), Food):
                        entity.get_attachment().place(self.get_carrying_object(side).get_child_0())
                        self.get_carrying_object(side).set_pickup_able(False)
                        self.get_carrying_object(side).get_child_0().set_pickup_able(False)
                        self.remove_carrying_object(side)
                        return 1

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

    def __pick_up_coffee(self, entity) -> bool:
        if entity in self.__coffee_machine.get_attachment().get_coffee_list():
            if self.__coffee_machine.get_attachment().is_brewing_coffee() and (entity.get_int_name() == "COFFEE" or entity.get_int_name() == "GLASS"):
                return False
            elif self.__coffee_machine.get_attachment().is_brewing_tea() and entity.get_int_name() == "TEA":
                return False
            self.__coffee_machine.get_attachment().remove_coffee(self.__coffee_machine.get_attachment().get_coffee_list().index(entity))
        elif entity in self.__coffee_machine_lf.get_attachment().get_coffee_list():
            if self.__coffee_machine_lf.get_attachment().is_brewing_coffee() and (entity.get_int_name() == "COFFEE" or entity.get_int_name() == "GLASS"):
                return False
            elif self.__coffee_machine_lf.get_attachment().is_brewing_tea() and entity.get_int_name() == "TEA":
                return False
            self.__coffee_machine_lf.get_attachment().remove_coffee(self.__coffee_machine_lf.get_attachment().get_coffee_list().index(entity))
        return True

    def __lay_down_coffee(self, side, coffee_machine):
        if side:
            if not isinstance(self.__carrying_object_right, GameObject):
                return
            if self.__carrying_object_right.get_int_name() == "COFFEE" or self.__carrying_object_right.get_int_name() == "GLASS"\
                    or self.__carrying_object_right.get_int_name() == "MIXER_VESSEL":
                if coffee_machine.get_attachment().get_coffee(1) is None:
                    coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_right)
                elif coffee_machine.get_attachment().get_coffee(2) is None:
                    coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_right)
            if self.__carrying_object_right.get_int_name() == "TEA":
                if coffee_machine.get_attachment().get_coffee(0) is None:
                    coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_right)
        else:
            if not isinstance(self.__carrying_object_left, GameObject):
                return
            if self.__carrying_object_left.get_int_name() == "COFFEE" or self.__carrying_object_left.get_int_name() == "GLASS" \
                    or self.__carrying_object_left.get_int_name() == "MIXER_VESSEL":
                if coffee_machine.get_attachment().get_coffee(1) is None:
                    coffee_machine.get_attachment().set_coffee(1, self.__carrying_object_left)
                elif coffee_machine.get_attachment().get_coffee(2) is None:
                    coffee_machine.get_attachment().set_coffee(2, self.__carrying_object_left)
            if self.__carrying_object_left.get_int_name() == "TEA":
                if coffee_machine.get_attachment().get_coffee(0) is None:
                    coffee_machine.get_attachment().set_coffee(0, self.__carrying_object_left)

    def __put_left_in_right(self):
        """Object in the left hand 'collides' with the object in the right hand."""
        if self.get_carrying_object(self.LEFT) and self.get_carrying_object(self.RIGHT):
            self.__lay_down_special_cases(self.get_carrying_object(self.RIGHT), self.LEFT)

    def __put_right_in_left(self):
        """Object in the right hand 'collides' with the object in the left hand."""
        if self.get_carrying_object(self.LEFT) and self.get_carrying_object(self.RIGHT):
            self.__lay_down_special_cases(self.get_carrying_object(self.LEFT), self.RIGHT)
