from functools import total_ordering


@total_ordering
class EndPoint:
    """
    The EndPoint class represents an endpoint of an axis-aligned bounding box (AABB) to use in collision detection.
    It saves a reference to the box it belongs to, its value, and if it is a minimum point.

    The class is decorated with `@total_ordering`, which provides full comparison capabilities (__eq__ & __lt__).
    """

    def __init__(self, owner, value: float, is_min: bool):
        """
        Initializes an EndPoint instance.

        :param owner: The object that owns this endpoint.
        :param value: The coordinate value of the endpoint along an axis.
        :param is_min: Boolean showing if this is the minimum (True) or maximum (False) endpoint along the axis.
        """
        self.owner = owner
        self.value = value
        self.is_min = is_min

    @staticmethod
    def _is_valid_operand(other) -> bool:
        """
        Checks if the operand is valid for comparison (has a `value` attribute)

        :param other: The other object to compare.
        :return: True if the operand is valid (has a `value` attribute), False otherwise.
        """
        return hasattr(other, "value")

    def __eq__(self, other) -> bool:
        """
        Compares equality between two EndPoint objects based on their `value`.

        :param other: The other EndPoint object to compare.
        :return: True if the two endpoints have the same value, False otherwise.
        """
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other) -> bool:
        """
        Compares two EndPoint objects to determine which one has a smaller `value`.

        :param other: The other EndPoint object to compare.
        :return: True if this EndPoint's value is less than the other's value, False otherwise.
        """
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value < other.value
