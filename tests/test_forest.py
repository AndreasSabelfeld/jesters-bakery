from OpenGL.GLUT import *
from OpenGL.GL import *
import random

from src.render_engine.display_manager import DisplayManager
from src.render_engine.gui_renderer import GuiRenderer
from src.render_engine.master_renderer import MasterRenderer
from src.render_engine.loader import Loader
from src.obj_converter.obj_loader import OBJLoader
from src.render_engine.time import Time

from src.textures.model_texture import ModelTexture
from src.textures.terrain_texture import TerrainTexture
from src.textures.terrain_texture_pack import TerrainTexturePack

from src.models.textured_model import TexturedModel

from src.entities.entity import Entity
from src.entities.camera import Camera
from src.entities.light import Light
from src.entities.player import ThirdPersonPlayer

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster
from src.water.water_frame_buffers import WaterFrameBuffers
from src.water.water_renderer import WaterRenderer
from src.water.water_shader import WaterShader
from src.water.water_tile import WaterTile

from src.guis.gui_texture import GuiTexture


def main():
    # DISPLAY
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(173, 216, 230)
    # display.set_backdrop_color(20, 20, 20)
    # ------------

    # LOADERS
    loader = Loader()
    obj_loader = OBJLoader()
    # ------------

    # GRASS
    grass_model = obj_loader.load_obj_model("grassModel", loader)
    static_grass_model = TexturedModel(grass_model, ModelTexture(loader.load_texture("grassTexture")))
    static_grass_model.get_texture().set_reflectivity(0)
    static_grass_model.get_texture().set_has_transparency(True)
    static_grass_model.get_texture().set_use_fake_lighting(True)
    # ------------

    # PINES
    pine_model = obj_loader.load_obj_model("pine", loader)
    static_pine_model = TexturedModel(pine_model, ModelTexture(loader.load_texture("pine")))
    # ------------

    # FERN
    fern_model = obj_loader.load_obj_model("fern", loader)
    fern_texture_atlas = ModelTexture(loader.load_texture("fern"))
    fern_texture_atlas.set_number_of_rows(2)

    static_fern_model = TexturedModel(fern_model, fern_texture_atlas)
    static_fern_model.get_texture().set_reflectivity(0)
    static_fern_model.get_texture().set_has_transparency(True)
    static_fern_model.get_texture().set_use_fake_lighting(True)
    # -----------

    # TERRAIN
    background_texture = TerrainTexture(loader.load_texture("grass"))
    r_texture = TerrainTexture(loader.load_texture("mud"))
    g_texture = TerrainTexture(loader.load_texture("grassFlowers"))
    b_texture = TerrainTexture(loader.load_texture("grass"))

    texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
    blend_map = TerrainTexture(loader.load_texture("blendMap"))

    terrains = []
    terrain = Terrain(0, 0, loader, texture_pack, blend_map, "heightmap")
    terrains.append(terrain)
    # -----------

    entities = []

    for i in range(20):
        for j in range(20):
            for k in range(1):
                model = static_fern_model
                x = random.randint(0, 800)
                z = random.randint(0, 800)
                y = terrain.get_height_of_terrain(x, z)

                entity = Entity(model, [x, y, z], 0, 0, 0, 1, texture_index=random.randint(0, 4))
                entities.append(entity)

    for i in range(20):
        for j in range(20):
            for k in range(1):
                model = static_pine_model
                x = random.randint(0, 800)
                z = random.randint(0, 800)
                y = terrain.get_height_of_terrain(x, z)

                entity = Entity(model, [x, y, z], 0, 0, 0, 1, texture_index=random.randint(0, 4))
                entities.append(entity)

    sun = Light([100000, 150000, -100000], [1, 1, 1])
    lights = [sun]

    # PLAYER
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = ThirdPersonPlayer(static_bunny_model, [0, 0, 0], 0, 0, 0, 1)
    entities.append(player)
    camera = Camera(player)
    # ----------

    # RENDERER
    master_renderer = MasterRenderer(loader, camera)
    gui_renderer = GuiRenderer(loader)
    master_renderer.set_fog_density(0.001)
    master_renderer.set_fog_gradient(5)
    # ----------

    # ~~~~~~~~~WATER RENDERER~~~~~~~~~~~
    buffers = WaterFrameBuffers()
    water_shader = WaterShader()
    water_renderer = WaterRenderer(loader, water_shader, master_renderer.get_projection_matrix(), buffers)
    water = WaterTile(250, 250, -1, 250)
    waters = [water]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # GUI
    guis = []
    shadow_map = GuiTexture(master_renderer.get_shadow_map_texture(), [0.5, 0.5], [0.5, 0.5])
    # guis.append(shadow_map)
    # ----------

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        player.move()
        camera.move()

        if Terrain.get_existing_terrains().get((player.get_position()[0] // Terrain.get_size(),
                                                player.get_position()[2] // Terrain.get_size()), None) is None:
            terrains.append(Terrain(player.get_position()[0] // Terrain.get_size(),
                                player.get_position()[2] // Terrain.get_size(),
                                loader, texture_pack, blend_map, "heightmap"))

        master_renderer.render_shadow_map(entities, sun)
        glEnable(GL_CLIP_DISTANCE0)

        # render reflection texture
        buffers.bind_reflection_frame_buffer()
        distance = 2 * (camera.get_position()[1] - water.get_height())
        camera.get_position()[1] -= distance
        camera.invert_pitch()
        master_renderer.render_scene(entities, [], terrains, lights, camera, display, [0, 1, 0, -water.get_height()+1])
        camera.get_position()[1] += distance
        camera.invert_pitch()

        # render refraction texture
        buffers.bind_refraction_frame_buffer()
        master_renderer.render_scene(entities, [], terrains, lights, camera, display, [0, -1, 0, water.get_height()+1])

        glDisable(GL_CLIP_DISTANCE0)

        # render to screen
        buffers.unbind_current_frame_buffer()
        master_renderer.render_scene(entities, [], terrains, lights, camera, display)
        water_renderer.render(waters, camera, sun)

        gui_renderer.render(guis)

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == '__main__':
    main()
