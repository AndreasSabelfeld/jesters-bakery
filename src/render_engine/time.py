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
        cls.__last_frame_time = value

    @classmethod
    def get_last_frame_time(cls) -> float:
        return cls.__last_frame_time

    @staticmethod
    def time_current_time() -> float:
        return time.time() * 1000

    @classmethod
    def set_current_time(cls, value: float):
        cls.__current_time = value

    @classmethod
    def get_current_time(cls):
        return cls.__current_time

    @classmethod
    def set_delta_time(cls):
        cls.__delta_time = (cls.__current_time - cls.__last_frame_time) / 1000

    @classmethod
    def get_delta_time(cls) -> float:
        return cls.__delta_time
