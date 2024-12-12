import os

from dotenv import load_dotenv, dotenv_values
from tkinter import messagebox
from win10toast import ToastNotifier

from src.dbox_handler import DBoxHandler
from src.valheim_detector import ValheimDetector


def main():
    choice = messagebox.askyesno("Valheim-Sync", "Start the program?")
    if not choice:
        return

    # loading variables from .env file
    load_dotenv()
    WORLD_NAME = os.getenv("WORLD_NAME")

    toaster = ToastNotifier()

    toaster.show_toast("running... ", "Valheim-Sync has been started.")
    dropbox = DBoxHandler(os.getenv("APP_KEY"), os.getenv("APP_SECRET"), os.getenv("REFRESH_TOKEN"), toaster)
    valheim = ValheimDetector(WORLD_NAME, dropbox, toaster)
    running = True
    while running:
        if valheim.game_started():
            dropbox.download_save_files(valheim.path, WORLD_NAME)
            valheim.initial_read()

        if valheim.files_changed():
            dropbox.upload_save_files(valheim.path, WORLD_NAME)


if __name__ == "__main__":
    main()
