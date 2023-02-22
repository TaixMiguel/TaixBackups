#!/usr/bin/python3
import datetime
import logging
import time

from app import kTaixBackups
from app.configApp import ConfigApp
from backups.models import Backup
from backups.mqtt import mqtt
from backups.mqtt.mqttDiscovery import create_sensor, MQTTEntity, MQTTDevice, create_device, MQTTTool

logger = logging.getLogger(__name__)

def send_mqtt_home_assistant_entity(client_mqtt: mqtt.MQTT, entity: MQTTEntity) -> None:
    client_mqtt.send_message(topic=entity.get_config_topic(), payload=entity.format_json(), retain=True)


class DaemonWatcher:

    turnOff: bool
    timeSleep: int
    warehouse: dict = {}

    def __init__(self) -> None:
        # TODO: cambiar a un minuto cuando toque mirar en BBDD
        self.timeSleep = 1 * 60 * 60  # Cada hora (se mide en segundos)

    def run(self) -> None:
        # thread = threading.Thread(target=self.__turn_on, name='DaemonWatcher')
        # thread.start()
        self.create_mqtt_entities()

    def __turn_on(self) -> None:
        logger.debug('Inicio de DaemonWatcher')
        self.turnOff = False

        while not self.turnOff:
            logger.debug('Nueva iteración')
            self.create_mqtt_entities()
            time.sleep(self.timeSleep)

    def turn_off(self) -> None:
        self.turnOff = True

    def create_mqtt_entities(self) -> None:
        if ConfigApp().get_value_boolean(kTaixBackups.Config.MQTT.ROOT, kTaixBackups.Config.MQTT.SWITCH_ENABLED):
            time_last_execution = self.get_object('last_execution_mqtt')
            if time_last_execution:
                next_execution = time_last_execution + datetime.timedelta(hours=12)
                if datetime.datetime.now() < next_execution:
                    return

            client_mqtt: mqtt.MQTT = mqtt.MQTT()
            logger.debug('Creación del dispositivo MQTT')

            state_topic: str = None
            entity: MQTTEntity = None
            mqtt_device: MQTTDevice = create_device()
            logger.debug('Creación del sensor global última ejecución')
            state_topic = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastExecution')
            entity = create_sensor(mqtt_device=mqtt_device, name='Última ejecución', state_topic=state_topic,
                                   object_id='taixBackups_global_lastExecution', retain=True)
            send_mqtt_home_assistant_entity(client_mqtt=client_mqtt, entity=entity)

            logger.debug('Creación del sensor global último backup')
            state_topic = mqtt.format_topic(topic_prefix='stat', topic_subfix='lastBackup')
            entity = create_sensor(mqtt_device=mqtt_device, name='Último backup', state_topic=state_topic, retain=True,
                                   object_id='taixBackups_global_lastBackup')
            send_mqtt_home_assistant_entity(client_mqtt=client_mqtt, entity=entity)

            backups = Backup.objects.filter(sw_sensor_mqtt=True)
            for aux_backup in backups:
                mqtt_tool: MQTTTool = MQTTTool(mqtt_device, aux_backup.name)
                logger.debug(f'Creación del sensor de última ejecución para el backup {aux_backup}')
                entity = mqtt_tool.create_sensor_last_execution()
                send_mqtt_home_assistant_entity(client_mqtt=client_mqtt, entity=entity)

                logger.debug(f'Creación del sensor de estado para el backup {aux_backup}')
                entity = mqtt_tool.create_sensor_state_backup()
                send_mqtt_home_assistant_entity(client_mqtt=client_mqtt, entity=entity)
            client_mqtt.disconnect()
            self.warehouse['last_execution_mqtt'] = datetime.datetime.now()

    def get_object(self, key: str):
        try:
            return self.warehouse[key]
        except KeyError:
            return None
