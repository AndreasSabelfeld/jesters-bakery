from OpenGL.GLUT import *
from OpenGL.GL import *
import random

from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.loader import Loader
from src.render_engine.time import Time
from src.render_engine.input_controller import KeyboardInput, ControllerInput

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

    coffee_machine_screen_model = obj_loader.load_obj_model("coffee_machine_screen", loader)
    coffee_machine_screen_texture = ModelTexture(loader.load_texture("white"))
    coffee_machine_screen_texture.set_shine_damper(10)
    coffee_machine_screen_texture.set_reflectivity(0.5)
    static_coffee_machine_screen_model = TexturedModel(coffee_machine_screen_model, coffee_machine_screen_texture)
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
    coffee_machine = Entity(static_coffee_machine_model, [70, 27.39, 50], 0, 0, 0, 1)
    coffee_machine_screen = Entity(static_coffee_machine_screen_model, [70, 27.39, 50], 0, 0, 0, 1)
    entities = [grass_block, crate, boulder, coffee_machine, coffee_machine_screen]
    collider_entities = entities.copy()

    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([-100000, -150000, -100000], [1, 1, 1])
    lights = [sun]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = FirstPersonPlayer(static_bunny_model, [60, 0, 40], 0, 0, 0, 1)
    entities.append(player)
    camera = Camera(player)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~RENDERER~~~~~~~~~~~~~~~
    master_renderer = MasterRenderer(loader, camera)
    master_renderer.set_fog_density(0.0035)
    master_renderer.set_fog_gradient(5)
    master_renderer.get_shadow_map_texture()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~MOUSE PICKER~~~~~~~~~~~~
    terrain_picker = TerrainRaycaster(camera, master_renderer.get_projection_matrix())
    object_picker = ObjectRaycaster(camera, master_renderer.get_projection_matrix())
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~GAME~~~~~~~~~~~~~~~~~
    carry = Carry(terrain_picker, object_picker)
    os = CoffeeMachineOS(coffee_machine_screen, [])
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    fbo = FBO(1920, 1080, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        fps = 1 / Time.get_delta_time()

        player.move(collider_entities)
        text2.set_text_string(str(['%.2f' % elem for elem in player.get_position()]))
        text3.set_text_string(str('%.2f' % fps))
        if not os.get_is_interacting():
            camera.move()
        carry.movable_entities = collider_entities
        carry.update()

        master_renderer.render_shadow_map(entities, sun)

        fbo.bind_frame_buffer()
        master_renderer.render_scene(entities, [], terrains, lights, camera, display)
        TextMaster.render()
        fbo.unbind_frame_buffer()

        os.check_for_interaction(player, camera)
        coffee_machine_screen.get_model().set_texture(ModelTexture(fbo.get_color_texture()))

        master_renderer.render_scene(entities, [], terrains, lights, camera, display)
        TextMaster.render()

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
