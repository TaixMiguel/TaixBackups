#!/usr/bin/python3

from abc import ABC, abstractmethod
import getopt
from . import toolBackupCreator
import sys


class BackupCreator(ABC):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.filename_backup = filename_backup

    def create_backup(self, user: str = "", password: str = "", date_format: str = "%Y%m%d_%H%M%S") -> bool:
        try:
            filename: str = toolBackupCreator.create_backup(source_dir=self.source_dir,
                                                            destination_dir=self.destination_dir,
                                                            filename_backup=self.filename_backup,
                                                            date_format=date_format)

            # TODO: añadir línea al log
            print(f"Se procede a la subida del backup {filename} al servidor escogido")
            self.upload_backup(filename_upload=filename, user=user, password=password)
        except FileNotFoundError:
            return False
        return True

    @abstractmethod
    def upload_backup(self, filename_upload: str, user: str, password: str):
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

    backup = toolBackupCreator.get_instance_backup(backup_type, source_dir=source, destination_dir=destination)
    backup.create_backup()
