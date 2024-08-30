from tests import test_cube, test_island, test_forest, test_cel_shading, test_text, test_audio, test_collision, \
    test_bakery, test_bakery_modelled, test_cups
from src.master.game_master import GameMaster


def main():
    game = GameMaster()

    """lvl = 8
    match lvl:
        case 0: test_island.main()
        case 1: test_forest.main()
        case 2: test_cube.main()
        case 3: test_cel_shading.main()
        case 4: test_text.main()
        case 5: test_audio.main()
        case 6: test_collision.main()
        case 7: test_bakery.main()
        case 8: test_bakery_modelled.main()
        case 9: test_cups.main()"""


if __name__ == "__main__":
    main()
