#!/usr/bin/python3

from app.backup.creator.backupCreator import BackupCreator
import logging
import os
from os import remove
import shutil

logger = logging.getLogger(__name__)


class LocalBackupCreator(BackupCreator):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        BackupCreator.__init__(self, source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    def upload_backup(self, filename_upload: str):
        if not os.path.exists(self.destination_dir):
            logger.info(f"El directorio '{self.destination_dir}' no existe, se crea de forma automática")
            os.makedirs(self.destination_dir)

        shutil.move(filename_upload, self.destination_dir)
        logger.debug(f"El fichero '{filename_upload}' se ha movido a la carpeta '{self.destination_dir}'")

    def remove_backup(self, filename_backup: str):
        logger.debug(f"Se procede a eliminar el fichero '{self.destination_dir}/{filename_backup}' del equipo local")
        remove(self.destination_dir+'/'+filename_backup)
        logger.info(f"El fichero '{filename_backup}' se ha eliminado del equipo local")
