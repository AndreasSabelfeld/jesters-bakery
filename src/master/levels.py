import random

from src.toolbox.path import PATH
from src.game_mechanics.game_object import GameObject
from src.game_mechanics.order import MasterOrder, Order
from src.render_engine.time import Time


class Levels:
    def __init__(self, master_order: MasterOrder, ticket_machine: GameObject, ents: list, col_ents: list, sm_ents: list):
        """
        Initialize the Levels class.

        :params master_order: The master order managing orders.
        :params ticket_machine: The game object representing the ticket machine.
        :params ents: List of entities.
        :params col_ents: List of collider entities.
        :params sm_ents: List of shadow map entities.
        """
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
        """
        Update the level state and manage orders.
        """
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
        """
        Check if all orders have been fulfilled.

        :return: True if all orders are fulfilled, False otherwise.
        """
        for i in range(len(self.__orders)):
            if not self.__orders[i].is_fulfilled():
                return False
        return True

    def calculate_points(self) -> int:
        """
        Calculate total points based on fulfilled orders.

        :return: Total points as an integer.
        """
        self.__total_points = 0
        for i in range(self.__current_order + 1):
            self.__total_points += self.__orders[i].calculate_points()
        return self.__total_points

    def progress_next_day(self) -> None:
        """
        Progress to the next day and save the level.
        """
        self.__current_lvl += 1
        self._write_save(self.__current_lvl)

    def start_current_day(self) -> bool:
        """
        Start the current day based on the level.

        :return: True if the day is started successfully, False otherwise.
        """
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
        self.__goal_points = 20

    def day_5(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 6
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 25

    def day_6(self):
        self.__amount_of_orders = 4
        for _ in range(self.__amount_of_orders):
            length_of_order = 8
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 35

    def day_7(self):
        self.__amount_of_orders = 8
        for _ in range(self.__amount_of_orders):
            length_of_order = 8
            self.__orders.append(Order(self.__master_order, length_of_order))
        self.__goal_points = 50

    def __start_order(self, order: Order) -> None:
        """
        Start a new order and spawn its game object.

        :params order: The order to start.
        """
        game_object = order.spawn_ticket(self.__ticket_machine)
        self.__entities.append(game_object)
        self.__collider_entities.append(game_object)
        self.__sm_entities.append(game_object)

    def __update_orders(self) -> None:
        """
        Update all current orders and check if they are fulfilled.
        """
        for i in range(self.__current_order + 1):
            self.__orders[i].check_if_fulfilled()

    def _load_save(self) -> None:
        """
        Load the current level from the save file.
        """
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
        """
        Write the current level to the save file.

        :params data: The level to save.
        """
        save_file = f"{PATH}/sav/save.txt"
        with open(save_file, "w") as f:
            f.write(f"{data}")
            f.close()

    def count_down(self) -> None:
        """
        Decrease the countdown timer.
        """
        if self.__countdown > 0:
            self.__countdown -= Time.get_delta_time()
        else:
            self.__countdown = 0
            return

    def get_current_lvl(self) -> int:
        """
        Get the current level.

        :return: Current level as an integer.
        """
        return self.__current_lvl

    def get_goal_points(self) -> int:
        """
        Get the goal points.

        :return: Goal points as an integer.
        """
        return self.__goal_points

    def get_total_points(self) -> int:
        """
        Get the total points.

        :return: Total points as an integer.
        """
        return self.__total_points

    def get_count_down(self) -> float:
        """
        Get the current countdown value.

        :return: Countdown value as a float.
        """
        return self.__countdown

    def set_countdown(self, value: float) -> None:
        """
        Set the countdown value.

        :params value: New countdown value.
        """
        self.__countdown = value

    def get_orders(self) -> list[Order]:
        """
        Get the list of orders.

        :return: List of orders.
        """
        return self.__orders

    def get_current_order(self) -> int:
        """
        Get the index of the current order.

        :return: Current order index as an integer.
        """
        return self.__current_order
