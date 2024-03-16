from src.audio.audio_master import AudioMaster
from src.audio.source import Source
from time import sleep
from openal import alDistanceModel, AL_LINEAR_DISTANCE, AL_LINEAR_DISTANCE_CLAMPED, AL_INVERSE_DISTANCE,  \
    AL_INVERSE_DISTANCE_CLAMPED, AL_EXPONENT_DISTANCE, AL_EXPONENT_DISTANCE_CLAMPED


def main():
    AudioMaster()
    AudioMaster.set_listener_data([0, 0, 0], [0, 0, 0])
    alDistanceModel(AL_INVERSE_DISTANCE_CLAMPED)

    buffer = AudioMaster.load_sound("res/bounce.wav")
    source = Source()
    source.set_looping(True)
    source.play(buffer)

    x_pos = 8
    source.set_position(0, 0, 0)

    c = ''
    while c != 'q':
        x_pos -= 0.3
        source.set_position(x_pos, 0, 2)
        print(x_pos)
        sleep(0.1)

    source.delete()
    AudioMaster.clean_up()


if __name__ == "__main__":
    main()
