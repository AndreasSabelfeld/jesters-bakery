import os

import dropbox


class DBoxHandler:

    def __init__(self, app_key: str, app_secret: str, refresh_token: str, toaster):
        self.dbx = dropbox.Dropbox(app_key=app_key, app_secret=app_secret, oauth2_refresh_token=refresh_token)
        self.toaster = toaster

    def upload_save_files(self, local_path: str, world_name: str) -> None:
        """
        Upload save files to Dropbox using API v2

        :return: None
        """

        with open(f"{local_path}\\{world_name}.db", 'rb') as f:
            self.dbx.files_upload(f.read(), f"/{world_name}.db", mode=dropbox.files.WriteMode.overwrite)
            f.close()
        with open(f"{local_path}\\{world_name}.fwl", 'rb') as f:
            self.dbx.files_upload(f.read(), f"/{world_name}.fwl", mode=dropbox.files.WriteMode.overwrite)
            f.close()
        self.toaster.show_toast("files uploaded!", " ")

    def download_save_files(self, local_path: str, world_name: str) -> None:
        try:
            with open("tmp.db", "wb+") as f:
                metadata, res = self.dbx.files_download(f"/{world_name}.db")
                f.write(res.content)
                f.close()
                os.replace("tmp.db", f"{local_path}\\{world_name}.db")
            with open(f"tmp.fwl", "wb+") as f:
                metadata, res = self.dbx.files_download(f"/{world_name}.fwl")
                f.write(res.content)
                f.close()
                os.replace("tmp.fwl", f"{local_path}\\{world_name}.fwl")
            self.toaster.show_toast("files downloaded!", " ")

        except dropbox.exceptions.ApiError:
            self.toaster.show_toast("Error:", "No such file in Dropbox directory.")
            self.upload_save_files(local_path, world_name)