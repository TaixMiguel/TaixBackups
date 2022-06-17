#!/usr/bin/python3

from app import db
from app.consts import Database
import datetime
import logging
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)


class BackupHistory(db.Model):
    __tablename__ = Database.BackupHistory

    id: int = db.Column(db.Integer, primary_key=True)
    id_backup_fk: int = db.Column(db.Integer, db.ForeignKey(Database.Backup+'.id'), nullable=False)
    backup_name: str = db.Column(db.String(), nullable=False)
    backup_size: float = db.Column(db.Float, default=0)
    status: bool = db.Column(db.Boolean, default=False)
    duration: float = db.Column(db.Float, default=0)
    audit_date: datetime = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def save(self) -> None:
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        logger.info(f"Se elimina el histórico del backup {self.backup_name} con estado {self.status}")
        db.session.delete(self)
        db.session.commit()

    def format_duration(self) -> str:
        minutes, seconds = divmod(self.duration, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
