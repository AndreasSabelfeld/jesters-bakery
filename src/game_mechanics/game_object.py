from src.entities.entity import Entity


class GameObject:

    def __init__(self, entity: Entity, child: Entity = None, name: str = "", collider: Entity = None):
        self.__entity = entity
        self.__name = name
        self.__pickup_able = True
        self.__attachment = None
        self.__collider = entity
        if collider: self.__collider = collider
        if child: self.__child = GameObject(child)
        else: self.__child = None

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
        if self.has_child():
            self.__child.set_position(pos)

    def get_position(self) -> list[float]:
        return self.__entity.get_position()

    def set_rot_x(self, value: float) -> None:
        self.__entity.set_rot_x(value)
        self.__collider.set_rot_x(value)
        if self.has_child():
            self.__child.set_rot_x(value)

    def set_rot_y(self, value: float) -> None:
        self.__entity.set_rot_y(value)
        self.__collider.set_rot_y(value)
        if self.has_child():
            self.__child.set_rot_y(value)

    def set_rot_z(self, value: float) -> None:
        self.__entity.set_rot_z(value)
        self.__collider.set_rot_z(value)
        if self.has_child():
            self.__child.set_rot_z(value)

    def get_entity(self) -> Entity:
        return self.__entity

    def get_child(self):
        return self.__child

    def set_child(self, child: Entity) -> None:
        self.__child = GameObject(child)

    def has_child(self) -> bool:
        if self.__child is not None:
            return True
        return False
