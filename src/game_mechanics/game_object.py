from src.entities.entity import Entity


class GameObject:

    def __init__(self, entity: Entity, child: Entity = None):
        self.__entity = entity
        if child is not None:
            self.__child = GameObject(child)
        else:
            self.__child = None

    def set_position(self, pos: list[float]) -> None:
        self.__entity.set_position(pos)
        if self.has_child():
            self.__child.set_position(pos)

    def set_rot_x(self, value: float) -> None:
        self.__entity.set_rot_x(value)
        if self.has_child():
            self.__child.set_rot_x(value)

    def set_rot_y(self, value: float) -> None:
        self.__entity.set_rot_y(value)
        if self.has_child():
            self.__child.set_rot_y(value)

    def set_rot_z(self, value: float) -> None:
        self.__entity.set_rot_z(value)
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
