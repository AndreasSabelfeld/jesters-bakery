import random
import sys

from src.entities.entity import Entity
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.coffee_page import CoffeePage
from src.game_mechanics.game_object import GameObject
from src.guis.gui_texture import GuiTexture
from src.models.raw_model import RawModel
from src.models.textured_model import TexturedModel
from src.post_processing.fbo import FBO
from src.textures.model_texture import ModelTexture


class Possibility:
    def __init__(self, name: str, wishes: list, time=None):
        self.__name = name
        self.__wishes = wishes
        self.__time = time

    def get_name(self) -> str:
        return self.__name

    def get_wishes(self) -> list:
        return self.__wishes.copy()

    def get_time(self) -> float:
        return self.__time


class Order:
    def __init__(self, master: 'MasterOrder', amount_of_orders: int):
        self.__master = master
        self.__order = master.create_order(amount_of_orders)
        self.__time = master.calculate_time(self.__order)
        self.__text = GUIText(self.get_order_string(), 10, self.__master.get_font(), [0, 0], 0.15, False)
        self.__white_texture = GuiTexture(self.__master.get_loader().load_texture("white"), [0, 0], [1920, 1080])

    def get_order(self) -> list:
        return self.__order

    def get_time(self) -> float:
        return self.__time

    def get_order_string(self) -> str:
        string = ""
        for element in self.get_order():
            name = element[0].get_name()
            string += f"1x {name} \n"
            if element[1]:
                string += 4 * ' ' + f"- {element[1]} \n"
        return string

    def get_gui_text(self) -> GUIText:
        return self.__text

    @staticmethod
    def create_fbo(x: int, y: int) -> FBO:
        return FBO(x, y, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)

    def get_texture(self) -> ModelTexture:
        x = 1920
        y = 1080
        fbo = FBO(x, y, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)
        fbo.bind_frame_buffer()
        guis = [self.__white_texture]
        self.__master.get_gui_renderer().render(guis)
        TextMaster.render_specified([self.get_gui_text()])
        fbo.unbind_frame_buffer()
        return ModelTexture(fbo.get_color_texture())

    def get_model(self) -> RawModel:
        file_name = "ticket"
        obj = open(f"{sys.path[0]}/res/{file_name}.obj", 'w')
        x = 0.075
        y = (0.5 / 16) * self.__text.get_text_string().count('\n')
        obj.write(f"v -{x} {y * 0.7} -0.000000\n" +
                  f"v {x} {y * 0.7} -0.000000\n" +
                  f"v -{x} 0.000000 0.000000\n" +
                  f"v {x} 0.000000 0.000000\n" +
                  f"vn -0.0000 -0.0000 -1.0000\n" +
                  f"vt 0.000000 0.000000\n" +
                  f"vt {2 * x} 0.000000\n" +
                  f"vt 0.000000 {y}\n" +
                  f"vt {2 * x} {y}\n" +
                  f"s 0\n" +
                  f"f 3/3/1 2/2/1 1/1/1\n" +
                  f"f 3/3/1 4/4/1 2/2/1")
        obj.close()
        return self.__master.get_obj_loader().load_obj_model(f"{file_name}", self.__master.get_loader())

    def get_game_object(self, pos: list[float], rot: list[float], size: float):
        static_model = TexturedModel(self.get_model(), self.get_texture())
        ticket_entity = Entity(static_model, pos, *rot, size)
        return GameObject(ticket_entity, int_name="TICKET")


