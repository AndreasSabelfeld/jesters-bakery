from OpenGL.GLUT import *
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
from src.entities.player import FirstPersonPlayer

from src.terrain.terrain import Terrain

from src.toolbox.raycaster import TerrainRaycaster


def main():
    # DISPLAY
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(173, 216, 230)
    # ------------

    # LOADERS
    loader = Loader()
    obj_loader = OBJLoader()
    # ------------

    # CUBE
    cube_model = obj_loader.load_obj_model("cube", loader)
    static_cube_model = TexturedModel(cube_model, ModelTexture(loader.load_texture("grass_block")))
    cube_texture = static_cube_model.get_texture()
    cube_texture.set_shine_damper(10)
    cube_texture.set_reflectivity(1)
    # ------------

    # ENTITIES
    entities = [Entity(static_cube_model, [0, 0, 10], 0, 0, 0, 1)]
    """for i in range(100):
        for j in range(100):
            e = Entity(static_cube_model, [0, i*2, j*2], 0, 0, 0, 1)
            entities.append(e)"""

    lights = []
    sun = Light([0, 1000, -7000], [0.5, 0.5, 0.5])
    lights.append(sun)

    # RENDERER
    master_renderer = MasterRenderer(loader)
    # ----------

    # CAMERA
    player = FirstPersonPlayer(static_cube_model, [0, 0, 0], 0, 0, 0, 1)
    camera = Camera(player)
    # ----------

    while glutGetWindow() != 0:
        # game logic
        Time.set_current_time(Time.time_current_time())
        Time.set_delta_time()                               # automatically calculates delta time
        Time.set_last_frame_time(Time.time_current_time())

        camera.move()
        player.move()

        master_renderer.render_scene(entities, [], [], lights, camera, display)

        glutSwapBuffers()         # needs to be called AFTER finished drawing
        glutMainLoopEvent()       # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == '__main__':
    main()
