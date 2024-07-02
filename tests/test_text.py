from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.render_engine.display_manager import DisplayManager
from src.render_engine.loader import Loader

from src.game_mechanics.order import Order, MasterOrder

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
    font = FontType(loader.load_texture("candara"), "res/candara.fnt")
    text = GUIText("This is a test text! \nEspresso \nCappuccino", 10, font, [0, 0], 1, True)
    text.set_color(1, 0, 0)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~~~~~~~~~~~~ORDER~~~~~~~~~~~~~~~~
    master_order = MasterOrder(loader)
    order1 = Order(master_order, 3)
    order1.get_gui_text()
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    while glutGetWindow() != 0:
        TextMaster.render()

        glutSwapBuffers()    # needs to be called AFTER finished drawing
        glutMainLoopEvent()  # used to run openGL manually in a loop instead of glutMainLoop()


if __name__ == "__main__":
    main()
