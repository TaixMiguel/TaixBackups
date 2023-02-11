#!/usr/bin/python3

from abc import ABC, abstractmethod
import getopt
import logging
import os
import sys

from backups.creator import toolBackupCreator

logger = logging.getLogger(__name__)


class BackupCreator(ABC):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        self.size = None
        self._user: str = None
        self._password: str = None
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.filename_backup = filename_backup

    def set_user(self, user: str = "", password: str = ""):
        self._user = user
        self._password = password

    def create_backup(self, date_format: str = "%Y%m%d_%H%M%S") -> str:
        filename: str = toolBackupCreator.create_backup(source_dir=self.source_dir,
                                                        destination_dir=self.destination_dir,
                                                        filename_backup=self.filename_backup,
                                                        date_format=date_format)

        self.size: int = os.path.getsize(filename)
        logger.info(f"Se procede a la subida del backup '{filename}' al servidor escogido")
        self.upload_backup(filename_upload=filename)
        return filename

    @abstractmethod
    def upload_backup(self, filename_upload: str):
        pass

    @abstractmethod
    def remove_backup(self, filename_backup: str):
        pass


if __name__ == '__main__':
    source: str = ''
    destination: str = ''
    backup_type: str = 'LOCAL'
    argumentList = sys.argv[1:]
    options = "t:s:d:"
    long_options = ["type=", "source=", "destination="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:
            if currentArgument in ("-t", "--type"):
                backup_type = currentValue
            if currentArgument in ("-s", "--source"):
                source = currentValue
            elif currentArgument in ("-d", "--destination"):
                destination = currentValue
    except getopt.error as err:
        print(str(err))

    if not source:
        source = input("Directorio al que hacer el backup: ")
    if not destination:
        destination = input("Directorio donde guardar la copia: ")

    creator = toolBackupCreator.get_instance_creator(backup_type, source_dir=source, destination_dir=destination)
    creator.create_backup()
