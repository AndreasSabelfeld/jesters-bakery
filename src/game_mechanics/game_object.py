from src.entities.entity import Entity


class GameObject:

    def __init__(self, entity: Entity, child_0: Entity = None, child_1: Entity = None, int_name: str = "", collider: Entity = None):
        self.__entity = entity
        self.__internal_name = int_name
        self.__external_name = ""
        self.__prompt = ""
        self.__info = ""
        self.__pickup_able = True
        self.__attachment = None
        self.__collider = entity
        self.__parent = None
        self.__offset = [0, 0, 0]
        self.__rot_offset = [0, 0, 0]
        if collider: self.__collider = collider
        if child_0: self.set_child_0(child_0)
        else: self.__child_0 = None
        if child_1: self.set_child_1(child_1)
        else: self.__child_1 = None

    def set_collider(self, collider: Entity) -> None:
        self.__collider = collider

    def get_collider(self) -> Entity:
        return self.__collider

    def set_attachment(self, attachment) -> None:
        self.__attachment = attachment

    def get_attachment(self):
        return self.__attachment

    def set_int_name(self, name: str) -> None:
        self.__internal_name = name

    def get_int_name(self) -> str:
        return self.__internal_name

    def set_ext_name(self, name: str) -> None:
        self.__external_name = name

    def get_ext_name(self) -> str:
        return self.__external_name

    def set_pickup_able(self, pickup_able: bool) -> None:
        self.__pickup_able = pickup_able

    def is_pickup_able(self) -> bool:
        return self.__pickup_able

    def set_position(self, pos: list[float]) -> None:
        pos = [pos[0] + self.get_offset()[0],
               pos[1] + self.get_offset()[1],
               pos[2] + self.get_offset()[2]]
        self.__entity.set_position(pos)
        self.__collider.set_position(pos)
        if self.has_child_0():
            self.__child_0.set_position(pos)
        if self.has_child_1():
            self.__child_1.set_position(pos)

    def get_position(self) -> list[float]:
        pos = [self.__entity.get_position()[0] + self.get_offset()[0],
               self.__entity.get_position()[1] + self.get_offset()[1],
               self.__entity.get_position()[2] + self.get_offset()[2]]
        return pos

    def increase_position(self, dx: float, dy: float, dz: float):
        self.set_position([self.get_position()[0] + dx,
                           self.get_position()[1] + dy,
                           self.get_position()[2] + dz])

    def set_rot_x(self, value: float) -> None:
        self.__entity.set_rot_x(value + self.get_rot_offset()[0])
        self.__collider.set_rot_x(value + self.get_rot_offset()[0])
        if self.has_child_0():
            self.__child_0.set_rot_x(value)
        if self.has_child_1():
            self.__child_1.set_rot_x(value)

    def set_rot_y(self, value: float) -> None:
        self.__entity.set_rot_y(value + self.get_rot_offset()[1])
        self.__collider.set_rot_y(value + self.get_rot_offset()[1])
        if self.has_child_0():
            self.__child_0.set_rot_y(value)
        if self.has_child_1():
            self.__child_1.set_rot_y(value)

    def set_rot_z(self, value: float) -> None:
        self.__entity.set_rot_z(value + self.get_rot_offset()[2])
        self.__collider.set_rot_z(value + self.get_rot_offset()[2])
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

    def get_offset(self) -> list[float]:
        return self.__offset

    def set_offset(self, offset: list[float]) -> None:
        self.__offset = offset

    def get_rot_offset(self) -> list[float]:
        return self.__rot_offset

    def set_rot_offset(self, offset: list[float]) -> None:
        self.__rot_offset = offset

    def get_entity(self) -> Entity:
        return self.__entity

    def set_parent(self, parent: 'GameObject') -> None:
        self.__parent = parent

    def get_parent(self) -> 'GameObject':
        return self.__parent

    def get_child_0(self) -> 'GameObject':
        return self.__child_0

    def set_child_0(self, child: Entity) -> None:
        if isinstance(child, GameObject):
            self.__child_0 = child
        else:
            self.__child_0 = GameObject(child)
        self.__child_0.set_parent(self)
        self.__child_0.set_offset([self.__child_0.get_position()[0] - self.get_position()[0],
                                   self.__child_0.get_position()[1] - self.get_position()[1],
                                   self.__child_0.get_position()[2] - self.get_position()[2]])
        self.__child_0.set_rot_offset([self.__child_0.get_rot_x() - self.get_rot_x(),
                                       self.__child_0.get_rot_y() - self.get_rot_y(),
                                       self.__child_0.get_rot_z() - self.get_rot_z()])

    def get_child_1(self) -> 'GameObject':
        return self.__child_1

    def set_child_1(self, child: Entity) -> None:
        if isinstance(child, GameObject):
            self.__child_1 = child
        else:
            self.__child_1 = GameObject(child)
        self.__child_1.set_parent(self)
        self.__child_1.set_offset([self.__child_1.get_position()[0] - self.get_position()[0],
                                   self.__child_1.get_position()[1] - self.get_position()[1],
                                   self.__child_1.get_position()[2] - self.get_position()[2]])
        self.__child_1.set_rot_offset([self.__child_0.get_rot_x() - self.get_rot_x(),
                                       self.__child_0.get_rot_y() - self.get_rot_y(),
                                       self.__child_0.get_rot_z() - self.get_rot_z()])

    def has_child_0(self) -> bool:
        if self.__child_0:
            return True
        return False

    def has_child_1(self) -> bool:
        if self.__child_1:
            return True
        return False

    def remove_child_0(self) -> None:
        self.__child_0 = None

    def remove_child_1(self) -> None:
        self.__child_1 = None

    def set_prompt(self, text: str) -> None:
        self.__prompt = text

    def get_prompt(self) -> str:
        return self.__prompt

    def set_info(self, info: str) -> None:
        self.__info = info

    def get_info(self) -> str:
        return self.__info
