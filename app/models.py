#!/usr/bin/python3

from . import db
from .backup import toolBackupCreator


class Backup(db.Model):
    __tablename__ = 'dbackup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String, nullable=True)
    server = db.Column(db.String(8), nullable=False)
    source_dir = db.Column(db.String(256), nullable=False)
    destination_dir = db.Column(db.String(256), nullable=False)
    user = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def create_backup(self):
        tool = toolBackupCreator.get_instance_backup(backup_code=self.server, source_dir=self.source_dir,
                                                     destination_dir=self.destination_dir)
        tool.create_backup()

    @staticmethod
    def get_instance(id_backup: int):
        return Backup.query.get(id_backup)

    @staticmethod
    def get_instances():
        return Backup.query.all()
