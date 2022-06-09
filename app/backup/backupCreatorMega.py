#!/usr/bin/python3

from .backupCreator import BackupCreator
import errno
from mega import Mega
from os import remove
import os


class MegaBackupCreator(BackupCreator):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        super().__init__(source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    def upload_backup(self, filename_upload: str):
        # TODO: añadir línea al log (debug)
        print("Se inicia sesión en la cuenta de Mega")
        # TODO: obtener los datos de otro sitio
        mega = Mega().login(os.environ.get("mega_user"), os.environ.get("mega_pass"))
        # TODO: añadir línea al log (debug)
        print("Cuenta de Mega iniciada")

        # TODO: añadir línea al log (debug)
        print(f"Se busca el directorio {self.destination_dir} en la cuenta de Mega")
        folder = mega.find(self.destination_dir, exclude_deleted=True)
        # Comprobar si el directorio no existe, para crearlo
        if not folder:
            # TODO: añadir línea al log
            print(f"Carpeta {self.destination_dir} no encontrada en la cuenta de Mega")
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.destination_dir)

        mega.upload(filename_upload, folder[0])
        # TODO: añadir línea al log
        print(f"El fichero {filename_upload} se ha subido a su cuenta de MEGA")
        remove(filename_upload)
        # TODO: añadir línea al log
        print(f"Se elimina el fichero {filename_upload} del equipo local")
