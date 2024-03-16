from OpenGL.GLUT import *
from OpenGL.GL import *
import random

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
from src.entities.player import ThirdPersonPlayer

from src.water.water_tile import WaterTile
from src.water.water_renderer import WaterRenderer
from src.water.water_shader import WaterShader
from src.water.water_frame_buffers import WaterFrameBuffers

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster

from src.obj_converter.obj_loader import OBJLoader, NormalMappedOBJLoader

from src.font_rendering.text_master import TextMaster
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText

from src.particles.particle_master import ParticleMaster
from src.particles.simple_particle_system import SimpleParticleSystem
from src.particles.complex_particle_system import ComplexParticleSystem
from src.particles.particle_texture import ParticleTexture

from src.post_processing.fbo import FBO
from src.post_processing.post_processing import PostProcessing

from src.collision.sap import SAP
from src.collision.box import Box
from src.collision.detection import Detection


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

    # ~~~~~~~~~~~~PINES~~~~~~~~~~~~~~~~
    pine_model = obj_loader.load_obj_model("pine", loader)
    static_pine_model = TexturedModel(pine_model, ModelTexture(loader.load_texture("pine")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~ROCK~~~~~~~~~~~~~~~~
    rock_model = obj_loader.load_obj_model("rocks", loader)
    static_rock_model = TexturedModel(rock_model, ModelTexture(loader.load_texture("rocks")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~CHERRY TREE~~~~~~~~~~~
    cherry_tree = obj_loader.load_obj_model("cherry", loader)
    static_cherry_tree = TexturedModel(cherry_tree, ModelTexture(loader.load_texture("cherry")))
    static_cherry_tree.get_texture().set_has_transparency(True)
    static_cherry_tree.get_texture().set_shine_damper(10)
    static_cherry_tree.get_texture().set_reflectivity(0.5)
    static_cherry_tree.get_texture().set_specular_map(loader.load_texture("cherryS"))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~FERN~~~~~~~~~~~~~~~~
    fern_model = obj_loader.load_obj_model("fern", loader)
    fern_texture_atlas = ModelTexture(loader.load_texture("fern"))
    fern_texture_atlas.set_number_of_rows(2)

    static_fern_model = TexturedModel(fern_model, fern_texture_atlas)
    static_fern_model.get_texture().set_reflectivity(0)
    static_fern_model.get_texture().set_has_transparency(True)
    static_fern_model.get_texture().set_use_fake_lighting(True)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~CRATE~~~~~~~~~~~~~~~~
    crate_model = normal_mapped_obj_loader.load_obj_model("crate", loader)
    crate_texture = ModelTexture(loader.load_texture("crate"))
    crate_texture.set_shine_damper(10)
    crate_texture.set_reflectivity(0.5)
    crate_texture.set_normal_map(loader.load_texture("crateNormal"))
    static_crate_model = TexturedModel(crate_model, crate_texture)
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

    # ~~~~~~~~~~~~TERRAIN~~~~~~~~~~~~~~~
    background_texture = TerrainTexture(loader.load_texture("grass"))
    r_texture = TerrainTexture(loader.load_texture("mud"))
    g_texture = TerrainTexture(loader.load_texture("grassFlowers"))
    b_texture = TerrainTexture(loader.load_texture("grass"))

    texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
    blend_map = TerrainTexture(loader.load_texture("blendMap_island"))

    terrains = []
    Terrain.set_size(200)
    terrain = Terrain(0, 0, loader, texture_pack, blend_map, "heightmap_island")
    terrains.append(terrain)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~COLLIDERS~~~~~~~~~~~~~
    colliders = []

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~ENTITIES~~~~~~~~~~~~~
    entities = []
    boulder = Entity(static_boulder_model, [10, 0, 100], 0, 0, 0, 1)
    crate = Entity(static_crate_model, [10, 10, 50], 0, 0, 0, 0.1)
    normal_map_entities = [Entity(static_barrel_model, [100, 10, 100], 0, 0, 0, 1),
                           boulder,
                           crate]
    for i in range(9):
        model = static_fern_model
        x = random.randint(0, 200)
        z = random.randint(0, 200)
        y = terrain.get_height_of_terrain(x, z)

        entity = Entity(model, [x, y, z], 0, 0, 0, 1, texture_index=random.randint(0, 4))
        entities.append(entity)

    for i in range(6):
        model = static_pine_model
        x = random.randint(10, 50)
        z = random.randint(10, 200)
        y = terrain.get_height_of_terrain(x, z)

        entity = Entity(model, [x, y, z], 0, 0, 0, 1, texture_index=random.randint(0, 4))
        colliders.append(Box(*Box.calculate_points([x, y, z], 4)))
        entities.append(entity)

    entities.append(Entity(static_rock_model, [100, 4.549, 100], 0, 0, 0, 100))
    entities.append(Entity(static_cherry_tree, [150, 0, 40], 0, 0, 0, 10))
    colliders.append(Box(*Box.calculate_points([150, 0, 40], 2)))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([100000, 150000, -100000], [1, 1, 1])
    lights = [sun]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = ThirdPersonPlayer(static_bunny_model, [0, 0, 0], 0, 0, 0, 1)
    player_collider = Box(*Box.calculate_points([0, 0, 0], 1))
    entities.append(player)
    camera = Camera(player)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~RENDERER~~~~~~~~~~~~~~~
    # ShaderProgram.set_is_cel(True)
    master_renderer = MasterRenderer(loader, camera)
    master_renderer.set_fog_density(0.0035)
    master_renderer.set_fog_gradient(5)
    master_renderer.get_shadow_map_texture()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~PARTICLES~~~~~~~~~~~~~~
    particle_master = ParticleMaster(loader, master_renderer.get_projection_matrix())

    smoke_texture = ParticleTexture(loader.load_texture("particleAtlas"), 4, True)
    fire = ComplexParticleSystem(smoke_texture, 100, 10, 0.1, 1, 2)
    fire.randomize_rotation()
    fire.set_direction([0, 10, 0], 0.2)
    fire.set_life_error(0.1)
    fire.set_speed_error(0.4)
    fire.set_scale_error(0.8)

    smoke_texture = ParticleTexture(loader.load_texture("smoke"), 4, False)
    smoke = ComplexParticleSystem(smoke_texture, 100, 5, -0.3, 10, 15)
    smoke.randomize_rotation()
    smoke.set_direction([0, 10, 0], 0.5)
    smoke.set_life_error(0.1)
    smoke.set_speed_error(0.4)
    smoke.set_scale_error(0.8)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~WATER RENDERER~~~~~~~~~~~
    buffers = WaterFrameBuffers()
    water_shader = WaterShader()
    water_renderer = WaterRenderer(loader, water_shader, master_renderer.get_projection_matrix(), buffers)
    water = WaterTile(100, 100, 0, 70)
    waters = [water]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~MOUSE PICKER~~~~~~~~~~~~
    picker = TerrainRaycaster(camera, master_renderer.get_projection_matrix())
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~POST PROCESSING~~~~~~~~~~
    multisample_fbo = FBO(DisplayManager.get_width(), DisplayManager.get_height(), True)
    output_fbo0 = FBO(DisplayManager.get_width(), DisplayManager.get_height(), False, FBO.DEPTH_TEXTURE)
    output_fbo1 = FBO(DisplayManager.get_width(), DisplayManager.get_height(), False, FBO.DEPTH_TEXTURE)
    post_processor = PostProcessing(loader)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~SAP~~~~~~~~~~~~~~~~~
    SAP.batch_insertion(colliders)
    SAP.add_box(player_collider)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        fps = 1 / Time.get_delta_time()

        # for entity in normal_map_entities:
        #     entity.increase_rotation(0, 1, 0)

        last_player_pos = player.get_position()
        player.move([crate, boulder])
        # SAP.update_object(player_collider, *Box.calculate_points(player.get_position(), 4))
        # colliding_pairs = SAP.get_colliding_pairs()
        # colliding_boxes = SAP.get_colliding_boxes(player_collider)
        # text1.set_text_string(str(collision_detection.detect_object(player, boulder)))
        text2.set_text_string(str(['%.2f' % elem for elem in player.get_position()]))
        text3.set_text_string(str('%.2f' % fps))
        # if colliding_pairs:
        #     player.set_position(last_player_pos)

        camera.move()
        picker.update()
        # print(picker.get_current_terrain_point())

        particle_master.update(camera)
        fire.emit_particle([10, 7, 10])
        smoke.emit_particle([30, 15, 60])

        master_renderer.render_shadow_map(entities, sun)
        glEnable(GL_CLIP_DISTANCE0)

        # render reflection texture
        buffers.bind_reflection_frame_buffer()
        distance = 2 * (camera.get_position()[1] - water.get_height())
        camera.get_position()[1] -= distance
        camera.invert_pitch()
        master_renderer.render_scene(entities, normal_map_entities, terrains, lights, camera, display, [0, 1, 0, -water.get_height()+1])
        camera.get_position()[1] += distance
        camera.invert_pitch()

        # render refraction texture
        buffers.bind_refraction_frame_buffer()
        master_renderer.render_scene(entities, normal_map_entities, terrains, lights, camera, display, [0, -1, 0, water.get_height()+1])

        glDisable(GL_CLIP_DISTANCE0)

        # render to screen
        buffers.unbind_current_frame_buffer()

        multisample_fbo.bind_frame_buffer()

        master_renderer.render_scene(entities, normal_map_entities, terrains, lights, camera, display)
        water_renderer.render(waters, camera, sun)

        particle_master.render_particles(camera)  # after 3D stuff, before GUI
        multisample_fbo.unbind_frame_buffer()
        # multisample_fbo.resolve_to_fbo(output_fbo0, GL_COLOR_ATTACHMENT0)
        # multisample_fbo.resolve_to_fbo(output_fbo1, GL_COLOR_ATTACHMENT1)
        # post_processor.do_post_processing(output_fbo0.get_color_texture(), output_fbo1.get_color_texture())
        multisample_fbo.resolve_to_screen()

        TextMaster.render()

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()

    """
    multisample_fbo.clean_up()
    output_fbo0.clean_up()
    output_fbo1.clean_up()
    TextMaster.clean_up()
    buffers.clean_up()
    water_shader.clean_up()
    particle_master.clean_up()
    master_renderer.clean_up()
    """


if __name__ == "__main__":
    main()
