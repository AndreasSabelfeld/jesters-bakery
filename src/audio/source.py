from openal import *


class Source:
    """
    Represents an audio source in OpenAL, providing methods to control playback and various other methods.
    """

    def __init__(self):
        """
        Initializes the Source class and generates an OpenAL source ID.
        """
        self.__source_id = ctypes.c_uint()
        alGenSources(1, ctypes.pointer(self.__source_id))

    def play(self, buffer) -> None:
        """
        Plays the given sound buffer.

        :param buffer: The OpenAL buffer ID to play.
        """
        self.stop()
        alSourcei(self.__source_id, AL_BUFFER, buffer)
        self.continue_playing()

    def delete(self) -> None:
        """
        Deletes the OpenAL source, stopping playback and freeing connected resources.
        """
        self.stop()
        alDeleteSources(1, ctypes.pointer(self.__source_id))

    def pause(self) -> None:
        """
        Pauses playback of the audio source.
        """
        alSourcePause(self.__source_id)

    def continue_playing(self) -> None:
        """
        Resumes playback of the paused audio source.
        """
        alSourcePlay(self.__source_id)

    def stop(self) -> None:
        """
        Stops playback of the audio source.
        """
        alSourceStop(self.__source_id)

    def is_playing(self) -> bool:
        """
        Checks if the audio source is currently playing.

        :return: True if the source is playing, False otherwise.
        """
        state = ctypes.c_long()
        alGetSourcei(self.__source_id, AL_SOURCE_STATE, ctypes.pointer(state))
        return state.value == AL_PLAYING

    def set_velocity(self, x: float, y: float, z: float) -> None:
        """
        Sets the velocity of the audio source in 3D space.

        :param x: The x-coordinate of the velocity.
        :param y: The y-coordinate of the velocity.
        :param z: The z-coordinate of the velocity.
        """
        alSource3f(self.__source_id, AL_VELOCITY, x, y, z)

    def set_looping(self, loop: bool) -> None:
        """
        Sets whether the audio source should loop or not.

        :param loop: True to enable looping, False to disable it.
        """
        alSourcei(self.__source_id, AL_LOOPING, AL_TRUE if loop else AL_FALSE)

    def set_volume(self, volume: float) -> None:
        """
        Sets the volume of the audio source.

        :param volume: The volume level, where 1.0 is the default volume.
        """
        alSourcef(self.__source_id, AL_GAIN, volume)

    def set_pitch(self, pitch: float) -> None:
        """
        Sets the pitch of the audio source.

        :param pitch: The pitch multiplier.
        """
        alSourcef(self.__source_id, AL_PITCH, pitch)

    def set_position(self, x: float, y: float, z: float) -> None:
        """
        Sets the position of the audio source in 3D space.

        :param x: The x-coordinate of the position.
        :param y: The y-coordinate of the position.
        :param z: The z-coordinate of the position.
        """
        alSource3f(self.__source_id, AL_POSITION, x, y, z)

    def set_rolloff_factor(self, factor: float) -> None:
        """
        Sets the rolloff factor, which controls how the source's volume decreases with distance.

        :param factor: The rolloff factor (higher values make the sound fade faster over distance).
        """
        alSourcef(self.__source_id, AL_ROLLOFF_FACTOR, factor)

    def set_reference_distance(self, reference_distance: float) -> None:
        """
        Sets the reference distance, which is the distance where the volume starts to decrease.

        :param reference_distance: The reference distance.
        """
        alSourcef(self.__source_id, AL_REFERENCE_DISTANCE, reference_distance)

    def set_max_distance(self, max_distance: float) -> None:
        """
        Sets the maximum distance of the perceivable audio.

        :param max_distance: The maximum distance.
        """
        alSourcef(self.__source_id, AL_MAX_DISTANCE, max_distance)
