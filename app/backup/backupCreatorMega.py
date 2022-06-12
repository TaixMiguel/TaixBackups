#!/usr/bin/python3

from .backupCreator import BackupCreator
import errno
from mega import Mega
from os import remove
import os


class MegaBackupCreator(BackupCreator):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        super().__init__(source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    def get_id_folder(self, mega: Mega) -> str:
        # TODO: añadir línea al log (debug)
        print(f"Se busca el directorio {self.destination_dir} en la cuenta de Mega")
        folders = self.destination_dir.split("/")
        parent_id: str = ''
        path: str = ''
        for i, folder in enumerate(folders):
            if not folder and i == 0:
                continue

            # TODO: añadir línea al log (debug)
            print(f"Buscando el directorio {folder}")
            folder_find = mega.find(folder, exclude_deleted=True)
            # TODO: añadir línea al log (debug)
            print(folder_find)
            if folder_find and (not parent_id or parent_id == folder_find[1].get('p')):
                # TODO: añadir línea al log (debug)
                print(f"Id padre {parent_id} - Soy {folder_find[0]}")
                parent_id = folder_find[0]
                path += folder + "/"
            else:
                # TODO: añadir línea al log (debug)
                print(f'El directorio {path}{folder} no existe en la cuenta de Mega')
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.destination_dir)
        return folder_find[0]

    def upload_backup(self, filename_upload: str, user: str, password: str):
        # TODO: añadir línea al log (debug)
        print("Se inicia sesión en la cuenta de Mega")
        mega = Mega().login(user, password)
        # TODO: controlar que el usuario logeado es el correcto y no el default
        # print(mega.get_user())
        # TODO: añadir línea al log (debug)
        print("Cuenta de Mega iniciada")

        # TODO: añadir línea al log (debug)
        print(f"Se busca el directorio {self.destination_dir} en la cuenta de Mega")
        id_folder: str = self.get_id_folder(mega=mega)

        # TODO: añadir línea al log (debug)
        print(f"Se procede a subir el fichero {filename_upload} a su cuenta de MEGA")
        mega.upload(filename_upload, id_folder)
        # TODO: añadir línea al log
        print(f"El fichero {filename_upload} se ha subido a su cuenta de MEGA")
        remove(filename_upload)
        # TODO: añadir línea al log
        print(f"Se elimina el fichero {filename_upload} del equipo local")
