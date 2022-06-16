#!/usr/bin/python3

from app import db
from app.backup.backupHistory import BackupHistory
from app.backup.creator import toolBackupCreator
from app.consts import Database
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

    def create_backup(self) -> None:
        status: bool = False
        logger.info(f"Se lanza la creación del Backup {self.name}")
        time_start = time.perf_counter()
        try:
            logger.debug(f"Se instancia el tipo de Backup {self.server}")
            tool = toolBackupCreator.get_instance_backup(backup_code=self.server, source_dir=self.source_dir,
                                                         destination_dir=self.destination_dir)
            logger.debug("Se ejecuta la creación del Backup")
            # TODO: obtener el tamaño del fichero generado
            filename = tool.create_backup(user=self.user, password=self.password)
            status = True
        except FileNotFoundError as error:
            logger.exception(error)
        time_end = time.perf_counter()

        logger.debug(f"Se registra un histórico asociado al Backup")
        history: BackupHistory = BackupHistory(id_backup_fk=self.id, backup_name=filename, backup_size=0, status=status,
                                               duration=time_end-time_start)
        history.save()

        while self.__get_number_history_correct() > self.n_backups_max:
            logger.debug(f"Se elimina el primer histórico del backup {self.name} por pasarnos del tope "
                         f"{self.n_backups_max}")
            # TODO: eliminar histórico completo (fichero incluido)
            self.__remove_first_history()

        # TODO: actualizar sensor MQTT si procede
        # TODO: actualizar sensor MQTT concreto si procede

    def get_last_history(self) -> BackupHistory:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).order_by(BackupHistory.id.desc()).first()

    def get_history(self) -> []:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).filter_by(status=True).order_by(BackupHistory.id).\
            all()

    def __get_number_history_correct(self) -> int:
        return BackupHistory.query.filter_by(id_backup_fk=self.id).filter_by(status=True).count()

    def __remove_first_history(self) -> None:
        self.get_history()[0].delete()

    @staticmethod
    def get_instance(id_backup: int):
        return Backup.query.get(id_backup)

    @staticmethod
    def get_instances():
        return Backup.query.all()
