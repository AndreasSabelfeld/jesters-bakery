import time


class Time:
    """
    Class that returns the current time, time from the last frame and the time difference 'delta time'
    """
    __last_frame_time: float
    __delta_time: float
    __current_time: float

    @classmethod
    def set_last_frame_time(cls, value: float) -> None:
        """
        Sets the last frame time.

        :params value: The time of the last frame in milliseconds.
        """
        cls.__last_frame_time = value

    @classmethod
    def get_last_frame_time(cls) -> float:
        """
        Returns the last frame time.

        :return: The last frame time in milliseconds.
        """
        return cls.__last_frame_time

    @staticmethod
    def time_current_time() -> float:
        """
        Returns the current time in milliseconds.

        :return: The current time in milliseconds.
        """
        return time.time() * 1000

    @classmethod
    def set_current_time(cls, value: float) -> None:
        """
        Sets the current time.

        :params value: The current time in milliseconds.
        """
        cls.__current_time = value

    @classmethod
    def get_current_time(cls) -> float:
        """
        Returns the current time.

        :return: The current time in milliseconds.
        """
        return cls.__current_time

    @classmethod
    def set_delta_time(cls) -> None:
        """
        Calculates and sets the delta time.
        """
        cls.__delta_time = (cls.__current_time - cls.__last_frame_time) / 1000

    @classmethod
    def get_delta_time(cls) -> float:
        """
        Returns the delta time.

        :return: The delta time in seconds.
        """
        return cls.__delta_time
