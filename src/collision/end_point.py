from functools import total_ordering


@total_ordering
class EndPoint:

    def __init__(self, owner, value: float, is_min: bool):
        self.owner = owner
        self.value = value
        self.is_min = is_min

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "value")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.value < other.value
