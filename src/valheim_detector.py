import os
import psutil
import hashlib

from src.world import World


class ValheimDetector:
    """
    Class responsible for detecting the start of the game and changing of the save files.
    """

    def __init__(self, world_name: str, dbox, toaster):
        self.world_name = world_name
        self.path = os.getenv('APPDATA').removesuffix("\\Roaming") + "\\LocalLow\\IronGate\\Valheim\\worlds_local"
        self.previously_run = False
        self.prev_hex = World()
        self.dbox = dbox
        self.toaster = toaster

    def initial_read(self):
        """
        Reads the content of the save files for the first time and saves the content into class attributes.

        :return: None
        """
        try:
            with open(f"{self.path}\\{self.world_name}.db", "rb") as f:
                self.prev_hex.db = hashlib.md5(f.read()).hexdigest()
                f.close()
            with open(f"{self.path}\\{self.world_name}.fwl", "rb") as f:
                self.prev_hex.fwl = hashlib.md5(f.read()).hexdigest()
                f.close()
        except FileNotFoundError:
            self.dbox.download_save_files(self.path, self.world_name)
            self.initial_read()

    def game_started(self) -> bool:
        """
        Iterates through all running processes and checks for 'valheim.exe' being run the first time.

        :return: True if 'valheim.exe' is a running process, otherwise False
        """
        try:
            if "valheim.exe" in (p.name() for p in psutil.process_iter()) and not self.previously_run:
                self.previously_run = True
                self.toaster.show_toast("Game start has been detected.", " ")
                return True
            elif not "valheim.exe" in (p.name() for p in psutil.process_iter()):
                self.previously_run = False
            else:
                return False
        except psutil.NoSuchProcess:  # Catch the error caused by the process no longer existing
            self.previously_run = False

    def files_changed(self) -> bool:
        """
        Compares previous contents of the save file to the current content.

        :return: True if the content of any of the files has changed, otherwise False
        """

        # early return because the hex is still empty, the files need to be downloaded first from the web
        if not self.prev_hex.db and not self.prev_hex.fwl:
            return False

        changed = False
        try:
            with open(f"{self.path}\\{self.world_name}.db", "rb") as f:
                new_hex = hashlib.md5(f.read()).hexdigest()
                if self.prev_hex.db != new_hex:
                    changed = True
                    self.toaster.show_toast("files changed.", " ")
                    self.prev_hex.db = new_hex
                f.close()
            with open(f"{self.path}\\{self.world_name}.fwl", "rb") as f:
                new_hex = hashlib.md5(f.read()).hexdigest()
                if self.prev_hex.fwl != new_hex:
                    changed = True
                    self.toaster.show_toast("files changed.", " ")
                    self.prev_hex.fwl = new_hex
                f.close()
        except FileNotFoundError:
            # This may happen while the new save file is being created
            pass

        return changed

