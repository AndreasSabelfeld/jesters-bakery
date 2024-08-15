import threading

from OpenGL.GLUT import *

from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import FirstPersonPlayer
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.order import MasterOrder, Order
from src.game_mechanics.pick_up import Carry
from src.game_mechanics.scanner import Scanner
from src.game_mechanics.tap import Tap
from src.game_ui.ui import UI
from src.master import prefabs
from src.master.levels import Levels
from src.models.textured_model import TexturedModel
from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.input_controller import KeyboardInput
from src.render_engine.loader import Loader
from src.game_mechanics.coffee_container import CoffeeContainer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.time import Time
from src.terrain.terrain import Terrain
from src.textures.model_texture import ModelTexture
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack
from src.toolbox.raycaster import TerrainRaycaster, ObjectRaycaster


class GameMaster:
    def __init__(self):
        self.__entities = []
        self.__nm_entities = []
        self.__collider_entities = []
        self.__shadow_map_entities = []
        self.__terrains = []
        self.__lights = []

        self.__display = DisplayManager(1920, 1080)
        self.__display.create_display("An-gine")  # creates display
        self.__display.set_backdrop_color(173, 216, 230)

        self.__loader = Loader()
        self.__obj_loader = OBJLoader()
        self.__normal_mapped_obj_loader = NormalMappedOBJLoader()
        CoffeeContainer.add_loaders(self.__loader, self.__obj_loader)
        TextMaster(self.__loader)

        player_model = self.__obj_loader.load_obj_model("objs/legacy/bunny", self.__loader)
        static_player_model = TexturedModel(player_model, ModelTexture(self.__loader.load_texture("pngs/machinery/white")))

        self.__player = FirstPersonPlayer(static_player_model, [160.5, 5.18, 180], 0, 0, 0, 14)
        self.__player.set_player_size(14)
        self.__camera = Camera(self.__player)

        self.__master_renderer = MasterRenderer(self.__loader, self.__camera)
        self.__master_renderer.set_fog_density(0.0035)
        self.__master_renderer.set_fog_gradient(5)
        self.__master_renderer.get_shadow_map_texture()

        self.__gui_renderer = GuiRenderer(self.__loader)

        self.__terrain_picker = TerrainRaycaster(self.__camera, self.__master_renderer.get_projection_matrix())
        self.__object_picker = ObjectRaycaster(self.__camera, self.__master_renderer.get_projection_matrix())

        self.__sun = Light([100000, 150000, -100000], [253/255, 243/255, 198/255])
        self.__lights.append(self.__sun)

        self.__scanner = Scanner(self.__object_picker, self.__loader, self.__gui_renderer)

        size = 1.75
        self.__coffee_machine       = self.__load_coffee_machine(size)
        self.__coffee_machine_lf    = self.__load_coffee_machine_lactose_free(size)
        self.__fridge               = self.__load_fridge(size)
        self.__work_drawer          = self.__load_work_drawer(size)
        self.__milk_foamer          = self.__load_milk_foamer()
        self.__mixer_vessel         = self.__load_mixer_vessel()
        self.__counter              = self.__load_counter(size)
        self.__finished_collider    = self.__load_finished_collider(size)
        self.__ticket_machine       = self.__load_ticket_machine()
        self.__tap                  = self.__load_tap()

        self.__coffee_os                = self.__coffee_machine.get_attachment()
        self.__coffee_os_lactose_free   = self.__coffee_machine_lf.get_attachment()
        self.__fridge_os                = self.__fridge.get_child_0().get_attachment()
        self.__work_drawer_os           = self.__work_drawer.get_child_0().get_attachment()
        self.__milk_foamer_os           = self.__milk_foamer.get_attachment()
        self.__mixer_vessel_os          = self.__mixer_vessel.get_attachment()
        self.__master_order             = MasterOrder(self.__loader, self.__obj_loader, self.__gui_renderer, self.__counter)

        self.__finished_collider.set_attachment(self.__master_order)

        self.__carry = Carry(self.__terrain_picker, self.__object_picker, self.__coffee_machine, self.__coffee_machine_lf)
        self.__carry.movable_entities = self.__collider_entities

        self.__level_master = Levels(self.__master_order, self.__ticket_machine, self.__entities, self.__collider_entities, self.__shadow_map_entities)
        self.__game_ui = UI(self.__loader, self.__gui_renderer, self.__level_master, self.__display)
        self.__game_ui.loading_screen(Time.time_current_time())

        self.__load_game()

    def __load_game(self):
        self.__game_ui.loading_screen(self.__load_terrain())
        self.__game_ui.loading_screen(self.__load_ui())
        self.__game_ui.loading_screen(self.__load_machines())
        self.__game_ui.loading_screen(self.__load_spawns())
        self.__game_ui.loading_screen(self.__load_entrance_area())
        self.__game_ui.loading_screen(self.__load_traiteur_area())
        self.__game_ui.loading_screen(self.__load_working_area())
        self.__game_ui.loading_screen(self.__load_kitchen_area())
        self.__game_ui.loading_screen(self.__load_eating_area())
        self.__game_ui.loading_screen(self.__load_chairs())
        self.__game_ui.loading_screen(self.__load_food())
        self.__game_ui.loading_screen(self.__load_walls())
        self.__game_ui.loading_screen(self.__load_outside_area())

        self.start_game()

    def start_game(self):
        args = (self.__master_renderer, self.__entities, self.__nm_entities, self.__terrains, self.__lights,
                self.__camera, self.__shadow_map_entities, self.__sun)

        self.__game_ui.main_menu(*args)

        self.__camera.set_position([160.5, 5.18, 180])
        self.__player.set_position([160.5, 5.18, 180])
        self.__level_master.set_countdown(10)
        self.__level_master.start_current_day()

        self.game_loop()

    def game_loop(self):
        first_frame = [True]        # to use it like a pointer
        while glutGetWindow() != 0:
            Time.set_current_time(Time.time_current_time())
            Time.set_delta_time()   # automatically calculates delta time
            Time.set_last_frame_time(Time.time_current_time())

            self.__move_player(first_frame)
            self.__update_objects()
            self.__render()

            glutSwapBuffers()       # needs to be called AFTER finished drawing
            glutMainLoopEvent()     # used to run openGL manually in a loop instead of glutMainLoop()

    def stop_game(self):
        ...

    def __move_player(self, first_frame: list[bool]) -> None:
        if not first_frame[0]:
            # in the first frame delta_time is zero
            self.__player.move(self.__collider_entities)

        # if player is interacting with any of these:
        if not (self.__coffee_os.get_is_interacting() or self.__coffee_os_lactose_free.get_is_interacting() or
                self.__fridge_os.get_is_interacting() or self.__work_drawer_os.get_is_interacting()):
            self.__camera.move()
            self.__carry.update()
        else:
            self.__carry.update(False)

        first_frame[0] = False

    def __update_objects(self) -> None:
        self.__level_master.update()
        self.__game_ui.game_loop()
        self.__object_picker.update(self.__collider_entities)
        self.__scanner.update(self.__collider_entities)
        self.__coffee_os.interact(self.__player, self.__camera)
        self.__coffee_os_lactose_free.interact(self.__player, self.__camera)
        self.__work_drawer_os.interact(self.__player, self.__camera)
        self.__fridge_os.interact(self.__player, self.__camera)
        self.__coffee_os.render_screen()
        self.__coffee_os_lactose_free.render_screen()
        self.__milk_foamer_os.update()
        self.__tap.update()
        self.__mixer_vessel_os.update()
        self.__fridge_os.update(self.__carry)
        self.__work_drawer_os.update(self.__carry)

    def __render(self) -> None:
        self.__master_renderer.render_shadow_map(self.__shadow_map_entities, self.__sun)
        self.__master_renderer.render_scene(self.__entities, self.__nm_entities, self.__terrains, self.__lights,
                                            self.__camera, self.__display)
        specified = [self.__scanner.get_text()]
        self.__fridge_os.render_selected_texture()
        self.__work_drawer_os.render_selected_texture()
        self.__scanner.render_crosshair()
        self.__game_ui.render()
        TextMaster.render_specified(specified)

    def __load_terrain(self) -> float:
        background_texture = TerrainTexture(self.__loader.load_texture("pngs/shop/asphalt"))
        r_texture = TerrainTexture(self.__loader.load_texture("pngs/shop/floor_tiles"))
        g_texture = TerrainTexture(self.__loader.load_texture("pngs/shop/asphalt"))
        b_texture = TerrainTexture(self.__loader.load_texture(""))

        texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
        blend_map = TerrainTexture(self.__loader.load_texture("pngs/shop/bakery_blendmap"))

        Terrain.set_size(300)
        terrain = Terrain(0, 0, self.__loader, texture_pack, blend_map, "pngs/shop/bakery_heightmap")
        self.__terrains.append(terrain)
        return Time.time_current_time()

    def __load_ui(self) -> float:
        font = FontType(self.__loader.load_texture("fnts/candara"), "res/fnts/candara.fnt")
        text1 = GUIText("a sample text!", 15, font, [0, 0.02], 1, False)
        text1.set_color(1, 0, 0)
        text1.set_border_width(0.7)
        text1.set_border_edge(0.1)
        text2 = GUIText("a sample text!", 20, font, [0, 0.1], 1, False)
        text2.set_color(1, 0, 0)
        text2.set_border_width(0.7)
        text2.set_border_edge(0.1)
        text3 = GUIText("a sample text!", 20, font, [0, 0.2], 1, False)
        text3.set_color(1, 0, 0)
        text3.set_border_width(0.7)
        text3.set_border_edge(0.1)
        return Time.time_current_time()

    def __load_machines(self) -> float:
        size = 1.75
        ice_machine_door = prefabs.ice_machine([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader,
                                               self.__obj_loader, self.__entities, self.__collider_entities)
        mixer_game_object = prefabs.mixer([150, 12.5, 185], [0, 90, 0], 0.5, self.__loader, self.__obj_loader)
        heater = prefabs.cup_heater([150, 12.5, 194], [0, 90, 0], size, self.__loader, self.__obj_loader,
                                    self.__entities, self.__collider_entities)

        machines = [ice_machine_door, mixer_game_object, heater]
        self.__entities.extend(machines)
        self.__collider_entities.extend(machines)
        self.__collider_entities.extend([heater.get_child_0(), heater.get_child_1()])
        self.__shadow_map_entities.extend(machines)
        return Time.time_current_time()

    def __load_spawns(self) -> float:
        size = 1.75
        small_glass_spawn = prefabs.small_glass_spawn([176, 12.5, 182], [0, -90, 0], 1, self.__loader, self.__obj_loader, self.__entities,
                                                      self.__collider_entities)
        plate_spawn = prefabs.plate_spawn([176, 12.5, 194], [0, -90, 0], 0.5, self.__loader, self.__obj_loader, self.__entities,
                                          self.__collider_entities)
        glas_ablage = prefabs.glas_ablage([150, 7, 173.5], [0, -90, 0], size, self.__loader, self.__obj_loader, self.__entities,
                                          self.__collider_entities)
        bier_ablage = prefabs.bier_ablage([146.5, 7, 184.6], [0, 90, 0], size, self.__loader, self.__obj_loader, self.__entities,
                                          self.__collider_entities)
        tee_ablage = prefabs.tee_ablage([146.5, 7, 184.5], [0, -90, 0], size, self.__loader, self.__obj_loader, self.__entities,
                                        self.__collider_entities)
        prosecco_ablage = prefabs.prosecco_ablage([146.5, 7, 184.5], [0, -90, 0], size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        espresso_spawn = prefabs.espresso_spawn([151, 18.5, 199], [0, 90, 0], 1, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)

        spawns = [small_glass_spawn, plate_spawn, glas_ablage, bier_ablage, tee_ablage, prosecco_ablage, espresso_spawn]
        self.__entities.extend(spawns)
        self.__collider_entities.extend(spawns)
        self.__shadow_map_entities.extend(spawns)
        return Time.time_current_time()

    def __load_entrance_area(self) -> float:
        size = 1.75
        front_counter = prefabs.front_counter([179.5, 5.18, 188.75], [0, -90, 0], size, self.__loader, self.__obj_loader)
        back_counter = prefabs.back_counter([146, 5.18, 202], [0, -90, 0], size, self.__loader, self.__obj_loader)
        kleine_theke_1 = prefabs.kleine_theke_1([167.5, 5.18, 288], [0, -90, 0], size, self.__loader, self.__obj_loader)
        kleine_theke_2 = prefabs.kleine_theke_2([207, 5.18, 238], [0, -90, 0], size - 0.05, self.__loader, self.__obj_loader)
        regal = prefabs.regal([204.4, 5.18, 210.5], [0, -90, 0], size, self.__loader, self.__obj_loader)

        entrance = [front_counter, back_counter, kleine_theke_2, kleine_theke_1, regal]

        self.__entities.extend(entrance)
        self.__collider_entities.extend(entrance)
        self.__shadow_map_entities.extend(entrance)
        return Time.time_current_time()

    def __load_traiteur_area(self) -> float:
        size = 1.75
        traiteur_front_counter = prefabs.traiteur_front_counter([101, 5.18, 242], [0, -90, 0], size, self.__loader, self.__obj_loader)
        traiteur_back_counter = prefabs.traiteur_back_counter([80, 5.18, 244], [0, -90, 0], size, self.__loader, self.__obj_loader)
        traiteur_freezer = prefabs.traiteur_freezer([80, 5.18, 229], [0, -90, 0], size, self.__loader, self.__obj_loader)
        traiteur_back_schrank = prefabs.traiteur_back_schrank([80, 5.18, 244], [0, -90, 0], size, self.__loader, self.__obj_loader)
        traiteur_klapptisch = prefabs.traiteur_klapptisch([101, 5.18, 230], [0, -90, 0], size, self.__loader, self.__obj_loader)
        traiteur_klapptisch_schrank = prefabs.traiteur_klapptisch_schrank([101, 5.18, 230], [0, -90, 0], size, self.__loader, self.__obj_loader)

        traiteur = [traiteur_freezer, traiteur_front_counter, traiteur_klapptisch_schrank, traiteur_klapptisch, traiteur_back_schrank, traiteur_back_counter]

        self.__entities.extend(traiteur)
        self.__collider_entities.extend(traiteur)
        self.__shadow_map_entities.extend(traiteur)
        return Time.time_current_time()

    def __load_working_area(self) -> float:
        size = 1.75
        table_12 = prefabs.table_12([217, 5.18, 177], [0, -90, 0], size, self.__loader, self.__obj_loader)
        table_11 = prefabs.table_12([217, 5.18, 141], [0, -90, 0], size, self.__loader, self.__obj_loader)
        workplate2 = prefabs.workplate2([150, 5.18, 190.5], [0, -90, 0], size, self.__loader, self.__obj_loader)

        working_area = [table_12, table_11, workplate2]

        self.__entities.extend(working_area)
        self.__collider_entities.extend(working_area)
        self.__shadow_map_entities.extend(working_area)
        return Time.time_current_time()

    def __load_kitchen_area(self) -> float:
        size = 1.75
        kitchen = prefabs.kitchen([145, 5.18, 149], [0, -90, 0], size, self.__loader, self.__obj_loader)

        self.__entities.append(kitchen)
        self.__collider_entities.append(kitchen)
        self.__shadow_map_entities.append(kitchen)
        return Time.time_current_time()

    def __load_eating_area(self) -> float:
        size = 1.75
        kommode = prefabs.kommode([207, 5.18, 132], [0, -90, 0], size - 0.15, self.__loader, self.__obj_loader)
        small_table = prefabs.small_table([207, 5.18, 111], [0, -90, 0], size, self.__loader, self.__obj_loader)
        table_1_2 = prefabs.table_1_2([186, 5.18, 89], [0, -90, 0], size, self.__loader, self.__obj_loader)

        table_3_5 = prefabs.table_3_5([106, 5.18, 103], [0, -90, 0], size, self.__loader, self.__obj_loader)

        table_6_9 = prefabs.table_6_9([209, 5.18, 53], [0, -90, 0], size, self.__loader, self.__obj_loader)

        table_37 = prefabs.table_37([122, 5.18, 58], [0, -90, 0], size, self.__loader, self.__obj_loader)

        eating_area = [kommode, small_table, table_1_2, table_3_5, table_6_9, table_37]
        self.__entities.extend(eating_area)
        self.__collider_entities.extend(eating_area)
        self.__shadow_map_entities.extend(eating_area)
        return Time.time_current_time()

    def __load_chairs(self) -> float:
        chairs = []
        size = 1.75
        for i in range(8):
            chairs.append(prefabs.chair([182 - 7 * i, 5.18, 95], [0, 180, 0], size, self.__loader, self.__obj_loader))
            chairs.append(prefabs.chair([182 - 7 * i, 5.18, 83], [0, 0, 0], size, self.__loader, self.__obj_loader))

        chairs.append(prefabs.chair([115, 5.18, 100], [0, -90, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([115, 5.18, 93], [0, -90, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([115, 5.18, 83], [0, -90, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([115, 5.18, 71], [0, -90, 0], size, self.__loader, self.__obj_loader))

        chairs.append(prefabs.chair([205, 5.18, 63], [0, 180, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([190, 5.18, 63], [0, 180, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([175, 5.18, 63], [0, 180, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([162, 5.18, 63], [0, 180, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([152, 5.18, 63], [0, 180, 0], size, self.__loader, self.__obj_loader))

        chairs.append(prefabs.chair([137, 5.18, 58], [0, -90, 0], size, self.__loader, self.__obj_loader))
        chairs.append(prefabs.chair([122, 5.18, 58], [0, 90, 0], size, self.__loader, self.__obj_loader))

        self.__entities.extend(chairs)
        self.__collider_entities.extend(chairs)
        self.__shadow_map_entities.extend(chairs)
        return Time.time_current_time()

    def __load_food(self) -> float:
        food_size = 0.5
        prefabs.ham_sandwich([175.5, 11, 203.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.ham_sandwich([178.5, 11, 203.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.ham_sandwich([181.5, 11, 203.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.ham_sandwich([184.5, 11, 203.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.egg_sandwich([174.5, 11, 209.0], [0, -10, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.egg_sandwich([177.5, 11, 210.0], [0, -10, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.egg_sandwich([180.5, 11, 210.0], [0, -10, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.egg_sandwich([183.5, 11, 211.0], [0, -10, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tuna_sandwich([172.5, 11, 215.0], [0, -20, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tuna_sandwich([175.5, 11, 216.0], [0, -20, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tuna_sandwich([178.5, 11, 217.0], [0, -20, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tuna_sandwich([181.5, 11, 218.0], [0, -20, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.mango_chutney_sandwich([169.5, 11, 221.0], [0, -30, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.mango_chutney_sandwich([172.5, 11, 222.0], [0, -30, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.mango_chutney_sandwich([175.5, 11, 223.0], [0, -30, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.mango_chutney_sandwich([178.5, 11, 224.0], [0, -30, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tomato_sandwich([166.5, 11, 227.0], [0, -40, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tomato_sandwich([169.5, 11, 229.0], [0, -40, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tomato_sandwich([172.5, 11, 231.0], [0, -40, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.tomato_sandwich([175.5, 11, 233.0], [0, -40, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.silserli([163.5, 11, 230.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.silserli([165.5, 11, 232.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.silserli([167.5, 11, 234.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.silserli([169.5, 11, 236.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([143, 10.5, 206], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([146, 10.5, 206], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([142, 10.5, 211], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([145, 10.5, 213], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([137, 10.5, 214], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([140, 10.5, 217], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([133, 10.5, 218], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([134, 10.5, 221], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([128, 10.5, 220], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.croissant([128, 10.5, 223], [0, -140, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_croissant([144, 15, 209], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_croissant([142, 15, 213], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_croissant([138, 15, 217.5], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_croissant([133, 15, 221], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.almond_croissant([144, 18.75, 209], [0, 90, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.almond_croissant([142, 18.75, 213], [0, 90, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.almond_croissant([138, 18.75, 217.5], [0, 90, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.almond_croissant([133, 18.75, 219], [0, 90, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.strawberry_tart([160.5, 11, 233.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.strawberry_tart([162.5, 11, 235.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.strawberry_tart([165.0, 11, 237.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.strawberry_tart([167.5, 11, 239.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.cookie([159.5, 11.1, 235.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.cookie([161.5, 11.1, 237.5], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.cookie([163.5, 11.1, 239.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.cookie([165.5, 11.1, 242.5], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.spitzbub([158.0, 11.1, 236.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.spitzbub([160.5, 11.1, 239.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.spitzbub([162.5, 11.1, 242.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.spitzbub([164.5, 11.1, 245.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.linzerli([156.5, 11.1, 237.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.linzerli([158.5, 11.1, 240.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.linzerli([160.5, 11.1, 243.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.linzerli([162.5, 11.1, 246.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carac([154.5, 11.1, 238.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carac([156.5, 11.1, 241.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carac([158.5, 11.1, 244.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carac([160.5, 11.1, 247.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.wurstwegge([152.5, 11.1, 240.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.wurstwegge([154.5, 11.1, 243.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.wurstwegge([156.5, 11.1, 246.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.wurstwegge([158.5, 11.1, 249.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.schinkengipfel([149.5, 11.1, 242.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.schinkengipfel([151.5, 11.1, 245.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.schinkengipfel([153.5, 11.1, 248.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.schinkengipfel([155.5, 11.1, 251.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_cake([145.5, 11.1, 243.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_cake([147.5, 11.1, 246.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_cake([149.5, 11.1, 249.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.chocolate_cake([151.5, 11.1, 252.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.passionfruit_cake([141.5, 11.1, 244.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.passionfruit_cake([143.0, 11.1, 247.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.passionfruit_cake([144.5, 11.1, 250.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.passionfruit_cake([146.0, 11.1, 253.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carrot_cake([137.5, 11.1, 245.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carrot_cake([138.5, 11.1, 248.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carrot_cake([139.5, 11.1, 251.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.carrot_cake([140.5, 11.1, 254.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.citron_cake([133.5, 11.1, 246.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.citron_cake([134.0, 11.1, 249.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.citron_cake([134.5, 11.1, 252.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        prefabs.citron_cake([135.0, 11.1, 255.0], [0, 0, 0], food_size, self.__loader, self.__obj_loader, self.__entities, self.__collider_entities)
        return Time.time_current_time()

    def __load_walls(self) -> float:
        size = 1.75
        south_wall_traiteur = prefabs.south_wall_traiteur([80, 5.18, 295], [0, -90, 0], size, self.__loader, self.__obj_loader)
        east_wall_1 = prefabs.east_wall_1([202.5, 5.18, 271.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        east_wall_2 = prefabs.east_wall_2([228, 5.18, 207.5], [0, -90, 0], size, self.__loader, self.__obj_loader, self.__normal_mapped_obj_loader)
        north_wall_essbereich = prefabs.north_wall_essbereich([211, 5.18, 42], [0, -90, 0], size, self.__loader, self.__obj_loader)
        west_wall_essbereich = prefabs.west_wall_essbereich([94.5, 5.18, 50], [0, -90, 0], size, self.__loader, self.__obj_loader)
        north_wall_kitchen = prefabs.north_wall_kitchen([96, 5.18, 106], [0, -90, 0], size, self.__loader, self.__obj_loader)
        west_wall_kitchen = prefabs.west_wall_kitchen([135.9, 5.18, 149], [0, -90, 0], size, self.__loader, self.__obj_loader)
        west_wall_arbeitsbereich = prefabs.west_wall_arbeitsbereich([145, 5.18, 173.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        north_wall_traiteur = prefabs.north_wall_traiteur([123, 5.18, 220.75], [0, -90, 0], size, self.__loader, self.__obj_loader)
        west_wall_traiteur = prefabs.west_wall_traiteur([75, 5.18, 226], [0, -90, 0], size, self.__loader, self.__obj_loader)
        ceiling = prefabs.ceiling([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        column = prefabs.column([172, 5.18, 176], [0, -90, 0], size, self.__loader, self.__obj_loader)
        column2 = prefabs.column([127, 5.18, 252], [0, 13, 0], size, self.__loader, self.__obj_loader)

        walls = [south_wall_traiteur, east_wall_1, east_wall_2, north_wall_essbereich, west_wall_essbereich, north_wall_kitchen,
                 west_wall_kitchen, west_wall_arbeitsbereich, north_wall_traiteur, west_wall_traiteur, ceiling, column, column2]
        self.__entities.extend(walls)
        self.__collider_entities.extend(walls)
        return Time.time_current_time()

    def __load_outside_area(self) -> float:
        size = 1.75
        outside_essbereich = prefabs.outside_essbereich([87, 3.5, 76], [0, -90, 0], size, self.__loader, self.__obj_loader)
        outside_hecke = prefabs.outside_hecke([220, 3.5, 64], [0, -90, 0], size, self.__loader, self.__obj_loader)
        outside_streets = prefabs.outside_streets([170, 3.5, 275], [0, -90, 0], size, self.__loader, self.__obj_loader)

        outside = [outside_hecke, outside_streets, outside_essbereich]
        self.__entities.extend(outside)
        return Time.time_current_time()

    def __load_coffee_machine(self, size: float) -> GameObject:
        coffee_machine_game_object = prefabs.coffee_machine([150, 12.5, 190], [0, 90, 0], size,
                                                            self.__loader,
                                                            self.__obj_loader,
                                                            self.__gui_renderer,
                                                            self.__object_picker)
        self.__entities.append(coffee_machine_game_object)
        self.__collider_entities.append(coffee_machine_game_object)
        self.__shadow_map_entities.append(coffee_machine_game_object)
        return coffee_machine_game_object

    def __load_coffee_machine_lactose_free(self, size: float) -> GameObject:
        coffee_machine_lactose_free_game_object = prefabs.lactose_free_coffee_machine([150, 12.5, 198], [0, 90, 0],
                                                                                      size,
                                                                                      self.__loader,
                                                                                      self.__obj_loader,
                                                                                      self.__gui_renderer,
                                                                                      self.__object_picker)
        self.__entities.append(coffee_machine_lactose_free_game_object)
        self.__collider_entities.append(coffee_machine_lactose_free_game_object)
        self.__shadow_map_entities.append(coffee_machine_lactose_free_game_object)
        return coffee_machine_lactose_free_game_object

    def __load_fridge(self, size: float) -> GameObject:
        fridge_game_object = prefabs.fridge([149.7, 5.18, 187.6], [0, 90, 0], size, self.__loader,
                                            self.__obj_loader, self.__gui_renderer, self.__object_picker)
        self.__entities.append(fridge_game_object)
        self.__collider_entities.extend([fridge_game_object, fridge_game_object.get_child_0(), fridge_game_object.get_child_1()])
        self.__shadow_map_entities.append(fridge_game_object)
        return fridge_game_object

    def __load_work_drawer(self, size: float) -> GameObject:
        workplate = prefabs.workplate1([150, 5.18, 173.5], [0, -90, 0], size, self.__loader, self.__obj_loader,
                                       self.__gui_renderer, self.__object_picker)
        self.__entities.append(workplate)
        self.__collider_entities.extend([workplate, workplate.get_child_0(), workplate.get_child_1()])
        self.__shadow_map_entities.append(workplate)
        return workplate

    def __load_milk_foamer(self) -> GameObject:
        milk_foamer_game_object = prefabs.milk_foamer([150, 12.5, 175], [0, 90, 0], 1, self.__loader, self.__obj_loader,
                                                      self.__gui_renderer, self.__object_picker)
        self.__entities.extend([milk_foamer_game_object, milk_foamer_game_object.get_child_0(), milk_foamer_game_object.get_child_1()])
        self.__collider_entities.extend([milk_foamer_game_object, milk_foamer_game_object.get_child_0(), milk_foamer_game_object.get_child_1()])
        self.__shadow_map_entities.extend([milk_foamer_game_object, milk_foamer_game_object.get_child_0(), milk_foamer_game_object.get_child_1()])
        return milk_foamer_game_object

    def __load_mixer_vessel(self) -> GameObject:
        mixer_vessel_game_object = prefabs.mixer_vessel([150, 12.5, 183], [0, 90, 0], 0.5, self.__loader,
                                                        self.__obj_loader)
        self.__entities.append(mixer_vessel_game_object)
        self.__collider_entities.append(mixer_vessel_game_object)
        self.__shadow_map_entities.append(mixer_vessel_game_object)
        return mixer_vessel_game_object

    def __load_counter(self, size: float) -> GameObject:
        counter = prefabs.finished_counter([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        self.__entities.append(counter)
        self.__collider_entities.append(counter)
        self.__shadow_map_entities.append(counter)
        return counter

    def __load_finished_collider(self, size: float) -> GameObject:
        col = prefabs.finished_collider([179.5, 5.18, 185.5], [0, -90, 0], size, self.__loader, self.__obj_loader)
        self.__collider_entities.append(col)
        return col

    def __load_ticket_machine(self) -> GameObject:
        ticket_machine = prefabs.ticket_machine([174, 12.5, 198], [0, -90, 0], 1, self.__loader, self.__obj_loader)
        self.__entities.append(ticket_machine)
        self.__collider_entities.append(ticket_machine)
        self.__shadow_map_entities.append(ticket_machine)
        return ticket_machine

    def __load_tap(self) -> Tap:
        textures = [ModelTexture(self.__loader.load_texture("pngs/cups/coke_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/schorle_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/water_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/water_filling_tex")),
                    ModelTexture(self.__loader.load_texture("pngs/cups/beer_filling_tex"))]
        tap = Tap(self.__obj_loader, self.__loader, [179.5, 12.5, 185.5], [0, -90, 0], 1, textures)
        self.__entities.extend(tap.get_game_objects())
        self.__collider_entities.extend(tap.get_game_objects())
        self.__collider_entities.remove(tap.get_base())
        self.__shadow_map_entities.extend(tap.get_game_objects())
        return tap

    def get_master_order(self) -> MasterOrder:
        return self.__master_order

    def get_ticket_machine(self) -> GameObject:
        return self.__ticket_machine

    def get_entities(self) -> list:
        return self.__entities

    def get_collider_entities(self) -> list:
        return self.__collider_entities

    def get_shadow_map_entities(self) -> list:
        return self.__shadow_map_entities

    def get_normal_map_entities(self) -> list:
        return self.__nm_entities
