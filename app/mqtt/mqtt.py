#!/usr/bin/python3

from app import consts
from app.config import Config
import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger(__name__)


def format_topic(topic_prefix: str, topic_subfix: str, backup_id: str = consts.MQTT.BackupGlobal) -> str:
    return topic_prefix + consts.MQTT.Topic + backup_id + '/' + topic_subfix


class MQTT:
    __client: mqtt.Client = None

    def __init__(self):
        self.__client = Config().get_client_mqtt()

    def send_message(self, topic: str, payload: str, retain: bool = False):
        if self.__client:
            logger.debug(f"Se envía el mensaje '{topic}' => '{payload}'{' [retain]' if retain else ''}")
            self.__client.publish(topic=topic, payload=payload, retain=retain)

    def disconnect(self):
        if self.__client:
            logger.debug('Se desconecta el cliente MQTT')
            self.__client.disconnect()
