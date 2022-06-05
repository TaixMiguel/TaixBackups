from datetime import datetime
import shutil
import os


def create_backup(source_dir: str, destination_dir: str, filename_backup: str = "backup",
                  date_format: str = "%Y%m%d_%H%M%S"):
    # TODO: añadir línea al log
    print("Se va a crear un backup del directorio {}".format(source_dir))

    # Controlar la existencia de los directorios
    if not os.path.exists(source_dir):
        # TODO: añadir línea al log
        print("No se puede realizar un backup de un directorio que no existe: '{}' ".format(source_dir))
        return

    if not os.path.exists(destination_dir):
        # TODO: añadir línea al log
        print("El directorio {} no existe, se crea de forma automática".format(destination_dir))
        os.makedirs(destination_dir)

    filename_backup += "_" + datetime.now().strftime(date_format)
    format_backup: str = "zip"
    archive_from = os.path.dirname(source_dir)
    archive_to = os.path.basename(source_dir.strip(os.sep))
    shutil.make_archive(filename_backup, format_backup, archive_from, archive_to)
    shutil.move('%s.%s' % (filename_backup, format_backup), destination_dir)


if __name__ == '__main__':
    print("Ejecutando un script desde la línea de comandos")
    source = input("Directorio al que hacer el backup: ")
    destination = input("Directorio donde guardar la copia: ")
    create_backup(source_dir=source, destination_dir=destination)
