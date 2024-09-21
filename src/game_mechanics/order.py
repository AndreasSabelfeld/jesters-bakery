import math
import random
import sys

from src.entities.entity import Entity
from src.font_mesh_creator.font_type import FontType
from src.font_mesh_creator.gui_text import GUIText
from src.font_rendering.text_master import TextMaster
from src.game_mechanics.coffee_container import CoffeeContainer
from src.game_mechanics.coffee_page import CoffeePage
from src.game_mechanics.food import Food
from src.game_mechanics.game_object import GameObject
from src.guis.gui_texture import GuiTexture
from src.models.raw_model import RawModel
from src.models.textured_model import TexturedModel
from src.post_processing.fbo import FBO
from src.render_engine.input_controller import Binds
from src.render_engine.time import Time
from src.textures.model_texture import ModelTexture


class Possibility:
    def __init__(self, name: str, wishes: list, time: float, vessel=None, content=None):
        self.__name = name
        self.__wishes = wishes
        self.__time = time
        self.__vessel = vessel
        self.__content = content

    def get_name(self) -> str:
        return self.__name

    def get_wishes(self) -> list:
        return self.__wishes.copy()

    def get_time(self) -> float:
        return self.__time

    def set_content(self, content: list[str]) -> None:
        self.__content = content

    def get_content(self) -> list[str]:
        return self.__content

    def get_vessel(self) -> int:
        return self.__vessel


