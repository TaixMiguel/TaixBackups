import logging
import time

from django_rq import job

from backups.creator import toolBackupCreator
from backups.models import Backup, BackupHistory

logger = logging.getLogger(__name__)

@job
def execute_backup_task(backup: Backup) -> None:
    logger.debug(f"Se registra un histórico asociado al Backup '{backup.name}'")
    history: BackupHistory = BackupHistory(id_backup_fk=backup)
    history.save()

    logger.info(f"Se lanza la creación del Backup '{backup.name}'")
    time_start = time.perf_counter()
    filename = 'No generado'
    status: bool = False
    try:
        logger.debug(f"Se instancia el tipo de Backup '{backup.id_storage_service_fK}'")
        backup_creator = toolBackupCreator.get_instance_creator(backup_code=backup.id_storage_service_fK.code,
                                                                source_dir=backup.source_dir,
                                                                destination_dir=backup.destination_dir)
        if backup_creator:
            if backup.user:
                backup_creator.set_user(user=backup.user, password=backup.password)
            logger.debug("Se ejecuta la creación del Backup")
            filename = backup_creator.create_backup()
            status = True
    except FileNotFoundError as error:
        logger.info(f"El backup '{backup.name}' no se ha generado por un error")
        # TODO: eliminar el backup generado, si se ha generado
        logger.exception(error)
    time_end = time.perf_counter()

    logger.debug(f"Se actualiza el histórico asociado al Backup '{backup.name}'")
    history.backup_size = backup_creator.size if backup_creator else 0
    history.status = 'COMPLETE' if status else 'ERROR'
    history.duration = time_end - time_start
    history.backup_name = filename
    history.save()

    while BackupHistory.objects.filter(id_backup_fk=backup, status=True).count() > backup.n_backups_max:
        logger.debug(f"Se elimina el primer histórico del backup '{backup.name}' por pasarnos del tope de "
                     f"{backup.n_backups_max}")
        backup.__remove_first_history(backup_creator)

    if status:
        # TODO: lanzar el aviso MQTT de último backup generado
        pass

        if backup.sw_sensor_mqtt:
            # TODO: actualizar sensor MQTT concreto si procede
            pass
