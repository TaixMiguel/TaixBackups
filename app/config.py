#!/usr/bin/python3

import app
import paho.mqtt.client as mqtt
from threading import Lock


class __SingletonConfig(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Config(metaclass=__SingletonConfig):
    __application: app = None

    def load(self, application: app) -> None:
        self.__application = application

    def sw_mqtt(self) -> bool:
        return self.__application.config['MQTT_SERVER']

    def get_client_mqtt(self) -> mqtt.Client:
        client: mqtt.Client = None
        if self.sw_mqtt():
            client = mqtt.Client('TaixBackups')
            client.username_pw_set(username=self.__application.config['MQTT_USER'],
                                   password=self.__application.config['MQTT_PASS'])
            client.connect(self.__application.config['MQTT_SERVER'])
        return client
