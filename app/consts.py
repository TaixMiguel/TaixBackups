#!/usr/bin/python3

APP_NAME = "Generador de Backups"
APP_VERSION = "0.0.2_alpha"


class Database:
    Backup = "dbackup"
    BackupHistory = "hbackup"


class MQTT:
    Topic: str = "/taixBackups/"
    BackupGlobal: str = "global"
