from OpenGL.GLUT import *

from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.order import MasterOrder, Order
from src.game_mechanics.tap import Tap
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.loader import Loader
from src.render_engine.time import Time
from src.render_engine.input_controller import KeyboardInput

from src.textures.model_texture import ModelTexture
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack

from src.models.textured_model import TexturedModel

from src.entities.entity import Entity
from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import FirstPersonPlayer

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster, ObjectRaycaster

from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader

from src.font_rendering.text_master import TextMaster
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText

from src.game_mechanics.pick_up import Carry
from src.game_mechanics.scanner import Scanner

import src.master.prefabs as prefabs


def main():
    # ~~~~~~~~~~~~DISPLAY~~~~~~~~~~~~~~
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(173, 216, 230)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~LOADERS~~~~~~~~~~~~~~
    loader = Loader()
    obj_loader = OBJLoader()
    normal_mapped_obj_loader = NormalMappedOBJLoader()
    CoffeeContainer.add_loaders(loader, obj_loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~TEXT~~~~~~~~~~~~~~~~
    TextMaster(loader)
    font = FontType(loader.load_texture("candara"), "res/candara.fnt")
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

    # ~~~~~~~~~~~~TERRAIN~~~~~~~~~~~~~~~
    background_texture = TerrainTexture(loader.load_texture("asphalt"))
    r_texture = TerrainTexture(loader.load_texture("floor_tiles"))
    g_texture = TerrainTexture(loader.load_texture("asphalt"))
    b_texture = TerrainTexture(loader.load_texture(""))

    texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
    blend_map = TerrainTexture(loader.load_texture("bakery_blendmap"))

    terrains = []
    Terrain.set_size(300)
    terrain = Terrain(0, 0, loader, texture_pack, blend_map, "bakery_heightmap")
    terrains.append(terrain)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("objs/legacy/bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [160.5, 5.18, 180], 0, 0, 0, 3)
    player.set_player_size(14)
    camera = Camera(player)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~RENDERER~~~~~~~~~~~~~~~
    master_renderer = MasterRenderer(loader, camera)
    master_renderer.set_fog_density(0.0035)
    master_renderer.set_fog_gradient(5)
    master_renderer.get_shadow_map_texture()

    gui_renderer = GuiRenderer(loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~MOUSE PICKER~~~~~~~~~~~~
    terrain_picker = TerrainRaycaster(camera, master_renderer.get_projection_matrix())
    object_picker = ObjectRaycaster(camera, master_renderer.get_projection_matrix())
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    entities = []
    nm_entities = []
    collider_entities = []

    grass_texture = ModelTexture(loader.load_texture("grass_block"))
    textures = [ModelTexture(loader.load_texture("pngs/cups/coke_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/schorle_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/beer_filling_tex"))]

    machine_size = 1.75
    mixer_size = 0.5

    counter_pos = [179.5, 5.18, 185.5]
    counter_rot = [0, -90, 0]
    front_counter = prefabs.front_counter([179.5, 5.18, 188.75], counter_rot, machine_size, loader, obj_loader)
    back_counter = prefabs.back_counter([146, 5.18, 202], counter_rot, machine_size, loader, obj_loader)

    traiteur_rot = [0, -90, 0]
    traiteur_front_counter = prefabs.traiteur_front_counter([101, 5.18, 242], traiteur_rot, machine_size, loader, obj_loader)
    traiteur_back_counter = prefabs.traiteur_back_counter([80, 5.18, 244], traiteur_rot, machine_size, loader, obj_loader)
    traiteur_freezer = prefabs.traiteur_freezer([80, 5.18, 229], traiteur_rot, machine_size, loader, obj_loader)
    traiteur_back_schrank = prefabs.traiteur_back_schrank([80, 5.18, 244], traiteur_rot, machine_size, loader, obj_loader)
    traiteur_klapptisch = prefabs.traiteur_klapptisch([101, 5.18, 230], traiteur_rot, machine_size, loader, obj_loader)
    traiteur_klapptisch_schrank = prefabs.traiteur_klapptisch_schrank([101, 5.18, 230], traiteur_rot, machine_size, loader, obj_loader)

    counter_game_object = prefabs.finished_counter(counter_pos, counter_rot, machine_size, loader, obj_loader)
    small_glass_spawn = prefabs.small_glass_spawn([176, 12.5, 182], [0, -90, 0], 1, loader, obj_loader, entities, collider_entities)
    plate_spawn = prefabs.plate_spawn([176, 12.5, 194], [0, -90, 0], 0.5, loader, obj_loader, entities, collider_entities)
    ticket_machine = prefabs.ticket_machine([174, 12.5, 198], [0, -90, 0], 1, loader, obj_loader)
    ice_machine_door = prefabs.ice_machine(counter_pos, counter_rot, machine_size, loader, obj_loader, entities,
                                           collider_entities)
    finished_col = prefabs.finished_collider(counter_pos, counter_rot, machine_size, loader, obj_loader)
    kleine_theke_1 = prefabs.kleine_theke_1([167.5, 5.18, 288], traiteur_rot, machine_size, loader, obj_loader)
    kleine_theke_2 = prefabs.kleine_theke_2([207, 5.18, 238], traiteur_rot, machine_size-0.05, loader, obj_loader)
    regal = prefabs.regal([204.4, 5.18, 210.5], traiteur_rot, machine_size, loader, obj_loader)
    table_12 = prefabs.table_12([217, 5.18, 177], traiteur_rot, machine_size, loader, obj_loader)
    table_11 = prefabs.table_12([217, 5.18, 141], traiteur_rot, machine_size, loader, obj_loader)
    workplate1 = prefabs.workplate1([150, 5.18, 173.5], traiteur_rot, machine_size, loader, obj_loader, gui_renderer, object_picker)
    workplate2 = prefabs.workplate2([150, 5.18, 190.5], traiteur_rot, machine_size, loader, obj_loader)
    glas_ablage = prefabs.glas_ablage([150, 7, 173.5], traiteur_rot, machine_size, loader, obj_loader, entities, collider_entities)
    bier_ablage = prefabs.bier_ablage([146.5, 7, 184.6], [0, 90, 0], machine_size, loader, obj_loader, entities, collider_entities)
    tee_ablage = prefabs.tee_ablage([146.5, 7, 184.5], traiteur_rot, machine_size, loader, obj_loader, entities, collider_entities)
    prosecco_ablage = prefabs.prosecco_ablage([146.5, 7, 184.5], traiteur_rot, machine_size, loader, obj_loader, entities, collider_entities)

    coffee_machine_game_object = prefabs.coffee_machine([150, 12.5, 190], [0, 90, 0], machine_size, loader, obj_loader,
                                                        gui_renderer, object_picker)
    coffee_machine_lactose_free_game_object = prefabs.lactose_free_coffee_machine([150, 12.5, 198], [0, 90, 0], machine_size,
                                                                                  loader, obj_loader,
                                                                                  gui_renderer, object_picker)
    heater = prefabs.cup_heater([150, 12.5, 194], [0, 90, 0], machine_size, loader, obj_loader, entities, collider_entities)
    espresso_spawn = prefabs.espresso_spawn([151, 18.5, 199], [0, 90, 0], 1, loader, obj_loader, entities, collider_entities)
    fridge_game_object = prefabs.fridge([149.7, 5.18, 187.6], [0, 90, 0], machine_size, loader, obj_loader,
                                        gui_renderer, object_picker,)
    milk_foamer_game_object = prefabs.milk_foamer([150, 12.5, 175], [0, 90, 0], 1, loader, obj_loader,
                                                  gui_renderer, object_picker)
    milk_foamer_screen = milk_foamer_game_object.get_attachment().get_render_target()
    mixer_game_object = prefabs.mixer([150, 12.5, 185], [0, 90, 0], mixer_size, loader, obj_loader)
    mixer_vessel_game_object = prefabs.mixer_vessel([150, 12.5, 183], [0, 90, 0], mixer_size, loader, obj_loader)
    tap = Tap(obj_loader, loader, [179.5, 12.5, 185.5], counter_rot, 1, textures)

    kitchen = prefabs.kitchen([145, 5.18, 149], counter_rot, machine_size, loader, obj_loader)

    kommode = prefabs.kommode([207, 5.18, 132], counter_rot, machine_size - 0.15, loader, obj_loader)
    small_table = prefabs.small_table([207, 5.18, 111], counter_rot, machine_size, loader, obj_loader)
    table_1_2 = prefabs.table_1_2([186, 5.18, 89], counter_rot, machine_size, loader, obj_loader)
    chairs = []
    for i in range(8):
        chairs.append(prefabs.chair([182 - 7 * i, 5.18, 95], [0, 180, 0], machine_size, loader, obj_loader))
        chairs.append(prefabs.chair([182 - 7 * i, 5.18, 83], [0, 0, 0], machine_size, loader, obj_loader))

    table_3_5 = prefabs.table_3_5([106, 5.18, 103], counter_rot, machine_size, loader, obj_loader)
    chairs.append(prefabs.chair([115, 5.18, 100], [0, -90, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([115, 5.18, 93], [0, -90, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([115, 5.18, 83], [0, -90, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([115, 5.18, 71], [0, -90, 0], machine_size, loader, obj_loader))

    table_6_9 = prefabs.table_6_9([209, 5.18, 53], counter_rot, machine_size, loader, obj_loader)
    chairs.append(prefabs.chair([205, 5.18, 63], [0, 180, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([190, 5.18, 63], [0, 180, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([175, 5.18, 63], [0, 180, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([162, 5.18, 63], [0, 180, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([152, 5.18, 63], [0, 180, 0], machine_size, loader, obj_loader))

    table_37 = prefabs.table_37([122, 5.18, 58], counter_rot, machine_size, loader, obj_loader)
    chairs.append(prefabs.chair([137, 5.18, 58], [0, -90, 0], machine_size, loader, obj_loader))
    chairs.append(prefabs.chair([122, 5.18, 58], [0, 90, 0], machine_size, loader, obj_loader))

    south_wall_traiteur = prefabs.south_wall_traiteur([80, 5.18, 295], traiteur_rot, machine_size, loader, obj_loader)
    east_wall_1 = prefabs.east_wall_1([202.5, 5.18, 271.5], traiteur_rot, machine_size, loader, obj_loader)
    east_wall_2 = prefabs.east_wall_2([228, 5.18, 207.5], traiteur_rot, machine_size, loader, obj_loader, normal_mapped_obj_loader)
    north_wall_essbereich = prefabs.north_wall_essbereich([211, 5.18, 42], traiteur_rot, machine_size, loader, obj_loader)
    west_wall_essbereich = prefabs.west_wall_essbereich([94.5, 5.18, 50], traiteur_rot, machine_size, loader, obj_loader)
    north_wall_kitchen = prefabs.north_wall_kitchen([96, 5.18, 106], traiteur_rot, machine_size, loader, obj_loader)
    west_wall_kitchen = prefabs.west_wall_kitchen([135.9, 5.18, 149], traiteur_rot, machine_size, loader, obj_loader)
    west_wall_arbeitsbereich = prefabs.west_wall_arbeitsbereich([145, 5.18, 173.5], traiteur_rot, machine_size, loader, obj_loader)
    north_wall_traiteur = prefabs.north_wall_traiteur([123, 5.18, 220.75], traiteur_rot, machine_size, loader, obj_loader)
    west_wall_traiteur = prefabs.west_wall_traiteur([75, 5.18, 226], traiteur_rot, machine_size, loader, obj_loader)
    ceiling = prefabs.ceiling([179.5, 5.18, 185.5], traiteur_rot, machine_size, loader, obj_loader)
    column = prefabs.column([172, 5.18, 176], traiteur_rot, machine_size, loader, obj_loader)
    column2 = prefabs.column([127, 5.18, 252], [0, 13, 0], machine_size, loader, obj_loader)
    outside_essbereich = prefabs.outside_essbereich([87, 3.5, 76], traiteur_rot, machine_size, loader, obj_loader)
    outside_hecke = prefabs.outside_hecke([220, 3.5, 64], traiteur_rot, machine_size, loader, obj_loader)
    outside_streets = prefabs.outside_streets([170, 3.5, 275], traiteur_rot, machine_size, loader, obj_loader)

    entities.extend([coffee_machine_game_object, fridge_game_object, milk_foamer_game_object, milk_foamer_game_object.get_child_0(),
                     milk_foamer_game_object.get_child_1(), milk_foamer_screen, mixer_game_object, mixer_vessel_game_object,
                     coffee_machine_lactose_free_game_object, counter_game_object, *tap.get_game_objects(),
                     ice_machine_door, front_counter, back_counter, traiteur_back_counter, traiteur_freezer, traiteur_front_counter,
                     traiteur_klapptisch_schrank, traiteur_klapptisch, traiteur_back_schrank, kleine_theke_1,
                     kleine_theke_2, regal, table_12, table_11, workplate1, workplate2, kitchen, glas_ablage,
                     kommode, small_table, table_1_2, table_3_5, table_6_9, table_37, bier_ablage, tee_ablage, prosecco_ablage,
                     south_wall_traiteur, east_wall_1, east_wall_2, north_wall_essbereich, west_wall_essbereich,
                     north_wall_kitchen, west_wall_kitchen, west_wall_arbeitsbereich, north_wall_traiteur,
                     west_wall_traiteur, ceiling, column, column2, espresso_spawn, small_glass_spawn, plate_spawn,
                     heater, ticket_machine])
    nm_entities.extend([])
    collider_entities.extend(entities.copy())
    collider_entities.extend(nm_entities.copy())
    collider_entities.extend([fridge_game_object.get_child_0(), fridge_game_object.get_child_1(),
                              milk_foamer_game_object.get_child_0(), milk_foamer_game_object.get_child_1(),
                              counter_game_object, finished_col, workplate1.get_child_0(), workplate1.get_child_1(),
                              heater.get_child_0(), heater.get_child_1()])
    entities.extend([outside_hecke, outside_streets, outside_essbereich])
    entities.extend(chairs)
    print("finished loading assets")
    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([100000, 150000, -100000], [253/255, 243/255, 198/255])
    player_light = Light([0, 0, 0], [1, 1, 1], [1, 0.001, 0.002])
    lights = [sun, player_light]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~GAME~~~~~~~~~~~~~~~~~
    carry = Carry(terrain_picker, object_picker, coffee_machine_game_object, coffee_machine_lactose_free_game_object)
    carry.movable_entities = collider_entities

    scanner = Scanner(object_picker, loader)
    coffee_os = coffee_machine_game_object.get_attachment()
    coffee_os_lactose_free = coffee_machine_lactose_free_game_object.get_attachment()
    fridge = fridge_game_object.get_child_0().get_attachment()
    work_drawer = workplate1.get_child_0().get_attachment()
    milk_foamer_os = milk_foamer_game_object.get_attachment()
    mixer_vessel_os = mixer_vessel_game_object.get_attachment()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    master_order = MasterOrder(loader, obj_loader, gui_renderer, counter_game_object)
    finished_col.set_attachment(master_order)
    order_1 = Order(master_order, 4)
    order_1_ga = order_1.spawn_ticket(ticket_machine)
    entities.append(order_1_ga)
    collider_entities.append(order_1_ga)

    cube_model = obj_loader.load_obj_model("cube", loader)
    static_cube_model = TexturedModel(cube_model, ModelTexture(loader.load_texture("grass_block")))
    cube_texture = static_cube_model.get_texture()

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()  # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        fps = 1 / Time.get_delta_time()

        player.move(collider_entities)
        player_light.set_position(camera.get_position())

        text1.set_text_string(str(fps))
        text2.set_text_string(str(order_1.calculate_points()))
        text3.set_text_string(str(order_1.get_time()))
        if not (coffee_os.get_is_interacting() or coffee_os_lactose_free.get_is_interacting() or fridge.get_is_interacting() or work_drawer.get_is_interacting()):
            camera.move()
            carry.update()
        else:
            carry.update(False)

        object_picker.update(collider_entities)
        scanner.update(collider_entities)

        if KeyboardInput.on_key_down(b'f'):
            # entities.append(Entity(static_cube_model, object_picker.get_current_object_point(), 0, 0, 0, 0.1))
            # print(object_picker.get_current_object_point())
            order_1 = Order(master_order, 4)
            order_1_ga = order_1.spawn_ticket(ticket_machine)
            entities.append(order_1_ga)
            collider_entities.append(order_1_ga)

        master_renderer.render_shadow_map(entities, sun)

        coffee_os.interact(player, camera)
        coffee_os_lactose_free.interact(player, camera)
        work_drawer.interact(player, camera)
        fridge.interact(player, camera)
        coffee_os.render_screen()
        coffee_os_lactose_free.render_screen()
        milk_foamer_os.update()
        tap.update()
        mixer_vessel_os.update()

        master_renderer.render_scene(entities, nm_entities, terrains, lights, camera, display)

        # specified = list()
        # specified.append(order_1.get_gui_text())
        # specified.extend(coffee_os.get_all_texts())
        # specified.extend(coffee_os_lactose_free.get_all_texts())
        # specified.append(milk_foamer_os.get_text())

        specified = [text1, text2, text3]
        TextMaster.render_specified(specified)

        fridge.update(carry)
        work_drawer.update(carry)

        order_1.check_if_fulfilled()

        glutSwapBuffers()  # needs to be called AFTER finished drawing
        glutMainLoopEvent()  # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
