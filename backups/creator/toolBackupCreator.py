#!/usr/bin/python3

from datetime import datetime
import errno
import logging
import shutil
import os

from backups.creator.backupCreatorLocal import LocalBackupCreator
from backups.creator.backupCreatorMega import MegaBackupCreator

logger = logging.getLogger(__name__)


def get_instance_creator(backup_code: str, source_dir: str, destination_dir: str, filename_backup: str = "backup"):
    if backup_code in ('local', 'LOCAL'):
        return LocalBackupCreator(source_dir=source_dir, destination_dir=destination_dir,
                                  filename_backup=filename_backup)
    if backup_code in ('mega', 'MEGA'):
        return MegaBackupCreator(source_dir=source_dir, destination_dir=destination_dir,
                                 filename_backup=filename_backup)
    logger.error(f"No se ha encontrado instancia con el código '{backup_code}'")


def create_backup(source_dir: str, destination_dir: str, filename_backup: str = "backup",
                  date_format: str = "%Y%m%d_%H%M%S") -> str:
    logger.info(f"Se va a crear un backup del directorio {source_dir}")

    # Controlar la existencia de los directorios
    if not os.path.exists(source_dir):
        logger.error(f"No se puede realizar un backup de un directorio que no existe: '{source_dir}'")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_dir)

    filename_backup += "_" + datetime.now().strftime(date_format)
    format_backup: str = "zip"
    archive_from = os.path.dirname(source_dir)
    archive_to = os.path.basename(source_dir.strip(os.sep))
    shutil.make_archive(filename_backup, format_backup, archive_from, archive_to)
    logger.info(f"Backup creado con el nombre {'%s.%s' % (filename_backup, format_backup)}")
    return '%s.%s' % (filename_backup, format_backup)
