#!/usr/bin/python3

import app
from app import consts
from app.config import Config
from app.mqtt import mqtt, mqttDiscovery
from app.cron.daemonWatcher import DaemonWatcher
from app.mqtt.mqttDiscovery import MQTTDevice, MQTTEntity
import logging

logger = logging.getLogger(__name__)


def format_object_id(backup_id: str, object_id: str) -> str:
    return consts.MQTT.Topic + backup_id + '/' + object_id


def create_sensor(client_mqtt: mqtt.MQTT, type: str, name: str, payload: str) -> None:
    topic: str = "homeassistant/" + type + "/" + name + "/config"
    client_mqtt.send_message(topic=topic, payload=payload)


def create_sensor_last_execution(client_mqtt: mqtt.MQTT, device: MQTTDevice, backup_id: str = consts.MQTT.BackupGlobal):
    object_id: str = format_object_id(backup_id=backup_id, object_id='lastExecution')
    state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastExecution', backup_id=backup_id)
    entity_last_execution: MQTTEntity = mqttDiscovery.create_sensor(mqtt_device=device, name='Última ejecución',
                                                                    state_topic=state_topic, object_id=object_id,
                                                                    retain=True)
    entity_last_execution.icon = 'mdi:calendar-clock'
    create_sensor(client_mqtt=client_mqtt, type='sensor', name=backup_id+'_lastExecution',
                  payload=entity_last_execution.format_json())


def create_sensor_last_backup(client_mqtt: mqtt.MQTT, device: MQTTDevice, backup_id: str = consts.MQTT.BackupGlobal):
    object_id: str = format_object_id(backup_id=backup_id, object_id='lastBackup')
    state_topic: str = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastBackup', backup_id=backup_id)
    entity_last_backup: MQTTEntity = mqttDiscovery.create_sensor(mqtt_device=device, name='Último backup',
                                                                 state_topic=state_topic, object_id=object_id,
                                                                 retain=True)
    entity_last_backup.icon = 'mdi:cloud-upload-outline'
    create_sensor(client_mqtt=client_mqtt, type='sensor', name=backup_id+'_lastBackup',
                  payload=entity_last_backup.format_json())


def servicios_mqtt() -> None:
    if not Config().sw_mqtt():
        return

    logger.debug("Se lanza el servicio MQTT")
    device: MQTTDevice = MQTTDevice(manufacturer='TaixMiguel', name=consts.APP_NAME, model='TaixBackups',
                                    version=consts.APP_VERSION)
    device.add_identifier('taix_generador_backups')

    client_mqtt: mqtt.MQTT = mqtt.MQTT()
    create_sensor_last_execution(client_mqtt=client_mqtt, device=device)
    create_sensor_last_backup(client_mqtt=client_mqtt, device=device)
    client_mqtt.disconnect()

    # TODO: llamar a todas las instancias de Backup y crear su entidad correspondiente


def servicios_cron() -> None:
    logger.debug("Se lanza el vigilador de demonios")
    daemon_watcher: DaemonWatcher = DaemonWatcher()
    daemon_watcher.run()


class ToolInit:
    __app: app

    def __init__(self, application: app) -> None:
        self.__app = application

    def iniciar_servicios(self) -> None:
        logger.debug("Se lanzan el resto de servicios definidos en el arranque")
        configuration: Config = Config()
        configuration.load(application=self.__app)
        servicios_mqtt()
        servicios_cron()
