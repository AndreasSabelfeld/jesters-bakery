from OpenGL.GL import *
from OpenGL.GLUT import *
import glfw

from .loader import Loader
from .input_controller import KeyboardInput
from src.render_engine.time import Time


class DisplayManager:
    """
    Class for managing everything that has to do with the OpenGL window.
    """
    __x = 1920
    __y = 1080
    __backdrop_color = (255, 0, 0)

    __viewport_x = 0
    __viewport_y = 0

    __delta: float = 0.0

    def __init__(self, x: int = 1920, y: int = 1080, backdrop_color: list[float] = (255, 0, 0)):
        """
        Creates a new DisplayManager object.
        On default, a 1920 by 1080 screen with a red background will be created.

        :params x: Width of the window.
        :params y: Height of the window.
        :params backdrop_color: Background color of the window as a list of RGB values.
        """
        DisplayManager.__backdrop_color = backdrop_color
        DisplayManager.__x = x
        DisplayManager.__y = y

        Time.set_last_frame_time(Time.time_current_time())

    def create_display(self, window_name: str) -> None:
        """
        Creates a new display to the screen.

        :params window_name: The name of the window.
        """
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        glutInit()                                               # initialize GLUT
        glutSetOption(GLUT_MULTISAMPLE, 4)                       # turn on anti-aliasing
        glutInitDisplayMode(GLUT_RGBA | GLUT_MULTISAMPLE)        # initialize colors
        glutInitWindowSize(self.get_width(), self.get_height())  # set windows size
        glutInitWindowPosition(0, 0)                             # set window position
        glutCreateWindow(f"{window_name}")                       # create window (with a name) and set window attribute
        glutFullScreen()                                         # make it fullscreen
        glutSetWindow(1)
        glutDisplayFunc(self.update_display)

        viewport = glGetIntegerv(GL_VIEWPORT)

        DisplayManager.__viewport_x = viewport[2]
        DisplayManager.__viewport_y = viewport[3]

        glutKeyboardFunc(KeyboardInput().key_down)
        glutKeyboardUpFunc(KeyboardInput().key_up)
        glutSpecialFunc(KeyboardInput().special_keys)

        glutMouseFunc(KeyboardInput().mouse_buttons)
        glutMouseWheelFunc(KeyboardInput().mouse_wheel)
        glutPassiveMotionFunc(KeyboardInput().mouse_movement)

        glutWarpPointer(self.get_width() // 2, self.get_height() // 2)
        KeyboardInput.set_window_size([self.get_width() // 2, self.get_height() // 2])
        glutSetCursor(GLUT_CURSOR_NONE)

        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)  # prevent program from stopping

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # so that transparent bits of the texture won't get rendered
        glEnable(GL_ALPHA_TEST)

        glEnable(GL_DEPTH_TEST)

    def update_display(self) -> None:
        """
        Update the display by clearing the screen and resetting the mouse position.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen

        r, g, b = self.get_backdrop_color()  # Get backdrop color
        glClearColor(r, g, b, 1)             # Set backdrop color

        glLoadIdentity()                                    # Reset all graphic/shape's position

        glutWarpPointer(self.get_width() // 2, self.get_height() // 2)
        KeyboardInput.set_window_size([self.get_width() // 2, self.get_height() // 2])
        KeyboardInput().mouse_wheel(0, 0, 0, 0)                               # reset mouse scroll
        KeyboardInput().mouse_movement(*KeyboardInput().get_mouse_pos())    # reset mouse movement

    @staticmethod
    def destroy_window() -> None:
        """
        Clean up resources and destroy the window.
        """
        Loader.clean_up()
        glutDestroyWindow(1)

    @classmethod
    def get_width(cls) -> int:
        """
        Get the width of the display.

        :return: Width of the display.
        """
        return cls.__x

    @classmethod
    def get_height(cls) -> int:
        """
        Get the height of the display.

        :return: Height of the display.
        """
        return cls.__y

    @classmethod
    def get_viewport(cls) -> list[int]:
        """
        Get the viewport dimensions.

        :return: List containing the viewport width and height.
        """
        return [cls.__viewport_x, cls.__viewport_y]

    @classmethod
    def set_backdrop_color(cls, r: int, g: int, b: int):
        """
        Set the backdrop color for the window.

        :params r: Red component of the color.
        :params g: Green component of the color.
        :params b: Blue component of the color.
        """
        cls.__backdrop_color = [r, g, b]

    @classmethod
    def get_backdrop_color(cls) -> list[float]:
        """
        Get the backdrop color for the window.

        :return: List containing the normalized RGB values of the backdrop color.
        """
        return [cls.__backdrop_color[0] / 255, cls.__backdrop_color[1] / 255, cls.__backdrop_color[2] / 255]
