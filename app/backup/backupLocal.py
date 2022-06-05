#!/usr/bin/python3

from backup import Backup
import os
import shutil


class LocalBackup(Backup):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        super().__init__(source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    def upload_backup(self, filename_upload: str):
        if not os.path.exists(self.destination_dir):
            # TODO: añadir línea al log
            print(f"El directorio {self.destination_dir} no existe, se crea de forma automática")
            os.makedirs(self.destination_dir)

        shutil.move(filename_upload, self.destination_dir)
        # TODO: añadir línea al log
        print(f"El fichero {filename_upload} se ha movido a la carpeta {self.destination_dir}")
