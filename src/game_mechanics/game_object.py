from src.audio.source import Source
from src.entities.entity import Entity


class GameObject:

    def __init__(self, entity: Entity, child_0: Entity = None, child_1: Entity = None, int_name: str = "", collider: Entity = None):
        """
        Initializes a GameObject with an entity, optional child entities, internal name, and collider.

        :param entity: The entity connected with this game object.
        :param child_0: An optional child entity of this game object.
        :param child_1: An optional second child entity of this game object.
        :param int_name: The internal name of the game object.
        :param collider: An optional collider entity for collision detection.
        """
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
        self.__sfx_source = Source()
        self.__sfx_source.set_position(*entity.get_position())
        if collider: self.__collider = collider
        if child_0: self.set_child_0(child_0)
        else: self.__child_0 = None
        if child_1: self.set_child_1(child_1)
        else: self.__child_1 = None

    def set_collider(self, collider: Entity) -> None:
        """
        Sets the collider entity for this game object.

        :param collider: The entity to be used as the collider.
        """
        self.__collider = collider

    def get_collider(self) -> Entity:
        """
        Returns the collider entity of this game object.
        """
        return self.__collider

    def set_attachment(self, attachment) -> None:
        """
        Sets the attachment for this game object.

        :param attachment: The attachment to be set.
        """
        self.__attachment = attachment

    def get_attachment(self):
        """
        Returns the attachment of this game object.
        """
        return self.__attachment

    def set_int_name(self, name: str) -> None:
        """
        Sets the internal name of this game object.

        :param name: The internal name to set.
        """
        self.__internal_name = name

    def get_int_name(self) -> str:
        """
        Returns the internal name of this game object.
        """
        return self.__internal_name

    def set_ext_name(self, name: str) -> None:
        """
        Sets the external name of this game object.

        :param name: The external name to set.
        """
        self.__external_name = name

    def get_ext_name(self) -> str:
        """
        Returns the external name of this game object.
        """
        return self.__external_name

    def set_pickup_able(self, pickup_able: bool) -> None:
        """
        Sets whether this game object can be picked up.

        :param pickup_able: True if the object can be picked up; otherwise, False.
        """
        self.__pickup_able = pickup_able

    def is_pickup_able(self) -> bool:
        """
        Returns whether this game object can be picked up.
        """
        return self.__pickup_able

    def set_position(self, pos: list[float]) -> None:
        """
        Sets the position of this game object, including its children and collider.

        :param pos: The new position as a list of three floats (x, y, z).
        """
        pos = [pos[0] + self.get_offset()[0],
               pos[1] + self.get_offset()[1],
               pos[2] + self.get_offset()[2]]
        self.__sfx_source.set_position(*pos)
        self.__entity.set_position(pos)
        self.__collider.set_position(pos)
        if self.has_child_0():
            self.__child_0.set_position(pos)
        if self.has_child_1():
            self.__child_1.set_position(pos)

    def get_position(self) -> list[float]:
        """
        Returns the position of this game object, taking into account its offset.
        """
        pos = [self.__entity.get_position()[0] + self.get_offset()[0],
               self.__entity.get_position()[1] + self.get_offset()[1],
               self.__entity.get_position()[2] + self.get_offset()[2]]
        return pos

    def increase_position(self, dx: float, dy: float, dz: float):
        """
        Increases the position of this game object by specified amounts.

        :param dx: Amount to increase the x position.
        :param dy: Amount to increase the y position.
        :param dz: Amount to increase the z position.
        """
        self.set_position([self.get_position()[0] + dx,
                           self.get_position()[1] + dy,
                           self.get_position()[2] + dz])

    def set_rot_x(self, value: float) -> None:
        """
        Sets the rotation around the x-axis for this game object and its collider.

        :param value: The rotation value to set.
        """
        self.__entity.set_rot_x(value + self.get_rot_offset()[0])
        self.__collider.set_rot_x(value + self.get_rot_offset()[0])
        if self.has_child_0():
            self.__child_0.set_rot_x(value)
        if self.has_child_1():
            self.__child_1.set_rot_x(value)

    def set_rot_y(self, value: float) -> None:
        """
        Sets the rotation around the y-axis for this game object and its collider.

        :param value: The rotation value to set.
        """
        self.__entity.set_rot_y(value + self.get_rot_offset()[1])
        self.__collider.set_rot_y(value + self.get_rot_offset()[1])
        if self.has_child_0():
            self.__child_0.set_rot_y(value)
        if self.has_child_1():
            self.__child_1.set_rot_y(value)

    def set_rot_z(self, value: float) -> None:
        """
        Sets the rotation around the z-axis for this game object and its collider.

        :param value: The rotation value to set.
        """
        self.__entity.set_rot_z(value + self.get_rot_offset()[2])
        self.__collider.set_rot_z(value + self.get_rot_offset()[2])
        if self.has_child_0():
            self.__child_0.set_rot_z(value)
        if self.has_child_1():
            self.__child_1.set_rot_z(value)

    def get_rot_x(self) -> float:
        """
        Returns the rotation around the x-axis of this game object's entity.
        """
        return self.get_entity().get_rot_x()

    def get_rot_y(self) -> float:
        """
        Returns the rotation around the y-axis of this game object's entity.
        """
        return self.get_entity().get_rot_y()

    def get_rot_z(self) -> float:
        """
        Returns the rotation around the z-axis of this game object's entity.
        """
        return self.get_entity().get_rot_z()

    def get_scale(self) -> float:
        """
        Returns the scale of this game object's entity.
        """
        return self.get_entity().get_scale()

    def get_offset(self) -> list[float]:
        """
        Returns the offset of this game object.
        """
        return self.__offset

    def set_offset(self, offset: list[float]) -> None:
        """
        Sets the offset for this game object.

        :param offset: The new offset as a list of three floats.
        """
        self.__offset = offset

    def get_rot_offset(self) -> list[float]:
        """
        Returns the rotational offset of this game object.
        """
        return self.__rot_offset

    def set_rot_offset(self, offset: list[float]) -> None:
        """
        Sets the rotational offset for this game object.

        :param offset: The new rotational offset as a list of three floats.
        """
        self.__rot_offset = offset

    def get_entity(self) -> Entity:
        """
        Returns the entity connected with this game object.
        """
        return self.__entity

    def set_parent(self, parent: 'GameObject') -> None:
        """
        Sets the parent of this game object.

        :param parent: The parent game object to set.
        """
        self.__parent = parent

    def get_parent(self) -> 'GameObject':
        """
        Returns the parent of this game object.
        """
        return self.__parent

    def get_child_0(self) -> 'GameObject':
        """
        Returns the first child game object.
        """
        return self.__child_0

    def set_child_0(self, child: Entity) -> None:
        """
        Sets the first child of this game object.

        :param child: The child entity to set.
        """
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
        """
        Returns the second child game object.
        """
        return self.__child_1

    def set_child_1(self, child: Entity) -> None:
        """
        Sets the second child of this game object.

        :param child: The child entity to set.
        """
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
        """
        Checks if this game object has a first child.

        :return: True if there is a first child; otherwise, False.
        """
        if self.__child_0:
            return True
        return False

    def has_child_1(self) -> bool:
        """
        Checks if this game object has a second child.

        :return: True if there is a second child; otherwise, False.
        """
        if self.__child_1:
            return True
        return False

    def remove_child_0(self) -> None:
        """
        Removes the first child of this game object.
        """
        self.__child_0 = None

    def remove_child_1(self) -> None:
        """
        Removes the second child of this game object.
        """
        self.__child_1 = None

    def set_prompt(self, text: str) -> None:
        """
        Sets the prompt text for this game object.

        :param text: The prompt text to set.
        """
        self.__prompt = text

    def get_prompt(self) -> str:
        """
        Returns the prompt text for this game object.
        """
        return self.__prompt

    def set_info(self, info: str) -> None:
        """
        Sets the info text for this game object.

        :param info: The info text to set.
        """
        self.__info = info

    def get_info(self) -> str:
        """
        Returns the info text for this game object.
        """
        return self.__info

    def get_sfx_source(self) -> Source:
        """
        Returns the sound effects source for this game object.
        """
        return self.__sfx_source
