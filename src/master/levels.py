import random

from src.toolbox.path import PATH
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.order import MasterOrder, Order
from src.render_engine.time import Time


class Levels:
    def __init__(self, master_order: MasterOrder, ticket_machine: GameObject, ents: list, col_ents: list, sm_ents: list):
        self.__master_order = master_order
        self.__ticket_machine = ticket_machine
        self.__entities = ents
        self.__collider_entities = col_ents
        self.__sm_entities = sm_ents

        self.__current_lvl = -1
        self._load_save()

        self.__current_order = 0
        self.__order_time = 0

        self.__amount_of_orders = 0
        self.__goal_points = 0
        self.__total_points = 0

        self.__countdown = 0
        self.__initial_spawn = False

        self.__orders = list()

    def update(self) -> None:
        if self.__countdown != 0:
            self.count_down()
            return
        if not self.__initial_spawn:
            self.__start_order(self.__orders[self.__current_order])
            self.__initial_spawn = True
        if self.__order_time > self.__orders[self.__current_order].get_initial_time():
            if self.__current_order < len(self.__orders) - 1:
                self.__current_order += 1
                self.__order_time = 0
                self.__start_order(self.__orders[self.__current_order])
        if self.check_if_all_orders_fulfilled():
            self.calculate_points()

        self.__order_time += Time.get_delta_time()
        self.__update_orders()

    def check_if_all_orders_fulfilled(self) -> bool:
        for i in range(len(self.__orders)):
            if not self.__orders[i].is_fulfilled():
                return False
        return True

    def calculate_points(self) -> int:
        self.__total_points = 0
        for i in range(self.__current_order + 1):
            self.__total_points += self.__orders[i].calculate_points()
        return self.__total_points

    def progress_next_day(self) -> None:
        self.__current_lvl += 1
        self._write_save(self.__current_lvl)

    def start_current_day(self) -> bool:
        self.__orders = list()

        match self.__current_lvl:
            case 1: self.day_1()
            case 2: self.day_2()
            case 3: self.day_3()
            case 4: self.day_4()
            case 5: self.day_5()
            case 6: self.day_6()
            case 7: self.day_7()
            case _:
                return False

        return True

    def day_1(self):
        self.__amount_of_orders = 2
        for _ in range(self.__amount_of_orders):
            length_of_order = 2
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 0

    def day_2(self):
        self.__amount_of_orders = 2
        for _ in range(self.__amount_of_orders):
            length_of_order = 4
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 0

    def day_3(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 2
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 10

    def day_4(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 4
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 15

    def day_5(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 6
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 15

    def day_6(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 8
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 15

    def day_7(self):
        self.__amount_of_orders = 8
        for _ in range(self.__amount_of_orders):
            length_of_order = 8
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 15

    def __start_order(self, order: Order) -> None:
        game_object = order.spawn_ticket(self.__ticket_machine)
        self.__entities.append(game_object)
        self.__collider_entities.append(game_object)
        self.__sm_entities.append(game_object)

    def __update_orders(self) -> None:
        for i in range(self.__current_order + 1):
            self.__orders[i].check_if_fulfilled()

    def _load_save(self) -> None:
        save_file = f"{PATH}/sav/save.txt"
        with open(save_file, "a+") as f:
            f.seek(0)
            data = f.read()
            if not data:
                f.write(f"{1}")
                f.seek(0)
                data = f.read()
            self.__current_lvl = int(data)
            f.close()

    @staticmethod
    def _write_save(data: int) -> None:
        save_file = f"{PATH}/sav/save.txt"
        with open(save_file, "w") as f:
            f.write(f"{data}")
            f.close()

    def count_down(self) -> None:
        if self.__countdown > 0:
            self.__countdown -= Time.get_delta_time()
        else:
            self.__countdown = 0
            return

    def get_current_lvl(self) -> int:
        return self.__current_lvl

    def get_goal_points(self) -> int:
        return self.__goal_points

    def get_total_points(self) -> int:
        return self.__total_points

    def get_count_down(self) -> float:
        return self.__countdown

    def set_countdown(self, value: float) -> None:
        self.__countdown = value

    def get_orders(self) -> list[Order]:
        return self.__orders

    def get_current_order(self) -> int:
        return self.__current_order
