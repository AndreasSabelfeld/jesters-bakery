from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.render_engine.display_manager import DisplayManager
from src.render_engine.loader import Loader

from OpenGL.GLUT import *


def main():
    # ~~~~~~~~~~~~DISPLAY~~~~~~~~~~~~~~
    display = DisplayManager(1920, 1080)
    display.create_display("An-gine")  # creates display
    display.set_backdrop_color(173, 216, 230)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~LOADERS~~~~~~~~~~~~~~
    loader = Loader()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~TEXT~~~~~~~~~~~~~~~~
    TextMaster(loader)
    font = FontType(loader.load_texture("arial"), "res/arial.fnt")
    text = GUIText("This is a test text!", 10, font, [0.5, 0.5], 0.5, True)
    text.set_color(1, 0, 0)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while glutGetWindow() != 0:
        TextMaster.render()

        glutSwapBuffers()    # needs to be called AFTER finished drawing
        glutMainLoopEvent()  # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
