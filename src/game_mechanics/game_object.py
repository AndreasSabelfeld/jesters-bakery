from src.entities.entity import Entity


class GameObject:

    def __init__(self, entity: Entity, child_0: Entity = None, child_1: Entity = None, name: str = "", collider: Entity = None):
        self.__entity = entity
        self.__name = name
        self.__pickup_able = True
        self.__attachment = None
        self.__collider = entity
        if collider: self.__collider = collider
        if child_0: self.__child_0 = GameObject(child_0)
        else: self.__child_0 = None
        if child_1: self.__child_1 = GameObject(child_1)
        else: self.__child_1 = None

    def set_collider(self, collider: Entity) -> None:
        self.__collider = collider

    def get_collider(self) -> Entity:
        return self.__collider

    def set_attachment(self, attachment) -> None:
        self.__attachment = attachment

    def get_attachment(self):
        return self.__attachment

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_pickup_able(self, pickup_able: bool) -> None:
        self.__pickup_able = pickup_able

    def is_pickup_able(self) -> bool:
        return self.__pickup_able

    def set_position(self, pos: list[float]) -> None:
        self.__entity.set_position(pos)
        self.__collider.set_position(pos)
        if self.has_child_0():
            self.__child_0.set_position(pos)
        if self.has_child_1():
            self.__child_1.set_position(pos)

    def get_position(self) -> list[float]:
        return self.__entity.get_position()

    def increase_position(self, dx: float, dy: float, dz: float):
        self.set_position([self.get_position()[0] + dx,
                           self.get_position()[1] + dy,
                           self.get_position()[2] + dz])

    def set_rot_x(self, value: float) -> None:
        self.__entity.set_rot_x(value)
        self.__collider.set_rot_x(value)
        if self.has_child_0():
            self.__child_0.set_rot_x(value)
        if self.has_child_1():
            self.__child_1.set_rot_x(value)

    def set_rot_y(self, value: float) -> None:
        self.__entity.set_rot_y(value)
        self.__collider.set_rot_y(value)
        if self.has_child_0():
            self.__child_0.set_rot_y(value)
        if self.has_child_1():
            self.__child_1.set_rot_y(value)

    def set_rot_z(self, value: float) -> None:
        self.__entity.set_rot_z(value)
        self.__collider.set_rot_z(value)
        if self.has_child_0():
            self.__child_0.set_rot_z(value)
        if self.has_child_1():
            self.__child_1.set_rot_z(value)

    def get_rot_x(self) -> float:
        return self.get_entity().get_rot_x()

    def get_rot_y(self) -> float:
        return self.get_entity().get_rot_y()

    def get_rot_z(self) -> float:
        return self.get_entity().get_rot_z()

    def get_scale(self) -> float:
        return self.get_entity().get_scale()

    def get_entity(self) -> Entity:
        return self.__entity

    def get_child_0(self) -> 'GameObject':
        return self.__child_0

    def set_child_0(self, child: Entity) -> None:
        self.__child_0 = GameObject(child)

    def get_child_1(self) -> 'GameObject':
        return self.__child_1

    def set_child_1(self, child: Entity) -> None:
        self.__child_1 = GameObject(child)

    def has_child_0(self) -> bool:
        if self.__child_0:
            return True
        return False

    def has_child_1(self) -> bool:
        if self.__child_1:
            return True
        return False

