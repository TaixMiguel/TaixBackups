#!/usr/bin/python3

from app import consts
from app.config import Config
import paho.mqtt.client as mqtt


def format_topic(topic_prefix: str, topic_subfix: str, backup_id: str = consts.MQTT.BackupGlobal) -> str:
    return topic_prefix + consts.MQTT.Topic + backup_id + '/' + topic_subfix


class MQTT:
    __client: mqtt.Client = None

    def __init__(self):
        self.__client = Config().get_client_mqtt()

    def send_message(self, topic: str, payload: str, retain: bool = False):
        if self.__client:
            self.__client.publish(topic=topic, payload=payload, retain=retain)

    def disconnect(self):
        if self.__client:
            self.__client.disconnect()
