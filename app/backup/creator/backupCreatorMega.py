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
        BackupCreator.__init__(self, source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)
        # TODO: serializar el diccionario si fuera posible
        self.folders: dict = {}

    def __login_mega(self):
        logger.debug("Se inicia sesión en la cuenta de Mega")
        mega = Mega().login(self._user, self._password)
        # TODO: controlar que el usuario logeado es el correcto y no el default
        # print(mega.get_user())
        logger.debug("Cuenta de Mega iniciada")
        return mega

    def __get_id_file(self, mega: Mega, pathfile: str) -> str:
        logger.debug(f"Se busca el directorio '{pathfile}' en el diccionario de Mega")
        if self.folders.get(pathfile):
            return self.folders[pathfile]

        logger.debug(f"Se busca el directorio '{pathfile}' en la cuenta de Mega")
        folders = pathfile.split("/")
        parent_id: str = ''
        path: str = ''
        for i, folder in enumerate(folders):
            if not folder and i == 0:
                continue

            logger.debug(f"Se busca el directorio o archivo '{folder}' en el diccionario")
            if self.folders.get(path+folder):
                logger.debug(f"Directorio o archivo '{folder}' encontrado en el diccionario")
                parent_id = self.folders.get(path+folder)
                path += folder + "/"
            else:
                logger.debug(f"Buscando el directorio o archivo '{folder}'")
                folder_find = mega.find(folder, exclude_deleted=True)
                logger.debug(folder_find)
                if folder_find and (not parent_id or parent_id == folder_find[1].get('p')):
                    logger.debug(f"Id padre '{parent_id}' - Soy '{folder_find[0]}' [{folder}]")
                    logger.debug(f"Se guarda el directorio o archivo '{folder}' en el diccionario")
                    self.folders[path+folder] = folder_find[0]
                    parent_id = folder_find[0]
                    path += folder + "/"
                else:
                    logger.info(f"El directorio o archivo '{path}{folder}' no existe en la cuenta de Mega")
                    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.destination_dir)
        return parent_id

    def upload_backup(self, filename_upload: str):
        mega: Mega = self.__login_mega()
        id_folder: str = self.__get_id_file(mega=mega, pathfile=self.destination_dir)

        logger.debug(f"Se procede a subir el fichero '{filename_upload}' a la cuenta de MEGA")
        mega.upload(filename_upload, id_folder)
        logger.info(f"El fichero '{filename_upload}' se ha subido a la cuenta de MEGA")
        remove(filename_upload)
        logger.debug(f"Se elimina el fichero '{filename_upload}' del equipo local")

    def remove_backup(self, filename_backup: str):
        mega: Mega = self.__login_mega()
        logger.debug(f"Se busca el fichero '{self.destination_dir}/{filename_backup}' en la cuenta de Mega")
        id_backup_file: str = self.__get_id_file(mega=mega, pathfile=self.destination_dir+'/'+filename_backup)

        logger.debug(f"Se procede a eliminar el fichero '{self.destination_dir}/{filename_backup}' de la cuenta de MEGA")
        mega.delete(id_backup_file)
        logger.info(f"El fichero '{filename_backup}' se ha eliminado de la cuenta de MEGA")
