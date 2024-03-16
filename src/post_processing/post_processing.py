from OpenGL.GL import *
from src.render_engine.display_manager import DisplayManager
from src.post_processing.contrast_changer import ContrastChanger
from src.gaussian_blur.horizontal_blur import HorizontalBlur
from src.gaussian_blur.vertical_blur import VerticalBlur
from src.bloom.bright_filter import BrightFilter
from src.bloom.combine_filter import CombineFilter


class PostProcessing:

    __POSITIONS = [-1, 1, -1, -1, 1, 1, 1, -1]

    def __init__(self, loader):
        self.__quad = loader.load_gui_to_vao(self.__POSITIONS, 2)
        self.__contrast_changer = ContrastChanger()
        self.__hblur_stage1 = HorizontalBlur(DisplayManager.get_width()//5, DisplayManager.get_height()//5)
        self.__vblur_stage1 = VerticalBlur(DisplayManager.get_width()//5, DisplayManager.get_height()//5)
        # self.__hblur_stage2 = HorizontalBlur(DisplayManager.get_width() // 8, DisplayManager.get_height() // 8)
        # self.__vblur_stage2 = VerticalBlur(DisplayManager.get_width() // 8, DisplayManager.get_height() // 8)
        self.__bright_filter = BrightFilter(DisplayManager.get_width()//2, DisplayManager.get_height()//2)
        self.__combine_filter = CombineFilter()

    def do_post_processing(self, color_texture: int, bright_texture: int) -> None:
        self.start()
        # self.__bright_filter.render(color_texture)
        self.__hblur_stage1.render(bright_texture)
        self.__vblur_stage1.render(self.__hblur_stage1.get_output_texture())
        # self.__hblur_stage2.render(self.__vblur_stage1.get_output_texture())
        # self.__vblur_stage2.render(self.__hblur_stage2.get_output_texture())
        # self.__contrast_changer.render(self.__vblur_stage1.get_output_texture())
        self.__combine_filter.render(color_texture, self.__vblur_stage1.get_output_texture())
        self.end()

    def clean_up(self) -> None:
        self.__contrast_changer.clean_up()
        self.__hblur_stage1.clean_up()
        self.__vblur_stage1.clean_up()
        # self.__hblur_stage2.clean_up()
        # self.__vblur_stage2.clean_up()
        self.__bright_filter.clean_up()
        self.__combine_filter.clean_up()

    def start(self) -> None:
        glBindVertexArray(self.__quad.get_vao_id())
        glEnableVertexAttribArray(0)
        glDisable(GL_DEPTH_TEST)

    @staticmethod
    def end() -> None:
        glEnable(GL_DEPTH_TEST)
        glDisableVertexAttribArray(0)
        glBindVertexArray(0)
