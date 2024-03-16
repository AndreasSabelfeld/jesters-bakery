from OpenGL.GLUT import *
import random

from src.render_engine.display_manager import DisplayManager
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

from src.shaders.shader_program import ShaderProgram

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster


def main():
    # ~~~~~~~~~~~~DISPLAY~~~~~~~~~~~~~~
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(255, 102, 204)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~LOADERS~~~~~~~~~~~~~~
    loader = Loader()
    obj_loader = OBJLoader()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~BOBBLE TREE~~~~~~~~~~~~
    tree_model = obj_loader.load_obj_model("bobbleTree", loader)
    static_tree_model = TexturedModel(tree_model, ModelTexture(loader.load_texture("bobbleTree")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~TOON ROCK~~~~~~~~~~~~~~
    rock_model = obj_loader.load_obj_model("toonRocks", loader)
    static_rock_model = TexturedModel(rock_model, ModelTexture(loader.load_texture("toonRocks")))
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~TERRAIN~~~~~~~~~~~~~~~~
    background_texture = TerrainTexture(loader.load_texture("light_yellow"))
    r_texture = TerrainTexture(loader.load_texture("light_green"))
    g_texture = TerrainTexture(loader.load_texture("light_green"))
    b_texture = TerrainTexture(loader.load_texture("white"))

    texture_pack = TerrainTexturePack(background_texture, r_texture, g_texture, b_texture)
    blend_map = TerrainTexture(loader.load_texture("blendMap_island"))

    terrains = []
    terrain = Terrain(0, 0, loader, texture_pack, blend_map, "heightmap")
    terrains.append(terrain)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~ENTITIES~~~~~~~~~~~~~
    entities = []
    for i in range(200):
        model = static_tree_model
        x = random.randint(0, 800)
        z = random.randint(0, 800)
        y = terrain.get_height_of_terrain(x, z)

        entity = Entity(model, [x, y, z], 0, random.randint(0, 360), 0, random.random()+0.3)
        entities.append(entity)

    for i in range(200):
        model = static_rock_model
        x = random.randint(0, 800)
        z = random.randint(0, 800)
        y = terrain.get_height_of_terrain(x, z)

        entity = Entity(model, [x, y, z], 0, random.randint(0, 360), 0, 1)
        entities.append(entity)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~LIGHTS~~~~~~~~~~~~~~~~
    sun = Light([100, 100, 1000], [1, 1, 1])
    lights = [sun]
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~RENDERER~~~~~~~~~~~~~~~
    ShaderProgram.set_is_cel(True)              # before master renderer is created
    master_renderer = MasterRenderer(loader)
    master_renderer.set_fog_density(0.0035)
    master_renderer.set_fog_gradient(5)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~~PLAYER~~~~~~~~~~~~~~
    bunny_model = obj_loader.load_obj_model("bunny", loader)
    static_bunny_model = TexturedModel(bunny_model, ModelTexture(loader.load_texture("white")))

    player = ThirdPersonPlayer(static_bunny_model, [0, 0, 0], 0, 0, 0, 1)
    entities.append(player)
    camera = Camera(player)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~MOUSE PICKER~~~~~~~~~~~~
    picker = TerrainRaycaster(camera, master_renderer.get_projection_matrix())
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        player.move()
        camera.move()

        picker.update()
        # print(picker.get_current_terrain_point())

        # render to screen
        master_renderer.render_scene(entities, terrains, lights, camera, display)

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
