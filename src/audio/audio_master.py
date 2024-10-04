from openal import *
import PyWave


class AudioMaster:
    """
    Manages audio functionalities such as loading sounds and setting listener data using OpenAL.
    """

    __buffers = []
    __device = alcOpenDevice(None)
    __context = alcCreateContext(__device, None)

    def __init__(self):
        """
        Initializes the AudioMaster class by making the OpenAL context current.
        """
        alcMakeContextCurrent(self.__context)

    @staticmethod
    def set_listener_data(position: [float, float, float], velocity: [float, float, float]) -> None:
        """
        Sets the listener's position and velocity in the 3D space.

        :param position: A list of three floats of the listener's position (x, y, z).
        :param velocity: A list of three floats of the listener's velocity (x, y, z).
        """
        alListener3f(AL_POSITION, *position)
        alListener3f(AL_VELOCITY, *velocity)

    @classmethod
    def load_sound(cls, file: str) -> int:
        """
        Loads a sound file into an OpenAL buffer and returns the buffer ID.

        :param file: The file path of the sound file to load.
        :return: The buffer ID of the loaded sound.
        """
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
        """
        Cleans up by deleting all audio buffers and destroying the OpenAL context and device.
        """
        for buffer in cls.__buffers:
            alDeleteBuffers(1, ctypes.pointer(buffer))
        alcDestroyContext(cls.__context)
        alcCloseDevice(cls.__device)

    @staticmethod
    def get_open_al_format(channels: int, bits_per_sample: int):
        """
        Determines the correct OpenAL audio format based on the number of channels and bits per sample.

        :param channels: The number of audio channels (1 for mono, 2 for stereo).
        :param bits_per_sample: The bit depth of the audio (8 or 16 bits).
        :return: The corresponding OpenAL audio format.
        """
        if channels == 1:
            return AL_FORMAT_MONO8 if bits_per_sample == 8 else AL_FORMAT_MONO16
        else:
            return AL_FORMAT_STEREO8 if bits_per_sample == 8 else AL_FORMAT_STEREO16
