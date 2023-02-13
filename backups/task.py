import logging
import time

from django_rq import job

from app import kTaixBackups
from app.configApp import ConfigApp
from backups.creator import toolBackupCreator
from backups.models import Backup, BackupHistory
from backups.mqtt import mqtt

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
    history.status = kTaixBackups.Backup.STATUS_COMPLETE if status else kTaixBackups.Backup.STATUS_ERROR
    history.duration = time_end - time_start
    history.backup_name = filename
    history.save()

    while backup.n_backups_max < BackupHistory.objects.filter(id_backup_fk=backup, status=kTaixBackups.Backup.STATUS_COMPLETE).count():
        logger.debug(f"Se elimina el primer histórico del backup '{backup.name}' por pasarnos del tope de "
                     f"{backup.n_backups_max}")
        BackupHistory.objects.filter(id_backup_fk=backup)[0].delete()

    if status and ConfigApp().get_value_boolean(kTaixBackups.Config.MQTT.ROOT, kTaixBackups.Config.MQTT.SWITCH_ENABLED):
        logger.debug(f"Se informa de la generación del backup {backup.name} por MQTT")
        client_mqtt: mqtt.MQTT = mqtt.MQTT()
        state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastBackup')
        client_mqtt.send_message(topic=state_topic, payload=backup.name, retain=True)

        state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastExecution')
        client_mqtt.send_message(topic=state_topic, payload=int(time.time()), retain=True)
        client_mqtt.disconnect()

        if backup.sw_sensor_mqtt:
            # TODO: actualizar sensor MQTT concreto si procede
            pass
