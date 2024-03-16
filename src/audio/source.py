from openal import *


class Source:
    def __init__(self):
        self.__source_id = ctypes.c_uint()
        alGenSources(1, ctypes.pointer(self.__source_id))

    def play(self, buffer) -> None:
        self.stop()
        alSourcei(self.__source_id, AL_BUFFER, buffer)
        self.continue_playing()

    def delete(self) -> None:
        self.stop()
        alDeleteSources(1, ctypes.pointer(self.__source_id))

    def pause(self) -> None:
        alSourcePause(self.__source_id)
        
    def continue_playing(self) -> None:
        alSourcePlay(self.__source_id)

    def stop(self) -> None:
        alSourceStop(self.__source_id)

    def is_playing(self) -> bool:
        state = ctypes.c_long()
        alGetSourcei(self.__source_id, AL_SOURCE_STATE, ctypes.pointer(state))
        return state.value == AL_PLAYING

    def set_velocity(self, x: float, y: float, z: float) -> None:
        alSource3f(self.__source_id, AL_VELOCITY, x, y, z)

    def set_looping(self, loop: bool) -> None:
        alSourcei(self.__source_id, AL_LOOPING, AL_TRUE if loop else AL_FALSE)

    def set_volume(self, volume: float) -> None:
        alSourcef(self.__source_id, AL_GAIN, volume)

    def set_pitch(self, pitch: float) -> None:
        alSourcef(self.__source_id, AL_PITCH, pitch)

    def set_position(self, x: float, y: float, z: float) -> None:
        alSource3f(self.__source_id, AL_POSITION, x, y, z)

    def set_rolloff_factor(self, factor: float):
        alSourcef(self.__source_id, AL_ROLLOFF_FACTOR, factor)

    def set_reference_distance(self, reference_distance: float):
        alSourcef(self.__source_id, AL_REFERENCE_DISTANCE, reference_distance)

    def set_max_distance(self, max_distance: float):
        alSourcef(self.__source_id, AL_MAX_DISTANCE, max_distance)