class Order:

    __unpicked_game_objects = list()

    def __init__(self, master: 'MasterOrder', amount_of_orders: int):
        self.__master = master
        self.__current_order = master.create_order(amount_of_orders)
        self.__initial_time = master.calculate_time(self.__current_order)
        self.__time = self.__initial_time
        font_size = 8
        self.__text = GUIText(self.get_order_string(), font_size, self.__master.get_font(), [0, 0], 0.15, False)
        self.__white_texture = GuiTexture(self.__master.get_loader().load_texture("pngs/machinery/white"), [0, 0], [1920, 1080])
        self.__fulfilled = False
        self.__points = 0
        self.__right_orders = 0
        self.__wrong_orders = 0
        self.__ticket_height = 0

    def get_order(self) -> list:
        return self.__current_order.copy()

    def get_time(self) -> float:
        return self.__time

    def get_initial_time(self) -> float:
        return self.__initial_time

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

    def get_all_contents(self) -> list[list]:
        l = list()
        for order in self.get_order():
            l.append(order[0].get_content())
        return l

    @staticmethod
    def create_fbo(x: int, y: int) -> FBO:
        return FBO(x, y, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)

    def __get_texture(self) -> ModelTexture:
        x = 1920
        y = 1080
        fbo = FBO(x, y, multi_target=False, depth_buffer_type=FBO.DEPTH_TEXTURE)
        fbo.bind_frame_buffer()
        guis = [self.__white_texture]
        self.__master.get_gui_renderer().render(guis)
        TextMaster.render_specified([self.get_gui_text()])
        fbo.unbind_frame_buffer()
        return ModelTexture(fbo.get_color_texture())

    def __get_model(self) -> RawModel:
        file_name = "ticket"
        obj = open(f"{sys.path[0]}/res/objs/machinery/{file_name}.obj", 'w')
        x = 0.075
        y = (0.5 / 16) * (self.__text.get_number_of_lines() - 1)
        self.__ticket_height = 0.7 * y
        obj.write(f"v -{x} {self.__ticket_height} -0.000000\n" +
                  f"v {x} {self.__ticket_height} -0.000000\n" +
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
        return self.__master.get_obj_loader().load_obj_model(f"objs/machinery/{file_name}", self.__master.get_loader())

    def __get_game_object(self, pos: list[float], rot: list[float], size: float) -> GameObject:
        static_model = TexturedModel(self.__get_model(), self.__get_texture())
        ticket_entity = Entity(static_model, pos, *rot, size)

        white_tex = ModelTexture(self.__master.get_loader().load_texture("pngs/machinery/white"))
        backside_static_model = TexturedModel(self.__get_model(), white_tex)
        offset_pos = [pos[0] + 0.1 * math.sin(math.radians(rot[1])),
                      pos[1],
                      pos[2] + 0.1 * math.cos(math.radians(rot[1]))]
        backside_ticket_entity = Entity(backside_static_model, offset_pos, rot[0], rot[1] + 180, rot[2], size)

        game_object = GameObject(ticket_entity, int_name="TICKET")
        game_object.set_attachment(self)
        game_object.set_child_0(backside_ticket_entity)

        return game_object

    def spawn_ticket(self, ticket_machine: GameObject) -> GameObject:
        x = 0.3 * math.sin(math.radians(ticket_machine.get_rot_y())) * ticket_machine.get_scale()
        y = 1.8 * ticket_machine.get_scale()
        z = 0.3 * math.cos(math.radians(ticket_machine.get_rot_y())) * ticket_machine.get_scale()
        game_object = self.__get_game_object([ticket_machine.get_position()[0] + x,
                                              ticket_machine.get_position()[1] + y,
                                              ticket_machine.get_position()[2] + z],
                                             [ticket_machine.get_rot_x(),
                                              ticket_machine.get_rot_y(),
                                              ticket_machine.get_rot_z()],
                                             ticket_machine.get_scale() * 10)
        game_object.set_ext_name("Ticket")
        game_object.set_prompt(f"Press {Binds.get_bind(Binds.R2)} or {Binds.get_bind(Binds.L2)} to pick up")
        if self.__unpicked_game_objects:
            for go in self.__unpicked_game_objects:
                go.increase_position(0, self.__ticket_height * ticket_machine.get_scale() * 10, 0)
        self.__unpicked_game_objects.append(game_object)
        return game_object

    def check_if_fulfilled(self) -> None:
        if self.__current_order:
            self.__time -= Time.get_delta_time()
        else:
            self.__fulfilled = True

        if self.__master.get_placed_products():
            for product in self.__master.get_placed_products():
                if isinstance(product, CoffeeContainer):
                    content = product.get_content()
                    vessel = product.get_container_type()
                else:
                    # it's food
                    content = [product.get_food()]
                    vessel = None
                try:
                    index = self.get_all_contents().index(content)
                    if vessel == self.__current_order[index][0].get_vessel():
                        self.__current_order.pop(index)
                        self.__right_orders += 1
                    self.__master.get_placed_products().remove(product)
                except ValueError:
                    # product is not in order
                    self.__wrong_orders += 1
                    self.__master.get_placed_products().remove(product)

    def calculate_points(self) -> int:
        self.__points = (10 * self.__right_orders) - (5 * self.__wrong_orders) + int(self.__time)
        return self.__points

    def is_fulfilled(self) -> bool:
        return self.__fulfilled

    def remove_game_object_from_list(self, game_object: GameObject) -> None:
        if game_object in self.__unpicked_game_objects:
            self.__unpicked_game_objects.remove(game_object)


class MasterOrder:
    def __init__(self, loader, obj_loader, gui_renderer, parent_object: GameObject):
        self.__chance_for_wish = 0.25
        self.__placed_products = []

        self.__coffee_dict = dict()
        self.__load_coffee_products()
        self.__possibilities = list()
        self.__load_possibilities()

        self.__loader = loader
        self.__obj_loader = obj_loader
        self.__font = FontType(self.__loader.load_texture("fnts/receipt"), "res/fnts/receipt.fnt")
        self.__gui_renderer = gui_renderer
        self.__parent_object = parent_object

        self.__i = 0

    def create_order(self, amount_of_orders: int) -> list:
        order = list()
        for _ in range(amount_of_orders):
            prod = self.__possibilities[random.randint(0, len(self.__possibilities)-1)]
            wish = None
            wish_time = 0
            if random.random() < self.__chance_for_wish:
                if prod.get_wishes():
                    wish = prod.get_wishes()[random.randint(0, len(prod.get_wishes())-1)]
                    if wish == "Oat Milk":
                        wish_time = 30
            self.load_content(prod, wish)
            order.append([prod, wish, prod.get_time() + wish_time])
        return order

    def load_content(self, prod: Possibility, wish: str) -> None:
        if not wish:
            if not prod.get_content():
                prod.set_content([prod.get_name()])
            if prod.get_name() == "Tea":
                wish = prod.get_wishes()[random.randint(0, len(prod.get_wishes()) - 1)]
                prod.get_content().append(wish)
        elif wish == "Oat Milk":
            if prod.get_name() == "Milk Coffee":
                prod.set_content(["Oat Milk", "Foam", "Oat Milk Coffee"])
            if prod.get_name() == "Latte Macchiato":
                prod.set_content(["Oat Milk", "Foam", "Espresso"])
            if prod.get_name() == "Cappuccino":
                prod.set_content(["Oat Milk", "Foam", "Espresso"])
            if prod.get_name() == "Cafe Latte":
                prod.set_content(["Oat Milk", "Foam", "Cafe Creme"])
            if prod.get_name() == "Hot Chocolate":
                prod.set_content(["Oat Milk", "Caotina"])
            if prod.get_name() == "Cold Chocolate":
                prod.set_content(["Oat Milk", "Caotina"])
            if prod.get_name() == "Children Chocolate":
                prod.set_content(["Oat Milk", "Caotina"])
            if prod.get_name() == "Doppio Macchiato":
                prod.set_content(["Oat Milk", "Foam", "Doppio"])
            if prod.get_name() == "Ovomaltine":
                prod.set_content(["Oat Milk", "Ovomaltine", "Mixed"])
            if prod.get_name() == "Chai":
                prod.set_content(["Oat Milk", "Chai", "Mixed"])
            if prod.get_name() == "Chocolatl":
                prod.set_content(["Oat Milk", "Chocolatl", "Mixed"])
        else:
            if not prod.get_content():
                prod.set_content([prod.get_name(), wish])
            else:
                prod.get_content().append(wish)

    def place(self, product: GameObject):
        self.__placed_products.append(product.get_attachment())
        left_corner_offset = [4 * self.__parent_object.get_scale(),
                              4.3 * self.__parent_object.get_scale(),
                              -2.1 * self.__parent_object.get_scale()]
        right_corner_offset = [-0.3 * self.__parent_object.get_scale(),
                               4.3 * self.__parent_object.get_scale(),
                               5.7 * self.__parent_object.get_scale()]

        length = 7
        width = 3
        height = 3
        offset = 0.4 * self.__parent_object.get_scale()

        j = (self.__i // length) % width
        k = (self.__i // (width * length)) % height

        x = self.__parent_object.get_position()[0] + left_corner_offset[0] - offset - j * (4 / width)
        y = self.__parent_object.get_position()[1] + right_corner_offset[1] + (2 * k)
        z = self.__parent_object.get_position()[2] + left_corner_offset[2] + offset + \
            ((right_corner_offset[2] - left_corner_offset[2]) / length) * (self.__i % length)

        if product.get_parent():
            product.get_parent().set_position([x, y, z])
        else:
            product.set_position([x, y, z])

        self.__i += 1

    @staticmethod
    def calculate_time(order: list):
        time = 0
        grace_factor = 3
        for element in order:
            time += element[2]
        time *= grace_factor
        return time

    def get_font(self) -> FontType:
        return self.__font

    def get_loader(self):
        return self.__loader

    def get_obj_loader(self):
        return self.__obj_loader

    def get_gui_renderer(self):
        return self.__gui_renderer

    def get_placed_products(self):
        return self.__placed_products

    def __load_coffee_products(self) -> None:
        for instance in CoffeePage.get_instances():
            for product in instance.get_products():
                self.__coffee_dict[product.get_name()] = product

    def __load_possibilities(self) -> None:
        poss = list()
        poss.append(Possibility("Espresso", ["Decaffeinated"],
                                self.__coffee_dict["Espresso"].get_brew_length(),
                                self.__coffee_dict["Espresso"].get_container_type()))
        poss.append(Possibility("Doppio", ["Decaffeinated"],
                                self.__coffee_dict["Doppio"].get_brew_length(),
                                self.__coffee_dict["Doppio"].get_container_type()))
        poss.append(Possibility("Cafe Creme", ["Decaffeinated"],
                                self.__coffee_dict["Cafe Creme"].get_brew_length(),
                                self.__coffee_dict["Cafe Creme"].get_container_type()))
        poss.append(Possibility("Milk Coffee", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Milk Coffee"].get_brew_length(),
                                self.__coffee_dict["Milk Coffee"].get_container_type()))
        poss.append(Possibility("Cappuccino", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Cappuccino"].get_brew_length(),
                                self.__coffee_dict["Cappuccino"].get_container_type()))
        poss.append(Possibility("Latte Macchiato", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Latte Macchiato"].get_brew_length(),
                                self.__coffee_dict["Latte Macchiato"].get_container_type()))
        poss.append(Possibility("Cafe Latte", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Cafe Latte"].get_brew_length(),
                                self.__coffee_dict["Cafe Latte"].get_container_type()))
        poss.append(Possibility("Tea", ["English Breakfast", "Earl Grey", "Rooibos", "Nana-Mint", "Verveine", "Ginger"],
                                self.__coffee_dict["Tea"].get_brew_length(),
                                self.__coffee_dict["Tea"].get_container_type()))
        poss.append(Possibility("Hot Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Hot Chocolate"].get_brew_length(),
                                self.__coffee_dict["Hot Chocolate"].get_container_type()))
        poss.append(Possibility("Cold Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Cold Chocolate"].get_brew_length(),
                                self.__coffee_dict["Cold Chocolate"].get_container_type()))
        poss.append(Possibility("Children Chocolate", ["Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Children Chocolate"].get_brew_length(),
                                self.__coffee_dict["Children Chocolate"].get_container_type()))
        poss.append(Possibility("Warm Milk", [],
                                self.__coffee_dict["Warm Milk"].get_brew_length(),
                                self.__coffee_dict["Warm Milk"].get_container_type()))
        poss.append(Possibility("Cold Milk", [],
                                self.__coffee_dict["Cold Milk"].get_brew_length(),
                                self.__coffee_dict["Cold Milk"].get_container_type()))
        poss.append(Possibility("Babyccino", [],
                                self.__coffee_dict["Babyccino"].get_brew_length(),
                                self.__coffee_dict["Babyccino"].get_container_type()))
        poss.append(Possibility("Americano", ["Decaffeinated"],
                                self.__coffee_dict["Americano"].get_brew_length(),
                                self.__coffee_dict["Americano"].get_container_type()))
        poss.append(Possibility("Doppio Macchiato", ["Decaffeinated", "Lactose Free", "Oat Milk"],
                                self.__coffee_dict["Doppio Macchiato"].get_brew_length(),
                                self.__coffee_dict["Doppio Macchiato"].get_container_type()))
        poss.append(Possibility("Coke", ["Ice", "Lemon"], 6.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Schorle", ["Ice", "Lemon"], 6.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Sparkling Water", ["Ice", "Lemon"], 6.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Still Water", ["Ice", "Lemon"], 6.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Beer", [], 6.0, CoffeeContainer.BEER))
        poss.append(Possibility("Chai", ["Lactose Free", "Oat Milk"], 5.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Sprite", ["Ice", "Lemon"], 5.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Coke Zero", ["Ice", "Lemon"], 5.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Orange Juice", ["Ice", "Lemon"], 5.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Topfit Juice", ["Ice", "Lemon"], 5.0, CoffeeContainer.BIG_GLASS))
        poss.append(Possibility("Prosecco", [], 5.0, CoffeeContainer.PROSECCO))
        poss.append(Possibility("Panache", [], 8.0, CoffeeContainer.BEER,
                                content=["Sprite", "Beer"]))
        poss.append(Possibility("Ovomaltine", [], 10.0, CoffeeContainer.BIG_GLASS,
                                content=["Milk for Chai, Ovo", "Ovomaltine", "Mixed"]))
        poss.append(Possibility("Chai", [], 10.0, CoffeeContainer.BIG_GLASS,
                                content=["Milk for Chai, Ovo", "Chai", "Mixed"]))
        poss.append(Possibility("Chocolatl", [], 10.0, CoffeeContainer.BIG_GLASS,
                                content=["Milk for Chai, Ovo", "Chocolatl", "Mixed"]))
        poss.append(Possibility("Ham Sandwich", [], 5.0))
        poss.append(Possibility("Egg Sandwich", [], 5.0))
        poss.append(Possibility("Tuna Sandwich", [], 5.0))
        poss.append(Possibility("Mango Chutney Sandwich", [], 5.0))
        poss.append(Possibility("Tomato Sandwich", [], 5.0))
        poss.append(Possibility("Silserli", [], 5.0))
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