class MasterOrder:
    def __init__(self, loader, obj_loader, gui_renderer):
        self.__chance_for_wish = 0.25

        self.__coffee_dict = dict()
        self.__load_coffee_products()
        self.__possibilities = list()
        self.__load_possibilities()

        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__font = FontType(self.__loader.load_texture("candara"), "res/candara.fnt")
        self.__gui_renderer = gui_renderer

    def create_order(self, amount_of_orders: int) -> list:
        order = list()
        for _ in range(amount_of_orders):
            prod = self.__possibilities[random.randint(0, len(self.__possibilities)-1)]
            wish = None
            if random.random() < self.__chance_for_wish:
                if prod.get_wishes():
                    wish = prod.get_wishes()[random.randint(0, len(prod.get_wishes())-1)]
            order.append([prod, wish, prod.get_time()])
        return order

    @staticmethod
    def calculate_time(order: list):
        time = 0
        for element in order:
            time += element[2]
        time *= 1.5
        return time

    def get_font(self) -> FontType:
        return self.__font

    def get_loader(self):
        return self.__loader

    def get_obj_loader(self):
        return self.__obj_loader

    def get_gui_renderer(self):
        return self.__gui_renderer

    def __load_coffee_products(self) -> None:
        for instance in CoffeePage.get_instances():
            for product in instance.get_products():
                self.__coffee_dict[product.get_name()] = product

    def __load_possibilities(self) -> None:
        poss = list()
        poss.append(Possibility("Espresso", ["Decaffeinated"], self.__coffee_dict["Espresso"].get_brew_length()))
        poss.append(Possibility("Doppio", ["Decaffeinated"], self.__coffee_dict["Doppio"].get_brew_length()))
        poss.append(Possibility("Café Crème", ["Decaffeinated"], self.__coffee_dict["Café Crème"].get_brew_length()))
        poss.append(Possibility("Milk Coffee", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Milk Coffee"].get_brew_length()))
        poss.append(Possibility("Cappuccino", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Cappuccino"].get_brew_length()))
        poss.append(Possibility("Latte Macchiato", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Latte Macchiato"].get_brew_length()))
        poss.append(Possibility("Café Latte", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Café Latte"].get_brew_length()))
        poss.append(Possibility("Tea", [], self.__coffee_dict["Tea"].get_brew_length()))
        poss.append(Possibility("Hot Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Hot Chocolate"].get_brew_length()))
        poss.append(Possibility("Cold Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Cold Chocolate"].get_brew_length()))
        poss.append(Possibility("Children Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Children Chocolate"].get_brew_length()))
        poss.append(Possibility("Warm Milk", [], self.__coffee_dict["Warm Milk"].get_brew_length()))
        poss.append(Possibility("Cold Milk", [], self.__coffee_dict["Cold Milk"].get_brew_length()))
        poss.append(Possibility("Babyccino", [], self.__coffee_dict["Babyccino"].get_brew_length()))
        poss.append(Possibility("Americano", ["Decaffeinated"], self.__coffee_dict["Americano"].get_brew_length()))
        poss.append(Possibility("Doppio Macchiato", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Doppio Macchiato"].get_brew_length()))
        poss.append(Possibility("Coke", ["Ice", "Lemon"], 6.0))
        poss.append(Possibility("Schorle", ["Ice", "Lemon"], 6.0))
        poss.append(Possibility("Sparkling Water", ["Ice", "Lemon"], 6.0))
        poss.append(Possibility("Still Water", ["Ice", "Lemon"], 6.0))
        poss.append(Possibility("Beer", ["Ice", "Lemon"], 6.0))
        poss.append(Possibility("Chai", ["Lactose Free", "Oat Milk"], 5.0))
        poss.append(Possibility("Sprite", ["Ice", "Lemon"], 5.0))
        poss.append(Possibility("Coke Zero", ["Ice", "Lemon"], 5.0))
        poss.append(Possibility("Juice", ["Ice", "Lemon"], 5.0))
        poss.append(Possibility("Prosecco", [], 5.0))
        poss.append(Possibility("Panaché", [], 8.0))
        poss.append(Possibility("Sandwich", [], 5.0))
        poss.append(Possibility("Sirserli", [], 5.0))
        poss.append(Possibility("Croissant", [], 5.0))
        poss.append(Possibility("Chocolate Croissant", [], 5.0))
        poss.append(Possibility("Almond Croissant", [], 5.0))
        poss.append(Possibility("Strawberry Tart", [], 5.0))
        poss.append(Possibility("Cookie", [], 5.0))
        poss.append(Possibility("Spitzbub", [], 5.0))
        poss.append(Possibility("Linzerli", [], 5.0))
        poss.append(Possibility("Carac", [], 5.0))
        poss.append(Possibility("Wurstwegge", [], 5.0))
        poss.append(Possibility("Schinkengipfel", [], 5.0))
        poss.append(Possibility("Chocolate Cake", [], 5.0))
        poss.append(Possibility("Passionfruit Cake", [], 5.0))
        poss.append(Possibility("Carrot Cake", [], 5.0))
        poss.append(Possibility("Citron Cake", [], 5.0))

        self.__possibilities = poss
