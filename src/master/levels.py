import random

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

        self.__current_lvl = 1
        self.__current_order = 0
        self.__order_time = 0

        self.__amount_of_orders = 0
        self.__length_of_day = 0
        self.__goal_points = 0
        self.__total_points = 0
        self.__start_offset_factor = 1

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
        if self.__order_time > self.__orders[self.__current_order].get_initial_time() * self.__start_offset_factor:
            if self.__current_order < len(self.__orders) - 1:
                self.__current_order += 1
                self.__order_time = 0
                self.__start_order(self.__orders[self.__current_order])

        self.__order_time += Time.get_delta_time()
        self.__update_orders()

    def progress_next_day(self) -> None:
        self.__current_lvl += 1

    def start_current_day(self) -> None:
        match self.__current_lvl:
            case 1:
                self.day_1()
            case _:
                # game finished
                pass

    def __start_order(self, order: Order) -> None:
        game_object = order.spawn_ticket(self.__ticket_machine)
        self.__entities.append(game_object)
        self.__collider_entities.append(game_object)
        self.__sm_entities.append(game_object)

    def __update_orders(self) -> None:
        for i in range(self.__current_order + 1):
            self.__orders[i].check_if_fulfilled()

    def day_1(self):
        self.__amount_of_orders = 3
        for _ in range(self.__amount_of_orders):
            length_of_order = random.randint(3, 5)
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__length_of_day = 0
        for order in self.__orders:
            self.__length_of_day += order.get_time()
        self.__goal_points = 0

    def count_down(self) -> None:
        if self.__countdown > 0:
            self.__countdown -= Time.get_delta_time()
        else:
            self.__countdown = 0
            return

    def get_current_lvl(self) -> int:
        return self.__current_lvl

    def get_length_of_day(self) -> int:
        return self.__length_of_day

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
