from src.game_mechanics.fridge_object import FridgeObject
from src.game_mechanics.pick_up import Carry
from src.guis.gui_texture import GuiTexture
from src.pycgtypes import vec3, mat3
from src.game_mechanics.game_object import GameObject
from src.render_engine.display_manager import DisplayManager
from src.render_engine.input_controller import KeyboardInput


class Fridge:

    __TOP_DRAWER = 1
    __BOTTOM_DRAWER = 2

    def __init__(self, top_drawer: GameObject, bottom_drawer: GameObject, object_picker, loader, gui_renderer):
        self.__top_drawer = top_drawer
        self.__top_drawer_is_open = False
        self.__top_drawer_inventory = [[None] * 4 for _ in range(5)]
        self.__bottom_drawer = bottom_drawer
        self.__bottom_drawer_is_open = False
        self.__bottom_drawer_inventory = [[None] * 4 for _ in range(5)]
        self.__opening_offset = vec3(0, 0, 1) * 6.5

        self.__interaction_key = b'f'
        self.__is_interacting = 0
        self.__original_camera_pos = None
        self.__original_camera_angles = None

        self.__object_picker = object_picker
        self.__gui_renderer = gui_renderer
        self.__icon_size_x = 100 * (1 / DisplayManager.get_width())
        self.__icon_size_y = 100 * (1 / DisplayManager.get_height())

        self.__selected_texture = GuiTexture(loader.load_texture("selected_test"), [0, 0], [self.__icon_size_x, self.__icon_size_y])
        self.__selected_pos = [0, 0]

    def update(self, pick_up: Carry):
        if self.__is_interacting:
            self.__gui_renderer.render([self.__selected_texture])
            self.__move_cursor()
            self.place(pick_up)

    def move_top_drawer(self):
        if self.__top_drawer_is_open:
            self.__top_drawer.set_position(vec3(self.__top_drawer.get_position()) - self.__opening_offset)
            [x.increase_position(0, 0, -self.__opening_offset.z) for xs in self.__top_drawer_inventory for x in xs if x is not None]
            self.__top_drawer_is_open = False
        else:
            self.__top_drawer.set_position(vec3(self.__top_drawer.get_position()) + self.__opening_offset)
            [x.increase_position(0, 0, self.__opening_offset.z) for xs in self.__top_drawer_inventory for x in xs if x is not None]
            self.__top_drawer_is_open = True

    def move_bottom_drawer(self):
        if self.__bottom_drawer_is_open:
            self.__bottom_drawer.set_position(vec3(self.__bottom_drawer.get_position()) - self.__opening_offset)
            [x.increase_position(0, 0, -self.__opening_offset.z) for xs in self.__bottom_drawer_inventory for x in xs if x is not None]
            self.__bottom_drawer_is_open = False
        else:
            self.__bottom_drawer.set_position(vec3(self.__bottom_drawer.get_position()) + self.__opening_offset)
            [x.increase_position(0, 0, self.__opening_offset.z) for xs in self.__bottom_drawer_inventory for x in xs if x is not None]
            self.__bottom_drawer_is_open = True

    def interact(self, player, camera, listener) -> None:
        if listener.on_key_down(self.__interaction_key):
            collision = self.__object_picker.update([self.__top_drawer.get_collider(), self.__bottom_drawer.get_collider()])
            if self.__is_interacting:
                self.__is_interacting = 0
                player.set_player_under_control(True)
                self.__move_camera_to_original_pos(camera)
            elif collision in [self.__top_drawer.get_collider(), self.__bottom_drawer.get_collider()]:
                if collision == self.__top_drawer.get_collider():
                    self.__is_interacting = 1
                else:
                    self.__is_interacting = 2
                player.set_player_under_control(False)
                self.__move_on_top_drawer(camera, collision)

    def get_is_interacting(self) -> bool:
        return bool(self.__is_interacting)

    def place(self, hands):
        if KeyboardInput.on_key_down(b'e'):
            entity = hands.remove_carrying_object(Carry.RIGHT)
            if not entity:
                self.take(Carry.RIGHT, hands)
                return
            if self.__is_interacting == self.__TOP_DRAWER:
                self.__place_in_top_drawer(entity)
            else:
                self.__place_in_bottom_drawer(entity)
            hands.movable_entities.remove(entity)
        elif KeyboardInput.on_key_down(b'q'):
            entity = hands.remove_carrying_object(Carry.LEFT)
            if not entity:
                self.take(Carry.LEFT, hands)
                return
            if self.__is_interacting == self.__TOP_DRAWER:
                self.__place_in_top_drawer(entity)
            else:
                self.__place_in_bottom_drawer(entity)
            hands.movable_entities.remove(entity)

    def take(self, side: int, hands: Carry):
        if self.__is_interacting == self.__TOP_DRAWER:
            entity = self.__top_drawer_inventory[self.__selected_pos[1]][self.__selected_pos[0]]
            if not entity:
                return
            hands.movable_entities.append(entity)
            hands.add_carrying_object(side, self.__top_drawer_inventory[self.__selected_pos[1]][self.__selected_pos[0]])
            self.__sort_out_inventory(entity, self.__top_drawer_inventory)
        else:
            entity = self.__bottom_drawer_inventory[self.__selected_pos[1]][self.__selected_pos[0]]
            if not entity:
                return
            hands.movable_entities.append(entity)
            hands.add_carrying_object(side, self.__bottom_drawer_inventory[self.__selected_pos[1]][self.__selected_pos[0]])
            self.__sort_out_inventory(entity, self.__bottom_drawer_inventory)

    def __place_in_top_drawer(self, entity) -> None:
        x_tile_size = 1.16
        z_tile_size = 1.21
        offset = [-2.4 + x_tile_size / 2, 3.66, -1.45 + z_tile_size / 2]

        x_pos = offset[0] + self.__selected_pos[0] * x_tile_size + self.__top_drawer.get_position()[0]
        y_pos = offset[1] + self.__top_drawer.get_position()[1]
        z_pos = offset[2] + self.__selected_pos[1] * z_tile_size + self.__top_drawer.get_position()[2]

        self.__sort_in_inventory(entity, self.__top_drawer_inventory)
        entity.set_position([x_pos, y_pos, z_pos])

    def __place_in_bottom_drawer(self, entity) -> None:
        x_tile_size = 1.16
        z_tile_size = 1.21
        offset = [-2.4 + x_tile_size / 2, 0.46, -1.45 + z_tile_size / 2]

        x_pos = offset[0] + self.__selected_pos[0] * x_tile_size + self.__bottom_drawer.get_position()[0]
        y_pos = offset[1]                                        + self.__bottom_drawer.get_position()[1]
        z_pos = offset[2] + self.__selected_pos[1] * z_tile_size + self.__bottom_drawer.get_position()[2]

        self.__sort_in_inventory(entity, self.__bottom_drawer_inventory)
        entity.set_position([x_pos, y_pos, z_pos])

    def __sort_in_inventory(self, entity, inventory):
        if isinstance(entity, GameObject):
            if isinstance(entity.get_attachment(), FridgeObject):
                for i in range(entity.get_attachment().get_size()[1]):
                    for j in range(entity.get_attachment().get_size()[0]):
                        inventory[self.__selected_pos[1] + i][self.__selected_pos[0] + j] = entity

        inventory[self.__selected_pos[1]][self.__selected_pos[0]] = entity

    def __sort_out_inventory(self, entity, inventory):
        if isinstance(entity, GameObject):
            if isinstance(entity.get_attachment(), FridgeObject):
                self.__nestrepl(inventory, entity, None)

        inventory[self.__selected_pos[1]][self.__selected_pos[0]] = None

    def __move_on_top_drawer(self, camera, drawer) -> None:
        self.__original_camera_pos = camera.get_position()
        self.__original_camera_angles = [camera.get_yaw(), camera.get_pitch(), camera.get_roll()]

        if drawer == self.__top_drawer.get_collider():
            offset = vec3(0, 6.85, 1) * drawer.get_scale()
        else:
            offset = vec3(0, 5, 1) * drawer.get_scale()
        rot_mat = mat3().rotation(drawer.get_rot_y(), vec3(0, 1, 0))
        offset = rot_mat * offset

        position = vec3(drawer.get_position()) + offset

        camera.set_position(position)
        camera.set_yaw(0)
        camera.set_pitch(90)
        camera.set_roll(0)

    def __move_camera_to_original_pos(self, camera) -> None:
        camera.set_yaw(self.__original_camera_angles[0])
        camera.set_pitch(self.__original_camera_angles[1])
        camera.set_roll(self.__original_camera_angles[2])
        camera.set_position(self.__original_camera_pos)

    def __move_cursor(self):
        if KeyboardInput.on_key_down(b'w'):
            if self.__selected_pos[1] > 0:
                self.__selected_pos[1] -= 1
        if KeyboardInput.on_key_down(b's'):
            if self.__selected_pos[1] < 4:
                self.__selected_pos[1] += 1
        if KeyboardInput.on_key_down(b'a'):
            if self.__selected_pos[0] > 0:
                self.__selected_pos[0] -= 1
        if KeyboardInput.on_key_down(b'd'):
            if self.__selected_pos[0] < 3:
                self.__selected_pos[0] += 1
        self.__move_selected_texture()

    def __move_selected_texture(self):
        x_tile_size = 0.184
        y_tile_size = 0.334

        x_offset = -0.275
        y_offset = 0.695

        x_pos = x_offset + x_tile_size * self.__selected_pos[0]
        y_pos = y_offset - y_tile_size * self.__selected_pos[1]

        self.__selected_texture.set_position([x_pos, y_pos])

    def get_bottom_drawer_inventory(self):
        return self.__bottom_drawer_inventory

    @staticmethod
    def __nestrepl(lst, instance, repl):
        """From: https://stackoverflow.com/questions/24516340/replace-all-occurrences-of-item-in-sublists-within-list"""
        for index, item in enumerate(lst):
            if isinstance(item, list):
                Fridge.__nestrepl(item, instance, repl)
            else:
                if item == instance:
                    lst[index] = repl
