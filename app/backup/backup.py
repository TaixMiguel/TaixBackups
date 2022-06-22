#!/usr/bin/python3

from app import db
from app.backup.backupHistory import BackupHistory
from app.backup.creator import toolBackupCreator
from app.consts import Database
from app.mqtt import mqtt
import logging
import time

logger = logging.getLogger(__name__)


class Backup(db.Model):
    __tablename__ = Database.Backup

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True, nullable=False)
    description: str = db.Column(db.String, nullable=True)
    server: str = db.Column(db.String(8), nullable=False)
    source_dir: str = db.Column(db.String(256), nullable=False)
    destination_dir: str = db.Column(db.String(256), nullable=False)
    user = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    n_backups_max: int = db.Column(db.Integer, default=10)
    sw_sensor_mqtt: bool = db.Column(db.Boolean, default=False)

    def save(self) -> None:
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def create_backup(self) -> bool:
        status: bool = False
        logger.info(f"Se lanza la creación del Backup '{self.name}'")
        time_start = time.perf_counter()
        try:
            logger.debug(f"Se instancia el tipo de Backup '{self.server}'")
            backup_creator = toolBackupCreator.get_instance_creator(backup_code=self.server, source_dir=self.source_dir,
                                                                    destination_dir=self.destination_dir)
            if self.user:
                backup_creator.set_user(user=self.user, password=self.password)
            logger.debug("Se ejecuta la creación del Backup")
            filename = backup_creator.create_backup()
            status = True
        except FileNotFoundError as error:
            logger.info(f"El backup '{self.name}' no se ha generado")
            # TODO: eliminar el backup generado, si se ha generado
            logger.exception(error)
            filename = 'No generado'
        time_end = time.perf_counter()

        logger.debug(f"Se registra un histórico asociado al Backup '{self.name}'")
        history: BackupHistory = BackupHistory(id_backup_fk=self.id, backup_name=filename,
                                               backup_size=backup_creator.size, status=status,
                                               duration=time_end-time_start)
        history.save()

        while self.__get_number_history_correct() > self.n_backups_max:
            logger.debug(f"Se elimina el primer histórico del backup '{self.name}' por pasarnos del tope de "
                         f"{self.n_backups_max}")
            self.__remove_first_history(backup_creator)

        if status:
            client_mqtt: mqtt.MQTT = mqtt.MQTT()
            state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastBackup')
            client_mqtt.send_message(topic=state_topic, payload=self.name, retain=True)

            state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastExecution')
            client_mqtt.send_message(topic=state_topic, payload=int(time.time()), retain=True)
            client_mqtt.disconnect()

        # TODO: actualizar sensor MQTT concreto si procede
        # if self.sw_sensor_mqtt:
        return status

    def get_last_history(self) -> BackupHistory:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).order_by(BackupHistory.id.desc()).first()

    def get_history(self) -> []:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).filter_by(status=True).order_by(BackupHistory.id).\
            all()

    def __get_number_history_correct(self) -> int:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).filter_by(status=True).count()

    def __remove_first_history(self, backup_creator) -> None:
        history: BackupHistory = self.get_history()[0]
        backup_creator.remove_backup(history.backup_name)
        history.delete()

    @staticmethod
    def get_instance(id_backup: int):
        return Backup.query.get(id_backup)

    @staticmethod
    def get_instances():
        return Backup.query.all()
