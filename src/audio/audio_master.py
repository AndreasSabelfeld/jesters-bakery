from openal import *
import PyWave


class AudioMaster:

    __buffers = []
    __device = alcOpenDevice(None)
    __context = alcCreateContext(__device, None)

    def __init__(self):
        alcMakeContextCurrent(self.__context)

    @staticmethod
    def set_listener_data(position: [float, float, float], velocity: [float, float, float]) -> None:
        alListener3f(AL_POSITION, *position)
        alListener3f(AL_VELOCITY, *velocity)

    @classmethod
    def load_sound(cls, file: str) -> int:
        buffer = ctypes.c_uint()
        alGenBuffers(1, ctypes.pointer(buffer))
        cls.__buffers.append(buffer)
        wave_file = PyWave.Wave(file, auto_read=True)
        alBufferData(ALuint(buffer.value),
                     cls.get_open_al_format(wave_file.channels, wave_file.bits_per_sample),
                     wave_file.data,
                     wave_file.data_length,
                     wave_file.samples_per_sec)
        del wave_file
        return buffer.value

    @classmethod
    def clean_up(cls) -> None:
        for buffer in cls.__buffers:
            alDeleteBuffers(1, ctypes.pointer(buffer))
        alcDestroyContext(cls.__context)
        alcCloseDevice(cls.__device)

    @staticmethod
    def get_open_al_format(channels: int, bits_per_sample: int):
        if channels == 1:
            return AL_FORMAT_MONO8 if bits_per_sample == 8 else AL_FORMAT_MONO16
        else:
            return AL_FORMAT_STEREO8 if bits_per_sample == 8 else AL_FORMAT_STEREO16
