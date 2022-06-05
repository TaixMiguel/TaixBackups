#!/usr/bin/python3

from abc import ABC, abstractmethod
import getopt
import toolBackups
import sys


class Backup(ABC):
    def __init__(self, source_dir: str, destination_dir: str, filename_backup: str):
        self.source_dir = source_dir
        self.destination_dir = destination_dir
        self.filename_backup = filename_backup

    def create_backup(self, date_format: str = "%Y%m%d_%H%M%S") -> bool:
        try:
            filename: str = toolBackups.create_backup(source_dir=self.source_dir, destination_dir=self.destination_dir,
                                                      filename_backup=self.filename_backup, date_format=date_format)
        except FileNotFoundError:
            return False

        # Mover el archivo a donde toca
        self.upload_backup(filename_upload=filename)
        return True

    @abstractmethod
    def upload_backup(self, filename_upload: str):
        pass


if __name__ == '__main__':
    source: str = ''
    destination: str = ''
    argumentList = sys.argv[1:]
    options = "s:d:"
    long_options = ["source=", "destination="]

    try:
        arguments, values = getopt.getopt(argumentList, options, long_options)

        for currentArgument, currentValue in arguments:
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

    backup = toolBackups.get_instance_backup('LOCAL', source_dir=source, destination_dir=destination)
    backup.create_backup()
