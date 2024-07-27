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
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [60, 0, 40], 0, 0, 0, 3)
    player.set_player_size(12)
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
    collider_entities = []

    grass_texture = ModelTexture(loader.load_texture("grass_block"))
    textures = [ModelTexture(loader.load_texture("pngs/cups/coke_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/schorle_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/water_filling_tex")),
                ModelTexture(loader.load_texture("pngs/cups/beer_filling_tex"))]

    machine_size = 1.75
    food_size = 0.5
    mixer_size = 0.5
    coffee_machine_game_object = prefabs.coffee_machine([50, 10, 50], [0, 0, 0], machine_size, loader, obj_loader,
                                                        gui_renderer, object_picker)
    coffee_machine_lactose_free_game_object = prefabs.lactose_free_coffee_machine([46, 10, 50], [0, 0, 0], machine_size,
                                                                                  loader, obj_loader,
                                                                                  gui_renderer, object_picker)
    fridge_game_object = prefabs.fridge([40, 10, 50], [0, 0, 0], machine_size, loader, obj_loader,
                                        gui_renderer, object_picker)
    milk_foamer_game_object = prefabs.milk_foamer([56, 10, 50], [0, 0, 0], 1, loader, obj_loader,
                                                  gui_renderer, object_picker)
    milk_foamer_screen = milk_foamer_game_object.get_attachment().get_render_target()
    mixer_game_object = prefabs.mixer([58, 10, 50], [0, 0, 0], mixer_size, loader, obj_loader)
    mixer_vessel_game_object = prefabs.mixer_vessel([60, 10, 50], [0, 0, 0], mixer_size, loader, obj_loader)
    tap = Tap(obj_loader, loader, [62, 12, 50], [0, 0, 0], 1, textures)
    counter_game_object = prefabs.finished_counter([66, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    ice_machine_door = prefabs.ice_machine([66, 10, 50], [0, 0, 0], 1, loader, obj_loader, entities, collider_entities)
    finished_col = prefabs.finished_collider([66, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    print("finished loading machines")

    for i in range(5):
        small_coffee_game_object = prefabs.coffee_cup([50, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        big_coffee_game_object = prefabs.cappuccino_cup([52, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        tea_pot_game_object = prefabs.tea([54, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        small_glass_game_object = prefabs.small_glass([56, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        big_glass_game_object = prefabs.big_glass([58, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        espresso_cup_game_object = prefabs.espresso_cup([60, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        plate_game_object = prefabs.plate([62, 10, 60 + i], [0, 0, 0], 0.5, loader, obj_loader)
        beer_game_object = prefabs.beer([64, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        prosecco_game_object = prefabs.prosecco_glass([66, 10, 60 + i], [0, 0, 0], 1, loader, obj_loader)
        print(f"round {i}")

        entities.extend([small_coffee_game_object, big_coffee_game_object, tea_pot_game_object, small_glass_game_object,
                         big_glass_game_object, espresso_cup_game_object, plate_game_object, beer_game_object,
                         prosecco_game_object])

    print("finished loading vessels")

    coke_zero = prefabs.coke_zero([72, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    sprite = prefabs.sprite([74, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    orange_juice = prefabs.orange_juice([76, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    topfit_juice = prefabs.topfit_juice([78, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    prosecco_bottle = prefabs.prosecco_bottle([80, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    chai_bottle = prefabs.chai_bottle([82, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    ovomaltine = prefabs.ovomaltine([84, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    caotina = prefabs.caotina([86, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    chocolatl = prefabs.chocolatl([88, 10, 50], [0, 0, 0], 1, loader, obj_loader)

    milk_sac_game_object = prefabs.milk_sac([80, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    lactose_free_milk = prefabs.lactose_free_milk([82, 10, 50], [0, 0, 0], 1, loader, obj_loader)
    oat_milk = prefabs.oat_milk([84, 10, 50], [0, 0, 0], 1, loader, obj_loader)

    prefabs.ham_sandwich([50, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.egg_sandwich([52, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.tuna_sandwich([54, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.mango_chutney_sandwich([56, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.tomato_sandwich([58, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.silserli([60, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.croissant([62, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.chocolate_croissant([64, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.almond_croissant([66, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.strawberry_tart([68, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.cookie([70, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.spitzbub([72, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.linzerli([74, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.carac([76, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.wurstwegge([78, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.schinkengipfel([80, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.chocolate_cake([82, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.passionfruit_cake([84, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.carrot_cake([86, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.citron_cake([88, 10, 70], [0, 0, 0], food_size, loader, obj_loader, entities, collider_entities)
    prefabs.lemons([90, 10, 70], [0, 0, 0], 1, loader, obj_loader, entities, collider_entities)

    print("finished loading food")

    entities.extend([coffee_machine_game_object, fridge_game_object, milk_sac_game_object, milk_foamer_game_object,
                     milk_foamer_screen, mixer_game_object, mixer_vessel_game_object,
                     coffee_machine_lactose_free_game_object, counter_game_object, *tap.get_game_objects(),
                     prosecco_bottle, chai_bottle, coke_zero, sprite, orange_juice, topfit_juice, lactose_free_milk,
                     oat_milk, ovomaltine, caotina, chocolatl, ice_machine_door])
    collider_entities.extend(entities.copy())
    collider_entities.extend([fridge_game_object.get_child_0(), fridge_game_object.get_child_1(),
                              milk_foamer_game_object.get_child_0(), milk_foamer_game_object.get_child_1(),
                              counter_game_object, finished_col])
    print("finished loading assets")
    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([100000, 150000, -100000], [1, 1, 1])
    player_light = Light([0, 0, 0], [1, 1, 1], [1, 0.001, 0.0002])
    lights = [player_light]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~GAME~~~~~~~~~~~~~~~~~
    carry = Carry(terrain_picker, object_picker, coffee_machine_game_object, coffee_machine_lactose_free_game_object)
    carry.movable_entities = collider_entities

    scanner = Scanner(object_picker, loader)
    coffee_os = coffee_machine_game_object.get_attachment()
    coffee_os_lactose_free = coffee_machine_lactose_free_game_object.get_attachment()
    fridge = fridge_game_object.get_child_0().get_attachment()
    milk_foamer_os = milk_foamer_game_object.get_attachment()
    mixer_vessel_os = mixer_vessel_game_object.get_attachment()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    master_order = MasterOrder(loader, obj_loader, gui_renderer, counter_game_object)
    finished_col.set_attachment(master_order)
    order_1 = Order(master_order, 4)
    order_1.get_gui_text()
    order_1_ga = order_1.get_game_object([40, 10, 55], [0, 0, 0], 10)
    entities.append(order_1_ga)
    collider_entities.append(order_1_ga)

    cube_model = obj_loader.load_obj_model("objs/legacy/cube", loader)
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

        text1.set_text_string(str(order_1.get_all_contents()))
        text2.set_text_string(str(order_1.calculate_points()))
        text3.set_text_string(str(order_1.get_time()))
        if not (coffee_os.get_is_interacting() or coffee_os_lactose_free.get_is_interacting() or fridge.get_is_interacting()):
            camera.move()
            carry.update()
        else:
            carry.update(False)

        object_picker.update(collider_entities)
        scanner.update(collider_entities)

        if KeyboardInput.on_key_down(b'f'):
            entities.append(Entity(static_cube_model, object_picker.get_current_object_point(), 0, 0, 0, 0.1))
            print(object_picker.get_current_object_point())

        master_renderer.render_shadow_map(entities, player_light)

        coffee_os.interact(player, camera)
        coffee_os_lactose_free.interact(player, camera)
        fridge.interact(player, camera)
        coffee_os.render_screen()
        coffee_os_lactose_free.render_screen()
        milk_foamer_os.update()
        tap.update()
        mixer_vessel_os.update()

        master_renderer.render_scene(entities, [], terrains, lights, camera, display)
        not_specified = coffee_os.get_all_texts()
        not_specified.extend(coffee_os_lactose_free.get_all_texts())
        not_specified.append(milk_foamer_os.get_text())
        TextMaster.render_not_specified(not_specified)
        fridge.update(carry)

        order_1.check_if_fulfilled()

        glutSwapBuffers()  # needs to be called AFTER finished drawing
        glutMainLoopEvent()  # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
