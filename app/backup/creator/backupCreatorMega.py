#!/usr/bin/python3

from app.backup.creator.backupCreator import BackupCreator
import errno
import logging
from mega import Mega
from os import remove
import os

logger = logging.getLogger(__name__)


class MegaBackupCreator(BackupCreator):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        super().__init__(source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    def get_id_folder(self, mega: Mega) -> str:
        logger.debug(f"Se busca el directorio {self.destination_dir} en la cuenta de Mega")
        folders = self.destination_dir.split("/")
        parent_id: str = ''
        path: str = ''
        for i, folder in enumerate(folders):
            if not folder and i == 0:
                continue

            logger.debug(f"Buscando el directorio {folder}")
            folder_find = mega.find(folder, exclude_deleted=True)
            logger.debug(folder_find)
            if folder_find and (not parent_id or parent_id == folder_find[1].get('p')):
                logger.debug(f"Id padre {parent_id} - Soy {folder_find[0]}")
                parent_id = folder_find[0]
                path += folder + "/"
            else:
                logger.info(f'El directorio {path}{folder} no existe en la cuenta de Mega')
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.destination_dir)
        return folder_find[0]

    def upload_backup(self, filename_upload: str, user: str, password: str):
        logger.debug("Se inicia sesión en la cuenta de Mega")
        mega = Mega().login(user, password)
        # TODO: controlar que el usuario logeado es el correcto y no el default
        # print(mega.get_user())
        logger.debug("Cuenta de Mega iniciada")

        logger.debug(f"Se busca el directorio {self.destination_dir} en la cuenta de Mega")
        id_folder: str = self.get_id_folder(mega=mega)

        logger.debug(f"Se procede a subir el fichero {filename_upload} a su cuenta de MEGA")
        mega.upload(filename_upload, id_folder)
        logger.info(f"El fichero {filename_upload} se ha subido a su cuenta de MEGA")
        remove(filename_upload)
        logger.debug(f"Se elimina el fichero {filename_upload} del equipo local")
