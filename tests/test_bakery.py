from OpenGL.GLUT import *
from OpenGL.GL import *
import random

from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.fridge import Fridge
from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.loader import Loader
from src.render_engine.time import Time
from src.render_engine.input_controller import KeyboardInput, KeyboardInputListener, ControllerInput

from src.textures.model_texture import ModelTexture
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack

from src.models.textured_model import TexturedModel

from src.entities.entity import Entity
from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import ThirdPersonPlayer, FirstPersonPlayer

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster, ObjectRaycaster

from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader

from src.font_rendering.text_master import TextMaster
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText

from src.post_processing.fbo import FBO
from src.post_processing.image_renderer import ImageRenderer

from src.collision.sap import SAP
from src.collision.box import Box
from src.collision.detection import Detection

from src.game_mechanics.pick_up import Carry
from src.game_mechanics.coffee_machine_os import CoffeeMachineOS
from src.game_mechanics.coffee_product import CoffeeProduct
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.fridge_object import FridgeObject


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
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~CRATE~~~~~~~~~~~~~~~~
    crate_model = normal_mapped_obj_loader.load_obj_model("crate", loader)
    crate_texture = ModelTexture(loader.load_texture("crate"))
    crate_texture.set_shine_damper(10)
    crate_texture.set_reflectivity(0.5)
    crate_texture.set_normal_map(loader.load_texture("crateNormal"))
    static_crate_model = TexturedModel(crate_model, crate_texture)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~GRASSBLOCK~~~~~~~~~~~~~~~~
    grass_model = obj_loader.load_obj_model("cube", loader)
    grass_texture = ModelTexture(loader.load_texture("grass_block"))
    grass_texture.set_shine_damper(10)
    grass_texture.set_reflectivity(0.5)
    static_grass_model = TexturedModel(grass_model, grass_texture)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~BOULDER~~~~~~~~~~~~~~
    boulder_model = normal_mapped_obj_loader.load_obj_model("boulder", loader)
    boulder_texture = ModelTexture(loader.load_texture("boulder"))
    boulder_texture.set_shine_damper(10)
    boulder_texture.set_reflectivity(0.5)
    boulder_texture.set_normal_map(loader.load_texture("boulderNormal"))
    static_boulder_model = TexturedModel(boulder_model, boulder_texture)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~BARREL~~~~~~~~~~~~~~~
    barrel_model = normal_mapped_obj_loader.load_obj_model("barrel", loader)
    barrel_texture = ModelTexture(loader.load_texture("barrel"))
    barrel_texture.set_shine_damper(10)
    barrel_texture.set_reflectivity(0.5)
    barrel_texture.set_normal_map(loader.load_texture("barrelNormal"))
    barrel_texture.set_specular_map(loader.load_texture("barrelS"))
    static_barrel_model = TexturedModel(barrel_model, barrel_texture)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~COFFEE MACHINE~~~~~~~~~~~
    coffee_machine_model = obj_loader.load_obj_model("coffee_machine", loader)
    coffee_machine_texture = ModelTexture(loader.load_texture("coffee_machine_texture"))
    coffee_machine_texture.set_shine_damper(10)
    coffee_machine_texture.set_reflectivity(0.5)
    static_coffee_machine_model = TexturedModel(coffee_machine_model, coffee_machine_texture)
    static_coffee_machine_collider = TexturedModel(obj_loader.load_obj_model("coffee_machine_collider", loader),
                                                 ModelTexture(loader.load_texture("")))

    coffee_machine_screen_model = obj_loader.load_obj_model("coffee_machine_screen", loader)
    coffee_machine_screen_texture = ModelTexture(loader.load_texture("white"))
    coffee_machine_screen_texture.set_shine_damper(10)
    coffee_machine_screen_texture.set_reflectivity(0.5)
    static_coffee_machine_screen_model = TexturedModel(coffee_machine_screen_model, coffee_machine_screen_texture)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~FRIDGE~~~~~~~~~~~~~~~
    fridge_case_model = obj_loader.load_obj_model("fridge_case", loader)
    fridge_case_texture = ModelTexture(loader.load_texture("counter"))
    fridge_case_texture.set_shine_damper(10)
    fridge_case_texture.set_reflectivity(0.5)
    static_fridge_case_model = TexturedModel(fridge_case_model, fridge_case_texture)
    static_fridge_case_collider = TexturedModel(obj_loader.load_obj_model("case_collider", loader), ModelTexture(loader.load_texture("")))

    fridge_top_drawer_model = obj_loader.load_obj_model("fridge_top_drawer", loader)
    fridge_top_drawer_texture = ModelTexture(loader.load_texture("drawer"))
    fridge_top_drawer_texture.set_shine_damper(10)
    fridge_top_drawer_texture.set_reflectivity(0.5)
    static_fridge_top_drawer_model = TexturedModel(fridge_top_drawer_model, fridge_top_drawer_texture)
    static_fridge_top_drawer_collider = TexturedModel(obj_loader.load_obj_model("top_drawer_collider", loader), ModelTexture(loader.load_texture("")))

    fridge_bottom_drawer_model = obj_loader.load_obj_model("fridge_bottom_drawer", loader)
    fridge_bottom_drawer_texture = ModelTexture(loader.load_texture("drawer"))
    fridge_bottom_drawer_texture.set_shine_damper(10)
    fridge_bottom_drawer_texture.set_reflectivity(0.5)
    static_fridge_bottom_drawer_model = TexturedModel(fridge_bottom_drawer_model, fridge_bottom_drawer_texture)
    static_fridge_bottom_drawer_collider = TexturedModel(obj_loader.load_obj_model("bottom_drawer_collider", loader), ModelTexture(loader.load_texture("")))

    fridge_bottom_grid_model = obj_loader.load_obj_model("fridge_bottom_grid", loader)
    fridge_bottom_grid_texture = ModelTexture(loader.load_texture("grass"))
    fridge_bottom_grid_texture.set_shine_damper(10)
    fridge_bottom_grid_texture.set_reflectivity(0)
    static_fridge_bottom_grid_model = TexturedModel(fridge_bottom_grid_model, fridge_bottom_grid_texture)

    fridge_top_grid_model = obj_loader.load_obj_model("fridge_top_grid", loader)
    fridge_top_grid_texture = ModelTexture(loader.load_texture("grass"))
    fridge_top_grid_texture.set_shine_damper(10)
    fridge_top_grid_texture.set_reflectivity(0)
    static_fridge_top_grid_model = TexturedModel(fridge_top_grid_model, fridge_top_grid_texture)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~COFFEE CUPS~~~~~~~~~~~~~
    small_coffee_model = obj_loader.load_obj_model("small_coffee_cup", loader)
    small_coffee_texture = ModelTexture(loader.load_texture("coffee_cup_texture"))
    small_coffee_texture.set_shine_damper(10)
    small_coffee_texture.set_reflectivity(0.5)
    static_small_coffee_model = TexturedModel(small_coffee_model, small_coffee_texture)
    static_small_coffee_collider = TexturedModel(obj_loader.load_obj_model("small_coffee_cup_collider", loader), ModelTexture(loader.load_texture("")))

    big_coffee_model = obj_loader.load_obj_model("big_coffee_cup", loader)
    static_big_coffee_model = TexturedModel(big_coffee_model, small_coffee_texture)
    static_big_coffee_collider = TexturedModel(obj_loader.load_obj_model("big_coffee_cup_collider", loader), ModelTexture(loader.load_texture("")))

    tea_pot_model = obj_loader.load_obj_model("tea_pot", loader)
    static_tea_pot_model = TexturedModel(tea_pot_model, small_coffee_texture)
    tea_pot_lid_model = obj_loader.load_obj_model("tea_pot_lid", loader)
    static_tea_pot_lid_model = TexturedModel(tea_pot_lid_model, small_coffee_texture)
    static_tea_pot_collider = TexturedModel(obj_loader.load_obj_model("tea_pot_collider", loader), ModelTexture(loader.load_texture("")))

    small_glass_model = obj_loader.load_obj_model("small_glass", loader)
    static_small_glass_model = TexturedModel(small_glass_model, small_coffee_texture)
    static_small_glass_collider = TexturedModel(obj_loader.load_obj_model("small_glass_collider", loader), ModelTexture(loader.load_texture("")))

    big_glass_model = obj_loader.load_obj_model("big_glass", loader)
    static_big_glass_model = TexturedModel(big_glass_model, small_coffee_texture)
    static_big_glass_collider = TexturedModel(obj_loader.load_obj_model("big_glass_collider", loader), ModelTexture(loader.load_texture("")))

    espresso_model = obj_loader.load_obj_model("espresso_cup", loader)
    static_espresso_model = TexturedModel(espresso_model, small_coffee_texture)
    static_espresso_collider = TexturedModel(obj_loader.load_obj_model("espresso_cup_collider", loader), ModelTexture(loader.load_texture("")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~BEVERAGES~~~~~~~~~~~~
    milk_sac_model = obj_loader.load_obj_model("milk_sac", loader)
    static_milk_sac_model = TexturedModel(milk_sac_model, small_coffee_texture)
    static_milk_sac_collider = TexturedModel(obj_loader.load_obj_model("milk_sac_collider", loader), ModelTexture(loader.load_texture("")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~TERRAIN~~~~~~~~~~~~~~~
    background_texture = TerrainTexture(loader.load_texture("grass"))
    r_texture = TerrainTexture(loader.load_texture("mud"))
    g_texture = TerrainTexture(loader.load_texture("grassFlowers"))
    b_texture = TerrainTexture(loader.load_texture("grass"))

    texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
    blend_map = TerrainTexture(loader.load_texture("black"))

    terrains = []
    Terrain.set_size(200)
    terrain = Terrain(0, 0, loader, texture_pack, blend_map, "white")
    terrains.append(terrain)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~COLLIDERS~~~~~~~~~~~~~
    colliders = []

    # ~~~~~~~~~~~~~ENTITIES~~~~~~~~~~~~~
    grass_block = Entity(static_grass_model, [50, 27.39, 50], 0, 0, 0, 1)
    crate = Entity(static_crate_model, [80, 35, 50], 0, 0, 0, 0.01)
    boulder = Entity(static_boulder_model, [80, 27.39, 70], 0, 0, 0, 0.1)
    barrel = Entity(static_barrel_model, [80, 27.39, 90], 0, 0, 0, 1)

    machine_size = 1.75
    coffee_machine = Entity(static_coffee_machine_model, [70, 29.39, 50], 0, 0, 0, machine_size)
    coffee_machine_collider = Entity(static_coffee_machine_collider, [70, 29.39, 50], 0, 0, 0, machine_size)
    coffee_machine_screen = Entity(static_coffee_machine_screen_model, [70, 29.39, 50], 0, 0, 0, machine_size)
    coffee_machine_game_object = GameObject(coffee_machine, coffee_machine_screen, name=CoffeeMachineOS.get_name(),
                                            collider=coffee_machine_collider)
    coffee_machine_game_object.set_pickup_able(False)

    fridge_case = Entity(static_fridge_case_model, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_case_collider = Entity(static_fridge_case_collider, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_top_drawer = Entity(static_fridge_top_drawer_model, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_top_drawer_collider = Entity(static_fridge_top_drawer_collider, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_bottom_drawer = Entity(static_fridge_bottom_drawer_model, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_bottom_drawer_collider = Entity(static_fridge_bottom_drawer_collider, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_bottom_grid = Entity(static_fridge_bottom_grid_model, [60, 29.39, 50], 0, 0, 0, machine_size)
    fridge_top_grid = Entity(static_fridge_top_grid_model, [60, 29.39, 50], 0, 0, 0, machine_size)

    fridge_game_object = GameObject(fridge_case, child_0=fridge_top_drawer, child_1=fridge_bottom_drawer, collider=fridge_case_collider)
    fridge_game_object.set_pickup_able(False)
    fridge_game_object.get_child_0().set_collider(fridge_top_drawer_collider)
    fridge_game_object.get_child_1().set_collider(fridge_bottom_drawer_collider)
    fridge_game_object.get_child_0().set_name("TOP_DRAWER")
    fridge_game_object.get_child_1().set_name("BOTTOM_DRAWER")
    # fridge_game_object.get_child_0().set_child_0(fridge_top_grid)
    # fridge_game_object.get_child_1().set_child_0(fridge_bottom_grid)

    small_coffee = Entity(static_small_coffee_model, [70 + 2, 29.39, 50], 0, 0, 0, 1)
    small_coffee_collider = Entity(static_small_coffee_collider, [70 + 2, 29.39, 50], 0, 0, 0, 1)
    small_coffee_game_object = GameObject(small_coffee, name="COFFEE", collider=small_coffee_collider)
    small_coffee_game_object.set_attachment(CoffeeContainer(CoffeeContainer.COFFEE_CUP, small_coffee_game_object))

    big_coffee = Entity(static_big_coffee_model, [70 + 4, 29.39, 50], 0, 0, 0, 1)
    big_coffee_collider = Entity(static_big_coffee_collider, [70 + 4, 29.39, 50], 0, 0, 0, 1)
    big_coffee_game_object = GameObject(big_coffee, name="COFFEE", collider=big_coffee_collider)
    big_coffee_game_object.set_attachment(CoffeeContainer(CoffeeContainer.CAPPUCCINO_CUP, big_coffee_game_object))

    tea_pot = Entity(static_tea_pot_model, [70 + 6, 29.39, 50], 0, 0, 0, 1)
    tea_pot_lid = Entity(static_tea_pot_lid_model, [70 + 6, 29.39, 50], 0, 0, 0, 1)
    tea_pot_collider = Entity(static_tea_pot_collider, [70 + 6, 29.39, 50], 0, 0, 0, 1)
    tea_pot_game_object = GameObject(tea_pot, tea_pot_lid, name="TEA", collider=tea_pot_collider)
    tea_pot_game_object.set_attachment(CoffeeContainer(CoffeeContainer.TEA_POT, tea_pot_game_object))

    small_glass = Entity(static_small_glass_model, [70 + 8, 29.39, 50], 0, 0, 0, 1)
    small_glass_collider = Entity(static_small_glass_collider, [70 + 8, 29.39, 50], 0, 0, 0, 1)
    small_glass_game_object = GameObject(small_glass, name="COFFEE", collider=small_glass_collider)
    small_glass_game_object.set_attachment(CoffeeContainer(CoffeeContainer.SMALL_GLASS, small_glass_game_object))

    big_glass = Entity(static_big_glass_model, [70 + 10, 29.39, 50], 0, 0, 0, 1)
    big_glass_collider = Entity(static_big_glass_collider, [70 + 10, 29.39, 50], 0, 0, 0, 1)
    big_glass_game_object = GameObject(big_glass, name="COFFEE", collider=big_glass_collider)
    big_glass_game_object.set_attachment(CoffeeContainer(CoffeeContainer.BIG_GLASS, big_glass_game_object))

    espresso_cup = Entity(static_espresso_model, [70 + 12, 29.39, 50], 0, 0, 0, 1)
    espresso_cup_collider = Entity(static_espresso_collider, [70 + 12, 29.39, 50], 0, 0, 0, 1)
    espresso_cup_game_object = GameObject(espresso_cup, name="COFFEE", collider=espresso_cup_collider)
    espresso_cup_game_object.set_attachment(CoffeeContainer(CoffeeContainer.ESPRESSO_CUP, espresso_cup_game_object))

    cauldron = Entity(static_small_glass_model, [70 + 8, 29.39, 50], 0, 0, 0, 3)
    cauldron_collider = Entity(static_small_glass_collider, [70 + 8, 29.39, 50], 0, 0, 0, 3)
    cauldron_game_object = GameObject(cauldron, name="FRIDGE", collider=cauldron_collider)
    cauldron_game_object.set_attachment(FridgeObject((2, 2), cauldron))

    milk_sac = Entity(static_milk_sac_model, [70 + 14, 29.39, 50], 0, 0, 0, machine_size)
    milk_sac_collider = Entity(static_milk_sac_collider, [70 + 14, 29.39, 50], 0, 0, 0, machine_size)
    milk_sac_game_object = GameObject(milk_sac, name="FRIDGE", collider=milk_sac_collider)
    milk_sac_game_object.set_attachment(FridgeObject((3, 2), milk_sac))

    entities = [coffee_machine_game_object, small_coffee_game_object, big_coffee_game_object, tea_pot_game_object,
                small_glass_game_object, big_glass_game_object, espresso_cup_game_object, fridge_game_object,
                cauldron_game_object, milk_sac_game_object]
    collider_entities = entities.copy()
    collider_entities.extend([fridge_game_object.get_child_0(), fridge_game_object.get_child_1()])
    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([-100000, -150000, -100000], [1, 1, 1])
    lights = [sun]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [60, 0, 40], 0, 0, 0, 3)
    player.set_player_size(12)
    entities.append(player)
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

    fbo = FBO(1920, 1080, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)

    # ~~~~~~~~~~~~~GAME~~~~~~~~~~~~~~~~~
    carry = Carry(terrain_picker, object_picker, coffee_machine_game_object)
    carry.movable_entities = collider_entities
    coffee_os = CoffeeMachineOS(coffee_machine_screen, loader, obj_loader, fbo, gui_renderer, object_picker)
    coffee_machine_game_object.set_attachment(coffee_os)
    fridge = Fridge(fridge_game_object.get_child_0(), fridge_game_object.get_child_1(), object_picker, loader, gui_renderer)
    fridge_game_object.get_child_0().set_attachment(fridge)
    fridge_game_object.get_child_1().set_attachment(fridge)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~KEYBOARD LISTENERS~~~~~~~~~
    listener_c = KeyboardInputListener()
    listener_f = KeyboardInputListener()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    cube = Entity(static_grass_model, [60, 29.39, 50], 0, 0, 0, 0.1)
    entities.append(cube)

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        fps = 1 / Time.get_delta_time()

        player.move(collider_entities)
        text2.set_text_string(str(['%.2f' % elem for elem in cube.get_position()]))
        if not (coffee_os.get_is_interacting() or fridge.get_is_interacting()):
            camera.move()
            carry.update()
        else:
            carry.update(False)

        object_picker.update(collider_entities)
        if KeyboardInput.get_keys_held().get(b'c'):
            ent = Entity(static_grass_model, object_picker.get_current_object_point(), 0, 0, 0, 0.1)
            entities.append(ent)

        master_renderer.render_shadow_map(entities, sun)

        coffee_os.interact(player, camera, listener_c)
        fridge.interact(player, camera, listener_f)
        coffee_os.render_screen()

        master_renderer.render_scene(entities, [], terrains, lights, camera, display)
        TextMaster.render_not_specified(coffee_os.get_all_texts())
        fridge.update(carry)

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
