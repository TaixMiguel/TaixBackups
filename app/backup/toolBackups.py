#!/usr/bin/python3

from backupLocal import LocalBackup
from datetime import datetime
import errno
import shutil
import os


def get_instance_backup(backup_code: str, source_dir: str, destination_dir: str, filename_backup: str = "backup"):
    if backup_code in ('local', 'LOCAL'):
        return LocalBackup(source_dir=source_dir, destination_dir=destination_dir, filename_backup=filename_backup)

    # TODO: añadir línea al log
    print(f"No se ha encontrado instancia con el código '{backup_code}'")


def create_backup(source_dir: str, destination_dir: str, filename_backup: str = "backup",
                  date_format: str = "%Y%m%d_%H%M%S") -> str:
    # TODO: añadir línea al log
    print("Se va a crear un backup del directorio {}".format(source_dir))

    # Controlar la existencia de los directorios
    if not os.path.exists(source_dir):
        # TODO: añadir línea al log
        print("No se puede realizar un backup de un directorio que no existe: '{}' ".format(source_dir))
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), source_dir)

    filename_backup += "_" + datetime.now().strftime(date_format)
    format_backup: str = "zip"
    archive_from = os.path.dirname(source_dir)
    archive_to = os.path.basename(source_dir.strip(os.sep))
    shutil.make_archive(filename_backup, format_backup, archive_from, archive_to)
    return '%s.%s' % (filename_backup, format_backup)
