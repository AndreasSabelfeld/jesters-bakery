from src.master.game_master import GameMaster


def main():
    game = GameMaster()
    game.get_display().destroy_window()

if __name__ == "__main__":
    main()
